# Small Scale Production-grade RAG
        
The system can answer complex queries such as combining information from multi pages or even multiple documents. Data, QnA pairs are originated from [Docugami Knowledge Graph Retrieval Augmented Generation Datasets](https://github.com/docugami/KG-RAG-datasets/)

## Documents Information
The SEC Form 10-Q is a quarterly report required by the Securities and Exchange Commission (SEC) that provides unaudited financial statements and other information about a company's operations and financial condition. While there is a basic formatting standard, different companies' forms can vary in style and explanation. Most importantly, these forms contain complex tables that store valuable information, making accurate extraction of this information crucial.

This app contains these forms for the following companies; Apple, Intel, Microsoft, Nvidia from 2022 Q3 to 2024 Q1.

## Tech Stack
- **Data Framework:** [LlamaIndex](https://www.llamaindex.ai)
- **PDF Parsing:** [LlamaParse](https://cloud.llamaindex.ai/)
- **Vector DB:** [Pinecone](https://www.pinecone.io)
- **LLM:** [OpenAI GPT-3.5-Turbo](https://platform.openai.com/docs/models/gpt-3-5-turbo)
- **Embedding Model:** [OpenAI Text Embedding 3 Large](https://platform.openai.com/docs/models/embeddings)
- **Reranking:** [Cohere](https://cohere.com)
- **Observation:** [Langfuse](https://langfuse.com)
- **Containerization:** [Docker](https://www.docker.com)
- **Cloud Platform:** [Google Run](https://cloud.google.com/run/docs/overview/what-is-cloud-run)
- **GUI Framework:** [Streamlit](https://streamlit.io)

## Other Technical Details
- **Total pages of docs:** 1364
- **Vector Length:** 1024
- **Similarity Metric:** Cosine
- **Prompt Management:** LangchainHub
- **Query Rephrasing:** Dynamic metadata retrieval 
- **Node Postprocessors:**
    - [SimilarityPostprocessor](https://docs.llamaindex.ai/en/stable/module_guides/querying/node_postprocessors/node_postprocessors/#similaritypostprocessor), 
    - [LongContextReorder](https://docs.llamaindex.ai/en/stable/module_guides/querying/node_postprocessors/node_postprocessors/#longcontextreorder)

## Cost Breakdown
- **Ingestion of all documents**
    - OpenAI Embedding: 0,14$
- **Inference**:
    - Open AI: *TO BE ADDED*
    - GCloud: *TO BE ADDED*

## Sample Questions
|Question Type|Question|Source Docs|
|-----|-----|-----|
|Multi-Doc|How has Apple's total net sales changed over time?|2022-Q3-AAPL, 2023-Q1-AAPL, 2023-Q2-AAPL, 2023-Q3-AAPL 2024-Q1-APPL|
|Single-Doc|How does Microsoft's revenue distribution across its various business segments in the latest 10-Q compare to the cost of sales for those segments?|2023-Q3-MSFT|
    
## Further Improvements & Known Issues
- Fast API integration
- Concurrency and Parallelization
- Caching (both for ingestion and inference)
- Document management
- Tool usage (e.g Pulling trading symbol)
- Image extraction & multi-modality
- Resource citing
- Hybrid datastoring 
- Unit testing
- Guardrailing to avoid any halucinations
- Robust tool usage for better metadata filtering
- Table extraction improvement
- Clutter clening