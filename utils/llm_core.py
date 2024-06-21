from os import getenv

from dotenv import load_dotenv
from langchain_community.llms.ollama import Ollama
from langchain_openai import AzureChatOpenAI

load_dotenv()


# OpenAI
gpt3_llm = AzureChatOpenAI(
    azure_endpoint=getenv("AZURE_OPENAI_GPT3_ENDPOINT"),
    deployment_name=getenv("GPT3_DEPLOYMENT_NAME"),
    api_key=getenv("GPT3_OPENAI_API_KEY"),
    api_version=getenv("OPENAI_API_VERSION"),
    temperature=0.0,
    max_tokens=1000,
)

gpt4o = AzureChatOpenAI(
    azure_endpoint=getenv("AZURE_OPENAI_GPT4o_ENDPOINT"),
    deployment_name=getenv("GPT4o_DEPLOYMENT_NAME"),
    api_key=getenv("GPT4o_OPENAI_API_KEY"),
    api_version=getenv("OPENAI_API_VERSION"),
)

phi3_ollama = Ollama(model="phi3:latest", base_url=getenv("OLLAMA_HOST"))

gpt3_llm.with_fallbacks([phi3_ollama])  # Use Ollama as fallabck

# Make params configurable

if __name__ == "__main__":
    # print(embeddings.embed_query("hi")[:5])
    print(gpt3_llm.invoke("Tell me a joke").content)
