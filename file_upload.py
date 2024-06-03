import streamlit as st
from utils.helpers.document_loaders import BytesIOPyMuPDFLoader, BytesIOTextLoader
from langchain_core.document_loaders import Blob
from langchain_community.document_loaders import UnstructuredExcelLoader
from tempfile import NamedTemporaryFile


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
                file_parts = file_name.split(".")
                file_name_raw , file_type = file_parts[0], file_parts[-1]
                
                if file_type == "pdf":
                    pdf_loader = BytesIOPyMuPDFLoader(pdf_stream=file)
                    documents = pdf_loader.load()
                    for doc in documents:
                        doc.metadata["source"] = file_name
                        doc.metadata["title"] = file_name_raw
                        # file_path (add url if files are kept) eg: blob, local etc
                        # add author, add uploader info
                        
                elif file_type in ["txt", "md"]:
                    blob = Blob(data=file.read())
                    documents = BytesIOTextLoader().lazy_parse(blob)
                    # add document splitting logic
                
                elif file_type in ["xls", "xlsx"]:
                    tmpfilepath = NamedTemporaryFile(dir='temp', suffix='.xlsx') 
                    print(tmpfilepath.name)
                    tmpfilepath.write(file.read())
                    # loader = UnstructuredExcelLoader("example_data/stanley-cups.xlsx", mode="elements")
                    # docs = loader.load()
                    
                st.success(body=f"Processed {file_name}", icon="📂")
    
        st.info(f"Finished processing {len(uploaded_files)} files", icon="✅")
