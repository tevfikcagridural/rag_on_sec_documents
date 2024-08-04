import streamlit as st
from services.inference_service import get_chat_engine

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me about uploaded SEC Form 10-Q documents!"}
    ]

if "chat_engine" not in st.session_state.keys(): # Initialize the chat engine
    st.session_state.chat_engine = get_chat_engine()
    

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt) # type: ignore
            response.response = response.response.replace('$', '\$') # Avoid TeX formating within the messages #type: ignore
            sources = set([node.metadata["file_name"] for node in response.source_nodes])
            st.write(f'*Source(s):* *{", ".join(sorted(sources))}*')
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message) # Add response to message history

