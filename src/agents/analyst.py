from agent import BaseAgent

from ..state import AgentState


class Analyst(BaseAgent):
    def __init__(self, model):
        super().__init__(
            model=model,
            name="Analyst",
            system_prompt="Meter prompt !!!!!!!!!!!",
            tools=[],  # TODO
        )

    def run(self, state: AgentState):
        return super().run(state)
