from tempfile import NamedTemporaryFile

import streamlit as st
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_core.document_loaders import Blob

from utils.helpers.document_loaders import (BytesIOPyMuPDFLoader,
                                            BytesIOTextLoader)
from utils.helpers.text_splitter import semantic_splitter
from utils.retrievers import upload_docs_db as chroma

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
                file_name_raw, file_type = file_parts[0], file_parts[-1]

                try:
                    if file_type == "pdf":
                        pdf_loader = BytesIOPyMuPDFLoader(pdf_stream=file)
                        documents = pdf_loader.load()
                        # file_path (add url if files are kept) eg: blob, local etc
                        # add author, add uploader info

                    elif file_type in ["txt", "md"]:
                        blob = Blob(data=file.read())
                        docs = BytesIOTextLoader().lazy_parse(blob)
                        documents = semantic_splitter.create_documents(
                            [i.page_content for i in docs]
                        )

                    elif file_type in ["xls", "xlsx"]:
                        tmpfilepath = NamedTemporaryFile(
                            dir="temp", suffix=".xlsx", delete=False
                        )
                        tmpfilepath.write(file.read())
                        loader = UnstructuredExcelLoader(tmpfilepath.name)
                        docs = loader.load()
                        documents = semantic_splitter.create_documents(
                            [i.page_content for i in docs]
                        )

                        st.success(body=f"Processed {file_name}", icon="📂")

                    for doc in documents:
                        doc.metadata["source"] = file_name
                        doc.metadata["title"] = file_name_raw

                    with st.spinner("Adding document to Chroma DB"):
                        chroma.add_documents(documents=documents)

                except NameError:
                    st.error(f"Failed to process file {file_name}")

        st.info(f"Finished processing {len(uploaded_files)} files", icon="✅")
