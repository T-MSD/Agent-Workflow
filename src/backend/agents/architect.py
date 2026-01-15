from state import AgentState
from .agent import BaseAgent

SYSTEM_PROMPT = """You are an expert enterprise architect.
You provide recommendations on enterprise architecture, reason about the application landscape, and answer enterprise-related questions.
"""


class Architect(BaseAgent):
    def __init__(self, model):
        super().__init__(
            model=model,
            name="Architect",
            system_prompt=SYSTEM_PROMPT,
            tools=[],
        )

    def run(self, state: AgentState):
        """
        Run the Architect and set a boolean flag in state to indicate
        the Architect has been executed once. This prevents additional
        Architect handoffs.
        """
        # Execute the base agent run to get the model response
        update = super().run(state)

        # Set a boolean flag instead of a numeric counter
        update["architect_ran"] = True

        return update
