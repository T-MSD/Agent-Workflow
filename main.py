import getpass
import os

from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from src.graph_builder import build_team_graph

if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter your Google API Key: ")


def run_agent_team():
    """
    Initializes the Gemini model, constructs the LangGraph,
    and executes a multi-agent conversation.
    """

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", temperature=0, streaming=True
    )

    app = build_team_graph(llm)

    user_prompt = input("Type your question: ")

    while user_prompt != "/bye":
        state = {
            "messages": [HumanMessage(content=user_prompt)],
            "next": "Supervisor",  # Start with the Leader
        }

        print("\n" + "=" * 50)
        print("🚀 TEAM ORCHESTRATION STARTED")
        print("=" * 50 + "\n")

        for output in app.stream(state, config={"recursion_limit": 20}):
            for node_name, state_update in output.items():
                print(f"[{node_name.upper()}]:")

                if "messages" in state_update:
                    last_msg = state_update["messages"][-1]
                    if last_msg.content:
                        print(f"💬 {last_msg.content}")

                    if hasattr(last_msg, "tool_calls") and last_msg.tool_calls:
                        for tool_call in last_msg.tool_calls:
                            print(
                                f"🛠️  Calling Tool: {tool_call['name']} with args {tool_call['args']}"
                            )

                if "next" in state_update:
                    print(f"⏭️  Next Step: {state_update['next']}")

                print("-" * 30)

        print("\n" + "=" * 50)
        print("✅ WORKFLOW COMPLETE")
        print("=" * 50)

        user_prompt = input("Type your question: ")


if __name__ == "__main__":
    run_agent_team()
