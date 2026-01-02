from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from .agents.analyst import Analyst, database_access_tool
from .agents.architect import Architect
from .state import AgentState
from .supervisor import Supervisor


def build_team_graph(llm):
    # Initialize Objects
    analyst = Analyst(llm)
    architect = Architect(llm)
    supervisor = Supervisor(llm)

    tools = [database_access_tool]

    workflow = StateGraph(AgentState)

    tool_node = ToolNode(tools)

    # Define Nodes using the object methods
    workflow.add_node("Analyst", analyst.run)
    workflow.add_node("Architect", architect.run)
    workflow.add_node("Supervisor", supervisor.invoke)
    workflow.add_node("action", tool_node)

    # Define the "Return to Leader" pattern
    workflow.add_edge("Analyst", "Supervisor")
    workflow.add_edge("Architect", "Supervisor")

    # The Supervisor Logic (Conditional)
    workflow.add_conditional_edges(
        "Supervisor",
        lambda state: state["next"],
        {"Analyst": "Analyst", "Architect": "Architect", "FINISH": END},
    )

    return workflow.compile()
