from typing import Any
from llama_index.core import Settings, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core.vector_stores import MetadataInfo, VectorStoreInfo
from llama_index.core.retrievers import VectorIndexAutoRetriever
from llama_index.core.chat_engine import CondenseQuestionChatEngine
from llama_index.core.postprocessor import LongContextReorder
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.callbacks import CallbackManager
from langfuse.llama_index import LlamaIndexCallbackHandler
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.core.prompts import LangchainPromptTemplate
from langchain import hub
from qdrant_client import QdrantClient
import config

# Env variables
OPENAI_API_KEY      = config.OPENAI_API_KEY
LLM_MODEL           = config.LLM_MODEL
LLM_TEMP            = config.LLM_TEMPERATURE
EMBED_MODEL         = config.EMBEDDING_MODEL
EMBED_DIM           = config.EMBEDDING_DIMENSIONS
QDRANT_API_KEY      = config.QDRANT_API_KEY
QDRANT_URL          = config.QDRANT_URL
LANGCHAIN_API_KEY   = config.LANGCHAIN_API_KEY
LANGCHAIN_PROJECT   = config.LANGCHAIN_PROJECT
COHERE_API_KEY      = config.COHERE_API_KEY
LANGFUSE_HOST       = config.LANGFUSE_HOST
LANGFUSE_PUBLIC_KEY = config.LANGFUSE_PUBLIC_KEY 
LANGFUSE_SECRET_KEY = config.LANGFUSE_SECRET_KEY

# Langfuse as callback manager for query observation 
langfuse_callback_handler = LlamaIndexCallbackHandler(public_key=LANGFUSE_PUBLIC_KEY, secret_key=LANGFUSE_SECRET_KEY, host=LANGFUSE_HOST)
Settings.callback_manager = CallbackManager([langfuse_callback_handler])

def get_chat_engine() -> CondenseQuestionChatEngine:
    """Creates a condense question chat engine from vector store.

    Returns:
        CondenseQuestionChatEngine: Chat engine to be used in chat page
    """
    
    # Models settings
    Settings.llm = OpenAI(model=LLM_MODEL, temperature=LLM_TEMP, api_key=OPENAI_API_KEY)
    Settings.embed_model = OpenAIEmbedding(model=EMBED_MODEL, dimensions=EMBED_DIM, api_key=OPENAI_API_KEY)
    
    # Load Qdrant as vector store
    qdrant_client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
        )
    vector_store = QdrantVectorStore(
        client=qdrant_client,
        collection_name='chunks'
    )

    # Create vector store index
    vector_index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    
    # Specially extracted metadata detailed information for dynamic metadata filtering 
    vector_store_info = VectorStoreInfo(
        content_info="FORM 10-Q of SEC Documents of Companies",
        metadata_info=[
            MetadataInfo(
                name="company_trading_symbol",
                description="Trading symbol of the company for NASDAQ. AAPL for Apple, AMZN for Amazon, INTC for Intel, MSFT for Microsoft, and NVDA for Nvidia",
                type="string",
                ),
            MetadataInfo(
                name="report_year",
                description="Creation year of the document",
                type="string",
                ),
            MetadataInfo(
                name="report_quarter",
                description="Creation quarter of the document. Only can be one of Q1, Q2, or Q3",
                type="string",
                ),
            ],
    )
        
    # Define retriever for dynamic metadata filtering
    retriever = VectorIndexAutoRetriever(
        index=vector_index,
        vector_store_info=vector_store_info,
        similarity_top_k=5,
        empty_query_top_k=10,  # if only metadata filters are specified, this is the limit
        verbose=True,
        # this is a hack to allow for blank queries in pinecone
        default_empty_query_vector=[0] * 1024, #1024 is vector dimension # type: ignore
    )
    
    ## Prompt management
    def format_additional_instrs(**kwargs: Any) -> str:
        # Resource: https://docs.llamaindex.ai/en/stable/examples/vector_stores/pinecone_auto_retriever/?h=format_additional_instrs#2b-implement-dynamic-metadata-retrieval
        """Format examples into a string."""
        context_str = (
            "If the query doesn't expilicitly mention about a specific filter return [] for the filter value."
            "The user probably won't mention the trading symbol expilicitly. Instead you should infer from the name of the company."
        )
        return context_str
    
    # Get prompts from langchain hub
    lc_prompt_tmpl_metadata_filter = LangchainPromptTemplate(
        template=hub.pull("tcd/metadata-filterer"),
        function_mappings={'additional_instructions': format_additional_instrs}
    )
    lc_prompt_tmpl_rag = LangchainPromptTemplate(
        template=hub.pull("tcd/rag-prompt")
    )

    # Set prompt for metadata fitering
    retriever.update_prompts({'prompt': lc_prompt_tmpl_metadata_filter})
    
    # Convert vector index to quey engine to update final system answerer propmt
    autoindex_query_engine = RetrieverQueryEngine(
        retriever=retriever,
        node_postprocessors=[
            CohereRerank(top_n=5, api_key=COHERE_API_KEY),
            LongContextReorder()
        ]
    )
    # Set prompt for final system answerer
    autoindex_query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": lc_prompt_tmpl_rag}
    )
    
    # Set chat memory
    memory = ChatMemoryBuffer.from_defaults(token_limit=3900)
    
    # Initializie chat engine
    chat_engine = CondenseQuestionChatEngine.from_defaults(
        query_engine=autoindex_query_engine,
        memory=memory,
        verbose=True
    )
    
    # Send all the process to the langfuse
    langfuse_callback_handler.flush()
    
    return chat_engine

if __name__ == '__main__':
    engine = get_chat_engine()