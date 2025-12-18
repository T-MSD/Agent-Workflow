from typing import List, Optional

from langchain_core.messages import SystemMessage
from langchain_core.runnables import Runnable
from langchain_core.tools import BaseTool

from ..state import AgentState


class BaseAgent:
    """
    Parent class for all agents in the team.
    Handles LLM initialization, tool binding, and the execution logic.
    """

    def __init__(
        self,
        model: Runnable,
        name: str,
        system_prompt: str,
        tools: Optional[List[BaseTool]] = None,
    ):
        self.name = name
        self.system_prompt = system_prompt

        # If the agent has tools, bind them to the LLM
        if tools:
            self.model = model.bind_tools(tools)
        else:
            self.model = model

    def run(self, state: AgentState):
        """
        The standard execution method for LangGraph nodes.
        It takes the current state, runs the agent logic, and returns the update.
        """
        # 1. Prepare messages (System Message + Conversation History)
        messages = [SystemMessage(content=self.system_prompt)] + state["messages"]

        # 2. Invoke the model
        response = self.model.invoke(messages)

        # 3. Return the update for the 'messages' key in the state
        # We ensure the message is tagged with the agent's name for the Supervisor
        return {"messages": [response]}
