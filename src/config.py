from services.secret_manager import get_secret

OPENAI_API_KEY      = get_secret('OPENAI_API_KEY')
QDRANT_API_KEY      = get_secret('QDRANT_API_KEY')
QDRANT_URL          = 'https://e9aae357-fe24-40a4-ab94-8949f758bbd6.europe-west3-0.gcp.cloud.qdrant.io:6333'
LANGCHAIN_API_KEY   = get_secret('LANGCHAIN_API_KEY')
LANGCHAIN_PROJECT   = get_secret('LANGCHAIN_PROJECT')
COHERE_API_KEY      = get_secret('COHERE_API_KEY')
LANGFUSE_HOST       = 'https://cloud.langfuse.com'
LANGFUSE_PUBLIC_KEY = get_secret('LANGFUSE_PUBLIC_KEY')
LANGFUSE_SECRET_KEY = get_secret('LANGFUSE_SECRET_KEY')
LLAMA_CLOUD_API_KEY = get_secret('LLAMA_CLOUD_API_KEY')
MONGO_DB_URI        = get_secret('MONGO_DB_URI')

LLM_MODEL       = 'gpt-3.5-turbo'
LLM_TEMPERATURE = 0.1

EMBEDDING_MODEL         = 'text-embedding-3-large' 
EMBEDDING_DIMENSIONS    = 1024
