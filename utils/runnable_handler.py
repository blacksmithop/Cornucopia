from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import Runnable
from utils.llm_tools import llm_with_tool
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from utils.custom_parsers import joke_parser, combined_parser


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are helpful assistant",
        ),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ]
)
runnable: Runnable = prompt | llm_with_tool | StrOutputParser() #combined_parser
