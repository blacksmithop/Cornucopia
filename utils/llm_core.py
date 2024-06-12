from os import getenv

from dotenv import load_dotenv
from langchain.embeddings import CacheBackedEmbeddings
from langchain.storage import LocalFileStore
from langchain_openai import (AzureChatOpenAI, AzureOpenAI,
                              AzureOpenAIEmbeddings)

load_dotenv()
store = LocalFileStore("./cache/")

# OpenAI Embeddings
underlying_embeddings = AzureOpenAIEmbeddings(
    azure_deployment=getenv("EMBEDDINGS_NAME")
)

embeddings = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings, store, namespace=underlying_embeddings.model
)

# OpenAI
gpt3_llm = AzureChatOpenAI(
    azure_endpoint=getenv("AZURE_OPENAI_GPT3_ENDPOINT"),
    deployment_name=getenv("GPT3_DEPLOYMENT_NAME"),
    api_key=getenv("GPT3_OPENAI_API_KEY"),
    api_version=getenv("OPENAI_API_VERSION"),
    temperature=0.0,
    max_tokens=1000,
)

gpt3_json_llm = AzureChatOpenAI(
    azure_endpoint=getenv("AZURE_OPENAI_GPT3_ENDPOINT"),
    deployment_name=getenv("GPT3_DEPLOYMENT_NAME"),
    api_key=getenv("GPT3_OPENAI_API_KEY"),
    api_version=getenv("OPENAI_API_VERSION"),
    temperature=0.0,
    max_tokens=1000,
    model_kwargs={"response_format": {"type": "json_object"}},
)

gpt4o = AzureChatOpenAI(
    azure_endpoint=getenv("AZURE_OPENAI_GPT4o_ENDPOINT"),
    deployment_name=getenv("GPT4o_DEPLOYMENT_NAME"),
    api_key=getenv("GPT4o_OPENAI_API_KEY"),
    api_version=getenv("OPENAI_API_VERSION"),
)

# Make params configurable

if __name__ == "__main__":
    # print(embeddings.embed_query("hi")[:5])
    print(gpt3_llm.invoke("Tell me a joke").content)
