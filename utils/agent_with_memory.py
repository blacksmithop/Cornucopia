from langchain.agents import AgentExecutor, create_react_agent
from langchain_core.runnables.history import RunnableWithMessageHistory

from utils.llm_core import gpt3_llm as llm
from utils.memory import get_session_history as memory
from utils.prompts import react_prompt as prompt
from utils.tools import tool_list as tools

agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent, tools=tools, handle_parsing_errors=True, max_iterations=6, verbose=True, return_intermediate_steps=True
)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)
