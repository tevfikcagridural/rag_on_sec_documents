from src.models.embedding_model import load_embedding_model, get_embeddings
from src.models.llm_model import load_llm_model, generate_response

embedding_model = load_embedding_model()
llm_model = load_llm_model()

def retrieve_and_generate(query):
    embeddings = get_embeddings(embedding_model, query)
    response = generate_response(llm_model, embeddings)
    return response
