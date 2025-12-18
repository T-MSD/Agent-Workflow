from agent import BaseAgent

from ..state import AgentState


class Architect(BaseAgent):
    def __init__(self, model):
        super().__init__(
            model=model,
            name="Architect",
            system_prompt="Meter prompt !!!!!!!!!!!",
            tools=None,
        )

    def run(self, state: AgentState):
        return super().run(state)
