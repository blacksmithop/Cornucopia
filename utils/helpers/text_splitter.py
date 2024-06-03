from langchain_experimental.text_splitter import SemanticChunker
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.embeddings import instruct_embeddings

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=20,
    length_function=len,
    is_separator_regex=False,
)


def get_relevant_chunks(text: str):
    docs = text_splitter.create_documents([text])
    text_chunks = [doc.page_content for doc in docs[:2]]
    return " ".join(text_chunks)


semantic_splitter = SemanticChunker(instruct_embeddings)
