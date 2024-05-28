from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.agents import AgentExecutor, create_react_agent
from utils.llm_core import gpt3_llm as llm
from utils.tools import tool_list as tools
from utils.prompts import react_prompt as prompt
from utils.memory import get_session_history as memory


agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, handle_parsing_errors=True, verbose=True)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    memory,
    input_messages_key="input",
    history_messages_key="chat_history",
)