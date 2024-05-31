import streamlit as st
from src.services.rag_service import retrieve_and_generate

def main():
    st.title("RAG System")
    query = st.text_input("Enter your query:")
    if st.button("Submit"):
        response = retrieve_and_generate(query)
        st.write(response)

if __name__ == "__main__":
    main()
