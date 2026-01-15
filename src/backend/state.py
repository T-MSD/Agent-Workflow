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

    next: str

    extracted_data: str
    final_recommendation: str

    architect_ran: bool
