from langchain.output_parsers import CombiningOutputParser
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain.output_parsers.openai_tools import JsonOutputKeyToolsParser
from langchain.schema import AgentAction, AgentFinish
from typing import Union
import re
from langchain.agents import AgentOutputParser

# from utils.llm_tools import Joke

# # joke_parser = JsonOutputKeyToolsParser(key_name="Joke", first_tool_only=True)

# def joke_parser(joke: Joke):
#     return f"{joke.setup}\n{joke.punchline}"

# parsers = [
#     StrOutputParser(),
#     StrOutputParser(),
#     # JsonOutputParser(),
#     # joke_parser
# ]

# combined_parser = CombiningOutputParser(parsers=parsers)


class CustomOutputParser(AgentOutputParser):

    def parse(self, llm_output: str) -> Union[AgentAction, AgentFinish]:

        # Check if agent should finish
        if "Final Answer:" in llm_output:
            return AgentFinish(
                # Return values is generally always a dictionary with a single `output` key
                # It is not recommended to try anything else at the moment :)
                return_values={"output": llm_output.split("Final Answer:")[-1].strip()},
                log=llm_output,
            )

        # Parse out the action and action input
        regex = r"Action: (.*?)[\n]*Action Input:[\s]*(.*)"
        match = re.search(regex, llm_output, re.DOTALL)

        # If it can't parse the output it raises an error
        # You can add your own logic here to handle errors in a different way i.e. pass to a human, give a canned response
        if not match:
            raise ValueError(f"Could not parse LLM output: `{llm_output}`")
        action = match.group(1).strip()
        action_input = match.group(2)

        # Return the action and action input
        return AgentAction(
            tool=action, tool_input=action_input.strip(" ").strip('"'), log=llm_output
        )


output_parser = CustomOutputParser()
