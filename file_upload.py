import streamlit as st
from time import sleep



uploaded_files = st.file_uploader(
    label="Upload files",
    accept_multiple_files=True,
    key="file_upload",
    help="Upload files to your knowledge base",
)


if uploaded_files:
    if st.button("Upload files", type="primary"):
        for file in uploaded_files:
            file_name = file.name
            with st.spinner(f"Processing {file_name}"):
                file_type = file_name.split(".")[-1]
                sleep(3)
                st.success(body=f"Processed {file_name}", icon="📂")
    
    st.info(f"Finished processing {len(uploaded_files)} files", icon="✅")
