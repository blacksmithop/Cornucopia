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


rag_prompt = PromptTemplate.from_template(
    """
You are an assistant for question-answering tasks. Use the following pieces of retrieved context to answer the question. If you don't know the answer, just say that you don't know. Use three sentences maximum and keep the answer concise.

Question: {question} 

Context: {context} 

Answer:
"""
)

rag_chain = rag_prompt | gpt3_llm | StrOutputParser()
