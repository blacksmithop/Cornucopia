import os

import chromadb
from langchain_chroma import Chroma
from langchain_community.retrievers.wikipedia import WikipediaRetriever

from utils.embeddings import instruct_embeddings

# wikipedia
wiki_retriever = WikipediaRetriever()

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ABS_PATH, "chroma_db")


client_settings = chromadb.config.Settings(
    is_persistent=True,
    persist_directory=DB_DIR,
    anonymized_telemetry=False,
)

# chromadb
upload_docs_db = Chroma(
    collection_name="project_store_all",
    persist_directory=DB_DIR,
    client_settings=client_settings,
    embedding_function=instruct_embeddings,
)

custom_retriever = upload_docs_db.as_retriever(
    search_type="similarity",
    search_kwargs={
        "k": 5,
    },  # "include_metadata": True
)
