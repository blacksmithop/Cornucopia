from typing import List

from langchain_community.document_transformers.embeddings_redundant_filter import \
    _DocumentWithState as Document

from utils.helpers.text_splitter import get_relevant_chunks


def parse_retriever_content(response: List[Document]):
    response_markdown = ""

    for index, item in enumerate(response, start=1):
        page_content = item.page_content
        relevant_content = get_relevant_chunks(text=page_content)

        if item.metadata and item.metadata != {}:
            metadata = item.metadata
            title = metadata["title"]
            source = metadata["source"]

            content = f"{relevant_content}\n[[{index}]({source})]\n\n"
        else:
            content = f"{relevant_content}\n\n"

        response_markdown += content

    return response_markdown
