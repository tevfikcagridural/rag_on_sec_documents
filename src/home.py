import streamlit as st
import pandas as pd
## Page Config
st.set_page_config(
    page_title="SEC Documents",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
        # Small Scale Production-Grade RAG System
        
        The system can answer complex queries such as combining information from multiple pages or even multiple documents. Data, Q&A pairs are originated from [Docugami Knowledge Graph Retrieval Augmented Generation Datasets](https://github.com/docugami/KG-RAG-datasets/). Details about how question and answer sets are developed can be found in the [SEC FORM 10-Q's README](https://github.com/docugami/KG-RAG-datasets/blob/main/sec-10-q/README.md)
        
        ## Documents Information
        The SEC Form 10-Q is a quarterly report required by the Securities and Exchange Commission (SEC) that provides unaudited financial statements and other information about a company's operations and financial condition. While there is a basic formatting standard, different companies' forms can vary in style and explanation. Most importantly, these forms contain complex tables that store valuable information; accurately extracting this information is crucial.
        
        This app contains forms for the following companies; Apple, Intel, Microsoft, Nvidia, from 2022 Q3 to 2024 Q1.

        ## Tech Stack
        - **Data Framework:** [LlamaIndex](https://www.llamaindex.ai)
        - **PDF Parsing:** [LlamaParse](https://cloud.llamaindex.ai/)
        - **Vector DB:** [Pinecone](https://www.pinecone.io)
        - **LLM:** [OpenAI GPT-4o-mini](https://platform.openai.com/docs/models/gpt-4o-mini)
        - **Embedding Model:** [OpenAI Text Embedding 3 Large](https://platform.openai.com/docs/models/embeddings)
        - **Reranking:** [Cohere](https://cohere.com)
        - **Observation:** [Langfuse](https://langfuse.com)
        - **Containerization:** [Docker](https://www.docker.com)
        - **Cloud Platform:** [Google Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run)
        - **GUI Framework:** [Streamlit](https://streamlit.io)
        
        ## Other Details
        - **Chunking Strategy:** [MarkdownElementNodeParser](https://docs.llamaindex.ai/en/stable/api_reference/node_parsers/markdown_element/?h=markdownelemen#llama_index.core.node_parser.MarkdownElementNodeParser)^[1](https://github.com/run-llama/llama_index/discussions/13412)
        - **Total pages of docs:** 1364
        - **Report Period:** 2022Q3 - 2024Q1
        - **Reporting Compines:** Apple, Amazon, Intel, Microsoft, Nvidia
        - **Vector Length:** 1024
        - **Similarity Metric:** Cosine
        - **Prompt Management:** LangchainHub
        - **Query Rephrasing:** Dynamic metadata retrieval 
        - **Node Postprocessors:**
            - [CohereRerank](https://docs.llamaindex.ai/en/stable/module_guides/querying/node_postprocessors/node_postprocessors/?h=cohererera#coherererank)
            - [LongContextReorder](https://docs.llamaindex.ai/en/stable/module_guides/querying/node_postprocessors/node_postprocessors/#longcontextreorder)
        
        ## Ingestion Cost
        - **Embedding:** ~$0.16
        - **LLM:** ~$1.83
         
        ## Evaluation
         24 Sample questions with question comparison from the original data source. Also detailed processes of each answering process can be accessed via the link on the final column. The details include; OpenAi costs, metadata filtering, question rephrasing, retrieval and reranking. *(Whole texts can be viewed by double-clicking on the cell)* 
         """
         )

qna_data = pd.read_csv('data/processed/qna_data.csv')
st.dataframe(
    qna_data,
    height=900,
    column_config={"Query Trace Details": st.column_config.LinkColumn("Query Trace Details")}
    )

st.markdown(""" 
        ## Further Improvements
        - Fast API integration
        - Concurrency/Parallelization
        - Caching
        - Tool usage (e.g Pulling trading symbol)
        - Image extraction & multi-modality
        - Guardrailing
       """)