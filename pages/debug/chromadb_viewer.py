import chromadb
import pandas as pd 
import streamlit as st


def view_collections(dir):
    st.markdown("### DB Path: %s" % dir)

    client = chromadb.PersistentClient(path=dir)

    # This might take a while in the first execution if Chroma wants to download
    # the embedding transformer
    print(client.list_collections())

    st.header("Collections")

    for collection in client.list_collections():
        data = collection.get()

        ids = data['ids']
        embeddings = data["embeddings"]
        metadata = data["metadatas"]
        documents = data["documents"]

        df = pd.DataFrame.from_dict(data)
        st.markdown("### Collection: **%s**" % collection.name)
        st.dataframe(df)

db_path = "./utils/chroma_db"
print(f"Opening database: {db_path}")
view_collections(db_path)

