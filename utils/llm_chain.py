from langchain.chains.llm import LLMChain
from utils.openai_llm import gpt3_llm
from utils.custom_prompt import prompt
from utils.custom_parsers import output_parser
from langchain.agents import AgentExecutor, LLMSingleActionAgent
from utils.llm_tools import tools
from langchain.memory import ConversationBufferWindowMemory


# LLM chain consisting of the LLM and a prompt
llm_chain = LLMChain(llm=gpt3_llm, prompt=prompt)

# Using tools, the LLM chain and output_parser to make an agent
tool_names = [tool.name for tool in tools]

agent = LLMSingleActionAgent(
    llm_chain=llm_chain,
    output_parser=output_parser,
    # We use "Observation" as our stop sequence so it will stop when it receives Tool output
    # If you change your prompt template you'll need to adjust this as well
    stop=["\nObservation:"],
    allowed_tools=tool_names,
)

memory = ConversationBufferWindowMemory(k=2)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent, tools=tools, verbose=True, memory=memory
)