from langchain_core.tools import tool

from ..state import AgentState
from .agent import BaseAgent

SYSTEM_PROMPT = """You are an expert data analyst.
Your role is to access a database, retrieve data, and perform analysis.
You must generate the correct SQL query based on the user's request to fetch the necessary information.
"""


class Analyst(BaseAgent):
    def __init__(self, model):
        super().__init__(
            model=model,
            name="Analyst",
            system_prompt=SYSTEM_PROMPT,
            tools=[database_access_tool, generate_query],
        )

    def run(self, state: AgentState):
        return super().run(state)


@tool
def generate_query(prompt):
    """
    Generate a query based on the received prompt
    """

    pass


@tool
def database_access_tool(query):
    """
    Query the database to retrieve data regarding the application inventory.

    Args:
        query: Query to run in the database.
    """

    pass
