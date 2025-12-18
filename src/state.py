import operator
from typing import Annotated, Sequence, TypedDict

from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    """
    The shared state (memory) of the LangGraph workflow.
    """

    # The 'messages' key is the history of the entire conversation.
    # Annotated with 'add_messages' (or operator.add) tells LangGraph
    # to APPEND new messages to the list rather than overwriting them.
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # This field is used by the Supervisor to track which agent is active.
    # It acts as the routing instruction for the next step.
    next: str

    # (Optional) High-level context fields if you want to keep them
    # separate from the message history for easier access by the Architect.
    extracted_data: str
    final_recommendation: str
