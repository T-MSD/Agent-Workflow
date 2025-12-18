from langgraph.graph import END, StateGraph

from .agents.analyst import Analyst
from .agents.architect import Architect
from .agents.supervisor import Supervisor
from .state import AgentState


def build_team_graph(llm):
    # Initialize Objects
    analyst = Analyst(llm)
    architect = Architect(llm)
    supervisor = Supervisor(llm, ["Analyst", "Architect"])

    workflow = StateGraph(AgentState)

    # Define Nodes using the object methods
    workflow.add_node("Analyst", analyst.run)
    workflow.add_node("Architect", architect.run)
    workflow.add_node("Supervisor", supervisor.invoke)

    # Define the "Return to Leader" pattern
    workflow.add_edge("Analyst", "Supervisor")
    workflow.add_edge("Architect", "Supervisor")

    # The Supervisor Logic (Conditional)
    workflow.add_conditional_edges(
        "Supervisor",
        lambda x: x["next"],
        {"Analyst": "Analyst", "Architect": "Architect", "FINISH": END},
    )

    return workflow.compile()
