import uvicorn
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from langchain_groq import ChatGroq
from graph_builder import build_team_graph

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
ORIGIN = os.getenv("ORIGIN")

app = FastAPI(
    title="Multi-Agent Team API",
    description="An API to interact with a team of autonomous agents.",
    version="1.0.0",
)


origins = [
    ORIGIN
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class InvokeRequest(BaseModel):
    """Request model for invoking the agent team."""
    prompt: str


class InvokeResponse(BaseModel):
    """Response model for the agent team's output."""
    output: str


@app.post("/invoke", response_model=InvokeResponse)
def invoke_agent_team(request: InvokeRequest):
    """
    Receives a prompt, runs it through the agent team, and returns the final result.
    """
    
    supervisor_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    worker_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    
    agent_graph = build_team_graph(supervisor_llm, worker_llm)
    
    initial_state = {
        "messages": [HumanMessage(content=request.prompt)],
        "next": "Supervisor",
    }
    
    final_output = ""
    for output in agent_graph.stream(initial_state, config={"recursion_limit": 20}):
        for node_name, state_update in output.items():
            if "messages" in state_update:
                last_msg = state_update["messages"][-1]
                if last_msg.content:
                    if state_update.get("next") is None:
                        final_output = last_msg.content
    return InvokeResponse(output=final_output)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)