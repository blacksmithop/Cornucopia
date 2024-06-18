import os

import chromadb
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
from langchain.docstore.document import Document


st.markdown(
    """
<style>
    [data-testid="collapsedControl"] {
        display: none
    }
</style>
""",
    unsafe_allow_html=True,
)

option_page_map = {
    "Home": "./main.py",
    "Upload": "pages/File_Upload.py",
    "Settings": "pages/Settings.py",
}

CHROMA_DIR = "./utils/chroma_db"

navbar_options = option_menu(
    0,
    ["Settings", "Upload", "Home"],
    icons=["gear", "house", "cloud-upload"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal",
    key="navbar",
)


if navbar_options:
    if st.session_state["current_page"] != navbar_options:
        st.session_state["current_page"] = navbar_options
        page = option_page_map.get(navbar_options, None)
        if page:
            st.switch_page(page)

st.markdown("# ⚙️ Settings")

st.markdown("## ChromaDB Data Viewer")

if not os.path.isdir(CHROMA_DIR):
    st.warning(f"No chroma db directory found at {CHROMA_DIR}", icon="❗")
else:
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    for collection in client.list_collections():
        data = collection.get()

        st.markdown(f"#### Collection - {collection.name}")
        
        unique_titles={m['title'] for m in collection.get(where={"title":{"$ne":""}},include=['metadatas'])['metadatas'] if 'title' in m}

        documents = [
            Document(page_content=content, metadata={"title": meta["title"]})
            for content, meta in zip(data["documents"], data["metadatas"])
            if content != "" and len(content) > 5 and meta["title"] != ""
        ]
        title_document_map = {k:[] for k in unique_titles}

        for doc in documents:
            title_document_map[doc.metadata["title"]].append(doc.page_content)

        for topic, documents in title_document_map.items():
            with st.expander(f"**{topic}**"):
                df = pd.DataFrame({"Content": documents})
                st.dataframe(df)
