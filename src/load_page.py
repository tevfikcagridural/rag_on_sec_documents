import streamlit as st
from services.ingestion_service import ingest
import os
import shutil

temp_dir = 'streamlit_tmp/'

def save_uploaded_file(uploaded_file):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)
    original_name = file.name.split('/')[-1]
    file_path = os.path.join(temp_dir, original_name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# File upload
files = st.file_uploader("Upload file", type=['pdf'], accept_multiple_files=True)

if files:
    submit = st.button('Process and upload document(s)')
    # Process each file
    for file in files:
        # Save file to the temporary directory
        file_path = save_uploaded_file(file)
        # Wait for the user to submit the ingestion process
        if submit:
            is_ingested = ingest(temp_dir)
            if is_ingested:
                st.info(f"Ingestion process completed for **{file.name}**")
            else:
                st.error(f"Ingestion process failed for **{file.name}**")
    
    submit = False
    
    # Cleanup temporary dir
    shutil.rmtree(temp_dir)