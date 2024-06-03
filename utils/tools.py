from typing import Optional, Type

from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun,
                                         CallbackManagerForToolRun)
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

from utils.chains import small_talk_chain
from utils.helpers.knowledge_base import \
    compression_retriever_reordered as supplemented_knowledge_base
from utils.helpers.parsers import parse_retriever_content

search = DuckDuckGoSearchRun()
wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


class SearchInput(BaseModel):
    query: str = Field(
        description="Used for search query that ask for metadata, detailed information, references etc."
    )


class ConversationInput(BaseModel):
    query: str = Field(
        description="Used for handling small talk and similar conversation. Use when no suitable action is found. Ask for clarification if necessary"
    )


class SmallTalkTool(BaseTool):
    name = "small_talk"
    description = "Used for handling small talk and similar conversation. Use when no other suitable action is found."
    args_schema: Type[BaseModel] = SearchInput
    return_direct = True

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        response = small_talk_chain.invoke({"input": query})
        return response

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("custom_search does not support async")


class CustomKnowledgeBaseTool(BaseTool):
    name = "custom_knowledge_search"
    description = "Used for search query that ask for metadata, detailed information, references etc."
    args_schema: Type[BaseModel] = SearchInput
    return_direct = True

    def _run(
        self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        response = supplemented_knowledge_base.get_relevant_documents(query=query)
        parsed_response = parse_retriever_content(response=response)
        return parsed_response

    async def _arun(
        self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("small_talk does not support async")


tool_list = [search, wikipedia, CustomKnowledgeBaseTool(), SmallTalkTool()]

if __name__ == "__main__":
    print(wikipedia.run("HUNTER X HUNTER"))
    # print(search.run("Latest news about Hunter X Hunter"))
