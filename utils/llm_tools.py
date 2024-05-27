from langchain.agents import Tool
from langchain_community.utilities import WikipediaAPIWrapper
from utils.openai_llm import gpt3_llm
from uuid import uuid4


# from langchain_core.pydantic_v1 import BaseModel, Field, validator

# class Joke(BaseModel):
#     """Joke to tell user."""
#     setup: str = Field(description="question to set up a joke")
#     punchline: str = Field(description="answer to resolve the joke")

# llm_with_tool = gpt3_llm #.bind_tools([Joke])


def get_unique_identifier(*args):
    random_uuid = uuid4().hex
    print(f"Generated uuid(4) - {random_uuid}")
    return random_uuid


def respond_to_greeting(*args):
    return gpt3_llm.invoke(args).content

def get_wikipedia_data(*args):
    return WikipediaAPIWrapper().run(args[0])

greeting_tool = Tool(
    name="Respond to greetings and small talk",
    description="Used for responding to greeting or small talk",
    func=respond_to_greeting,
)

greeting_tool.return_direct = True


tools = [
    Tool(
        name="Create unique id (uuid)",
        func=get_unique_identifier,
        description="Useful for when you need to get a random uuid4 string. Use only when explicity requested",
    ),
    Tool(
        name="Get data from Wikipedia",
        func=get_wikipedia_data,
        description="Useful when user looks things up. Use when answer needs to be factual, detailed and peer-reviewed. Make sure any answer generated is summarised for ease of consumption"
    ),
    greeting_tool,
]


# expanded_tools = [
#     Tool(
#         name="Search",
#         func=search.run,
#         description="useful for when you need to answer questions about current events",
#     ),
#     Tool(
#         name="Knowledge Base",
#         func=podcast_retriever.run,
#         description="Useful for general questions about how to do things and for details on interesting topics. Input should be a fully formed question.",
#     ),
# ]
