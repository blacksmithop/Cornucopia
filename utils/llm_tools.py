from langchain.agents import (
    Tool,
    AgentExecutor,
    LLMSingleActionAgent,
    AgentOutputParser,
)
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


tools = [
    Tool(
        name="Get unique identifier",
        func=get_unique_identifier,
        description="useful for when you need to get a random uuid4 string",
    )
]
