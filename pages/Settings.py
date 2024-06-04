import streamlit as st
from streamlit_option_menu import option_menu
import chromadb
import pandas as pd
import os

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

option_page_map = {"Home": "./main.py", "Upload": "pages/File_Upload.py", "Settings": "pages/Settings.py"}

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

st.markdown("### ChromaDB Data Viewer")

if not os.path.isdir(CHROMA_DIR):
    st.warning(f"No chroma db directory found at {CHROMA_DIR}", icon="❗")
else:
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    st.header("Collections")

    for collection in client.list_collections():
        data = collection.get()
        metadata = data["metadatas"]
        documents = data["documents"]

        df = pd.DataFrame.from_dict({
            "Documents": documents, "Metadata": metadata
        })
        with st.expander(f"### **{collection.name}**"):
            st.dataframe(df)