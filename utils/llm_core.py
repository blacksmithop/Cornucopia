from os import getenv

from dotenv import load_dotenv
from langchain_community.llms.ollama import Ollama
from langchain_openai import AzureChatOpenAI

load_dotenv()

try:
    # OpenAI
    chat_llm = AzureChatOpenAI(
        azure_endpoint=getenv("AZURE_OPENAI_GPT3_ENDPOINT"),
        deployment_name=getenv("GPT3_DEPLOYMENT_NAME"),
        api_key=getenv("GPT3_OPENAI_API_KEY"),
        api_version=getenv("OPENAI_API_VERSION"),
        temperature=0.0,
        max_tokens=1000,
    )

    vision_llm = AzureChatOpenAI(
        azure_endpoint=getenv("AZURE_OPENAI_GPT4o_ENDPOINT"),
        deployment_name=getenv("GPT4o_DEPLOYMENT_NAME"),
        api_key=getenv("GPT4o_OPENAI_API_KEY"),
        api_version=getenv("OPENAI_API_VERSION"),
    )
except KeyError:
    # Use Ollama
    chat_llm = Ollama(model=getenv("OLLAMA_MODEL"), base_url=getenv("OLLAMA_HOST"))
    vision_llm = chat_llm

# Make params configurable

if __name__ == "__main__":
    pass
    # print(embeddings.embed_query("hi")[:5])
    # print(gpt3_llm.invoke("Tell me a joke").content)
