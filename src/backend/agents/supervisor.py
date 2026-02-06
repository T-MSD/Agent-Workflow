from typing import Literal

from langchain_core.messages import SystemMessage
from pydantic import BaseModel, Field

from helpers.state import AgentState


# 1. Define the routing schema
# This Pydantic model forces the LLM to choose one of your team members or finish.
class Router(BaseModel):
    """Decide which worker to route to next. If the task is fully complete, route to FINISH."""

    next: Literal["Analyst", "Architect", "OUT_OF_SCOPE", "FINISH"] = Field(
        description="The name of the next agent to act, OUT_OF_SCOPE if the question is not Enterprise Architecture or application inventory related, and FINISH if the user's request is satisfied."
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
            "You are the Enterprise Architecture Team Leader (Supervisor) managing a Data Analyst and an Enterprise Architect.\n"
            "Your job is to route work to the right agent and finish when the user's request is satisfied.\n\n"
            "ROUTING RULES:\n"
            "1. If the user asks for specific data, evidence, or application inventory details, route to 'Analyst'.\n"
            "2. If the user asks for architecture strategy, target-state design, standards, or governance guidance, route to 'Architect'.\n"
            "3. If the user wants both data and recommendations, call 'Analyst' first, then 'Architect'.\n"
            "4. If the last agent response fully answers the request, return 'FINISH'.\n"
            "5. If the request is not about enterprise architecture or application inventory, return 'OUT_OF_SCOPE'.\n"
            "6. You may call agents multiple times, but only call 'Architect' once per request.\n\n"
            "DECISION CRITERIA:\n"
            "- Prefer 'Analyst' when the question depends on missing facts or data.\n"
            "- Prefer 'Architect' when the question is primarily interpretive, strategic, or design-oriented.\n"
            "- If uncertain, choose the smallest next step that reduces ambiguity (usually 'Analyst')."
        )

    def scope_message(self, state: AgentState):
        """
        Adds a message to the state indicating the request is out of scope
        """

        return {
            "messages": [
                SystemMessage(
                    content="I am sorry, but your request is outside of my scope. I can only answer questions about Enterprise Architecture and application inventory."
                )
            ]
        }

    def invoke(self, state: AgentState):
        """
        The entry point for the Supervisor node in LangGraph.
        """
        if state.get("architect_ran", False):
            pass

        # Full message history + system prompt
        messages = [SystemMessage(content=self.system_prompt)] + list(state["messages"])

        # Next step prediction
        prediction = self.model.invoke(messages)

        if prediction.next == "Architect" and state.get("architect_ran", False):
            return {
                "next": "FINISH",
                "messages": [
                    SystemMessage(
                        content="Architect already executed once. Skipping additional Architect passes and finishing workflow."
                    )
                ],
            }

        return {"next": prediction.next}
