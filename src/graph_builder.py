from langgraph.graph import END, StateGraph
from langgraph.prebuilt import ToolNode

from .agents.analyst import Analyst
from .agents.architect import Architect
from .state import AgentState
from .supervisor import Supervisor


# Helper function to check if the last message contains a tool call
def should_continue(state: AgentState):
    """
    Helper function to check if the last message contains a tool call.
    """
    last_message = state["messages"][-1]

    # The last message has tool calls, so execute the tool.
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "action"
    # Otherwise, return to the supervisor to decide the next step.
    return "Supervisor"


def build_team_graph(supervisor_llm, worker_llm):
    analyst = Analyst(worker_llm)
    architect = Architect(worker_llm)
    supervisor = Supervisor(supervisor_llm)

    tool_node = ToolNode(analyst.tools)

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

    # After a tool is executed, route back to the Supervisor to decide the next step
    workflow.add_edge("action", "Supervisor")

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
