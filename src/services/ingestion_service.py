from typing import List
from llama_index.core.ingestion import IngestionPipeline, DocstoreStrategy
from llama_index.core import Settings
from llama_index.core.extractors import BaseExtractor
from llama_index.core.schema import TransformComponent, BaseNode
from llama_index.core.node_parser import MarkdownElementNodeParser
from llama_index.core import SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.storage.docstore.mongodb import MongoDocumentStore
from llama_parse import LlamaParse
from qdrant_client import QdrantClient
import re
import config

OPENAI_API_KEY      = config.OPENAI_API_KEY
LLM_MODEL           = config.LLM_MODEL
LLM_TEMP            = config.LLM_TEMPERATURE
EMBED_MODEL         = config.EMBEDDING_MODEL
EMBED_DIM           = config.EMBEDDING_DIMENSIONS
LLAMA_CLOUD_API_KEY = config.LLAMA_CLOUD_API_KEY
QDRANT_API_KEY      = config.QDRANT_API_KEY
MONGO_DB_URI        = config.MONGO_DB_URI

## Models Settings
Settings.llm = OpenAI(model=LLM_MODEL, temperature=LLM_TEMP, api_key=OPENAI_API_KEY)
Settings.embed_model = OpenAIEmbedding(model=EMBED_MODEL, dimensions=EMBED_DIM, api_key=OPENAI_API_KEY)

## Custom transformations
class TextCleaner(TransformComponent):
    def __call__(self, nodes, **kwargs) -> List[BaseNode]:
        for node in nodes:

            # Fix hyphenated words broken by newline
            node.text = re.sub(r'(\w+)-\n(\w+)', r'\1\2', node.text) # type: ignore
            
            # Fix improperly spaced hyphenated words and normalize whitespace
            node.text = re.sub(r'(\w)\s*-\s*(\w)', r'\1-\2', node.text) # type: ignore
            node.text = re.sub(r'\s+', ' ', node.text) # type: ignore
            
            # Remove useless text detected in data exploration
            unwanted_patterns = [
                r'(Apple Inc. \| Q[0-9]{1} [0-9]{4} Form 10-Q \| [0-9]+)', 
                r'Table of Contents',
                r'PART (I|II) Item [0-9]{1,2}',
                r"NVIDIA CORPORATION AND SUBSIDIARIES NOTES TO CONDENSED CONSOLIDATED FINANCIAL STATEMENTS (Continued) (Unaudited)"
            ]
            for pattern in unwanted_patterns:
                node.text = re.sub(pattern, '', node.text) # type: ignore
            
        return nodes

class CustomExtractor(BaseExtractor):
    """
    Extracts company trading signal, year and the quarter. 
    Expects the files to be named as `2023_Q3_APPL.pdf`
    """
    async def aextract(self, nodes):

        metadata_list = [
            {
                "company_trading_symbol":   node.metadata["file_name"].split('_')[-1].split('.')[0],
                "report_year":              node.metadata["file_name"].split('_')[0],
                "report_quarter":           node.metadata["file_name"].split('_')[1]
            }
            for node in nodes
        ]
        return metadata_list

def ingest(data_dir: str):
    
    # Set PDF Parsing with LlamaParse
    parser = LlamaParse(
        api_key=LLAMA_CLOUD_API_KEY, # type: ignore
        result_type= "markdown",  # type: ignore
        parsing_instruction="\
            You are parsing SEC documents for tech companies. Pay extra attention on tables since there can be complex tables without explicit row or column lines",
        invalidate_cache=False,
    )
    file_extractor = {".pdf": parser}

    ## TODO: Add a checking strategy for duplicated docs. 
        # Unfortunately LlamaIndex only checks it within the pipeline 
        # and this step runs LlamaParse unnecessarily before the pipeline runs
    # Send PDF(s) to LlamaParse and get returned markdown(s)
    documents = SimpleDirectoryReader(
        input_dir=data_dir, 
        file_extractor=file_extractor, # type: ignore
        raise_on_error=True,
    ).load_data()
    
    # Manual metadata updates
    for doc in documents:
        # Remove unnecessary metadata
        del doc.metadata['file_path']
        del doc.metadata['file_type']
        del doc.metadata['file_size']
        del doc.metadata['creation_date']
        del doc.metadata['last_modified_date']
        # Set which metadata llm and embedding model uses
        doc.excluded_embed_metadata_keys.extend(['file_name', 'company_trading_symbol','report_year', 'report_quarter',])
        doc.excluded_llm_metadata_keys.extend(['company_trading_symbol','report_year', 'report_quarter'])
        
    # Set Qdrant as vector and MongoDB as document stores
    qdrant_client = QdrantClient(url='https://e9aae357-fe24-40a4-ab94-8949f758bbd6.europe-west3-0.gcp.cloud.qdrant.io:6333', api_key=QDRANT_API_KEY)
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name='chunks'
    )
    
    doc_store=MongoDocumentStore.from_uri(MONGO_DB_URI, db_name='secDocuments', namespace='documents')

    # Set ingestion pipeline with defined transformations
    pipeline = IngestionPipeline(
        transformations=[
            TextCleaner(),
            CustomExtractor(),
            Settings.embed_model,
        ],
        vector_store=vector_store,
        docstore=doc_store,
        # Only handle duplicates. https://docs.llamaindex.ai/en/stable/api_reference/ingestion/?h=docstorestrategy.duplicates_only#llama_index.core.ingestion.pipeline.DocstoreStrategy
        docstore_strategy=DocstoreStrategy.DUPLICATES_ONLY, 
    )
    
    node_parser = MarkdownElementNodeParser(llm=Settings.llm)
    nodes = node_parser.get_nodes_from_documents(documents=documents)
    base_nodes, objects = node_parser.get_nodes_and_objects(nodes)
    
    # Run pipeline
    nodes = pipeline.run(nodes= base_nodes + objects)
    
    if nodes:
        return True