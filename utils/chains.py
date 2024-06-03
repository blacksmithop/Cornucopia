from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.llm_core import gpt3_llm

small_talk_prompt = PromptTemplate.from_template(
    """
You are a helpful chat assistant. Your task is to respond to small talk, greetings and such interactions.
User Input:
{input}

Response:
"""
)

small_talk_chain = small_talk_prompt | gpt3_llm | StrOutputParser()
