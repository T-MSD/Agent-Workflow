from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from .agents.analyst import Analyst, database_access_tool, generate_query
from .agents.architect import Architect
from .state import AgentState
from .supervisor import Supervisor


# Helper function to check if the last message contains a tool call
def should_continue(state: AgentState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "action"
    return "Supervisor"


def build_team_graph(llm):
    analyst = Analyst(llm)
    architect = Architect(llm)
    supervisor = Supervisor(llm)

    tools = [database_access_tool, generate_query]
    tool_node = ToolNode(tools)

    workflow = StateGraph(AgentState)

    workflow.add_node("Analyst", analyst.run)
    workflow.add_node("Architect", architect.run)
    workflow.add_node("Supervisor", supervisor.invoke)
    workflow.add_node("OUT_OF_SCOPE", supervisor.scope_message)
    workflow.add_node("action", tool_node)

    workflow.set_entry_point("Supervisor")

    workflow.add_edge("Architect", "Supervisor")
    workflow.add_edge("OUT_OF_SCOPE", END)

    workflow.add_conditional_edges(
        "Analyst", should_continue, {"action": "action", "Supervisor": "Supervisor"}
    )

    workflow.add_edge("action", "Analyst")

    workflow.add_conditional_edges(
        "Supervisor",
        lambda state: state["next"],
        {
            "Analyst": "Analyst",
            "Architect": "Architect",
            "OUT_OF_SCOPE": "OUT_OF_SCOPE",
            "FINISH": END,
        },
    )

    return workflow.compile()
