from langchain_community.embeddings import HuggingFaceInstructEmbeddings


instruct_embeddings = HuggingFaceInstructEmbeddings(
query_instruction="Represent the query for retrieval: "
)
    
if __name__ == "__main__":

    text = "Document about Hunter X Hunter/"
    query_result = instruct_embeddings.embed_query(text)

    print(query_result)