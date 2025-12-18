from typing import Literal

from langchain_core.messages import SystemMessage
from langchain_core.pydantic_v1 import BaseModel, Field

from state import AgentState


# 1. Define the routing schema
# This forces the LLM to choose a valid next step.
class Router(BaseModel):
    """Decide which worker to route to next. If no more work is needed, route to FINISH."""

    next: Literal["Analyst", "Architect", "FINISH"] = Field(
        description="The name of the next agent to act, or FINISH if the goal is met."
    )


class Supervisor:
    def __init__(self, model):
        # We bind the structured output schema to the model
        self.model = model.with_structured_output(Router)
        self.members = ["Analyst", "Architect"]
        self.system_prompt = (
            "You are a team supervisor managing a conversation between {members}. "
            "Based on the user request, delegate tasks:\n"
            "- Use 'Analyst' if specific data needs to be retrieved from the database.\n"
            "- Use 'Architect' once data is available to provide EA recommendations.\n"
            "- Use 'FINISH' only when the final recommendation fully answers the user prompt."
        ).format(members=", ".join(self.members))

    def invoke(self, state: AgentState):
        """
        The node function that LangGraph calls.
        It looks at the messages and decides the 'next' agent.
        """
        # Prepare the messages for the LLM
        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]

        # Call the LLM with structured output
        response = self.model.invoke(messages)

        # Extract the decision
        goto = response.next

        # We return an update to the 'next' field in our AgentState
        return {"next": goto}

