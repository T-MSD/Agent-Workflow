from typing import Literal

from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

from .state import AgentState


# 1. Define the routing schema
# This Pydantic model forces the LLM to choose one of your team members or finish.
class Router(BaseModel):
    """Decide which worker to route to next. If the task is fully complete, route to FINISH."""

    next: Literal["Analyst", "Architect", "FINISH"] = Field(
        description="The name of the next agent to act, or FINISH if the user's request is satisfied."
    )


class Supervisor:
    """
    The Orchestrator (Leader) of the team.
    It doesn't perform tasks but manages the flow between workers.
    """

    def __init__(self, model):
        # We bind the 'Router' schema to the LLM.
        # This makes the model return a Router object instead of plain text.
        self.model = model.with_structured_output(Router)

        self.team_members = ["Analyst", "Architect"]
        self.system_prompt = (
            "You are the Team Leader (Supervisor) managing a Data Analyst and an Enterprise Architect.\n"
            "Your job is to coordinate their efforts to answer the user's prompt.\n\n"
            "GUIDELINES:\n"
            "1. If specific data is needed (e.g., application data such as \
            applications on cloud or obsolete applications), call the 'Analyst'.\n"
            "2. Once data is available, if strategic advice or EA questions remain, call the 'Architect'.\n"
            "3. For all other questions regarding Enterprise Architecture, call \
            the 'Architect' immediately.\n"
            "4. If the chat history contains a complete answer that satisfies the user, respond with 'FINISH'.\n"
            "5. You can call agents multiple times if refinement or more data is needed.\n"
            "6. Only answer questions related to the application landscape or Enterprise Architecture."
        )

    def invoke(self, state: AgentState):
        """
        The entry point for the Supervisor node in LangGraph.
        """
        # We pass the full message history so the Supervisor knows what has happened so far.
        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]

        # The LLM chooses the next step based on the history
        prediction = self.model.invoke(messages)

        # We update the 'next' key in our AgentState
        # This string will be used by the conditional edges to route the graph.
        return {"next": prediction.next}
