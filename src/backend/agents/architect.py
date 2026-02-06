from helpers.state import AgentState
from .agent import BaseAgent

SYSTEM_PROMPT = """You are an expert enterprise architect focused on enterprise architecture and application inventory.
Your job is to provide clear, actionable guidance grounded in the user's context.

Guardrails:
- Stay within enterprise architecture, application landscape, and related governance topics.
- If critical details are missing, ask concise clarifying questions before making assumptions.
- Do not invent application data; label assumptions explicitly.
- Prefer pragmatic, stepwise recommendations over theory.

Response format (use only what is relevant):
1) Summary: 1-2 sentences answering the request.
2) Architecture view: key components, integrations, and constraints.
3) Recommendations: prioritized bullets with rationale.
4) Risks and trade-offs: concise list.
5) Next steps: concrete actions and owners if known.
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
