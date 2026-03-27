import uvicorn
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_groq import ChatGroq
from helpers.graph_builder import build_team_graph
import db

load_dotenv()

HOST = os.getenv("HOST")
PORT = int(os.getenv("PORT"))
ORIGIN = os.getenv("ORIGIN")


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.init_db()
    yield


app = FastAPI(
    title="Multi-Agent Team API",
    description="An API to interact with a team of autonomous agents.",
    version="1.0.0",
    lifespan=lifespan,
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


# --- Pydantic Models ---

class InvokeRequest(BaseModel):
    prompt: str
    conversation_id: str | None = None


class InvokeResponse(BaseModel):
    response: str
    conversation_id: str


class ConversationResponse(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    created_at: str


class CreateConversationRequest(BaseModel):
    title: str | None = None


class UpdateConversationRequest(BaseModel):
    title: str


# --- Conversation Endpoints ---

@app.get("/conversations", response_model=list[ConversationResponse])
def list_conversations():
    return db.list_conversations()


@app.post("/conversations", response_model=ConversationResponse)
def create_conversation(request: CreateConversationRequest):
    title = request.title or "New Conversation"
    return db.create_conversation(title)


@app.get("/conversations/{conversation_id}/messages", response_model=list[MessageResponse])
def get_conversation_messages(conversation_id: str):
    conversation = db.get_conversation(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return db.get_messages(conversation_id)


@app.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: str):
    deleted = db.delete_conversation(conversation_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return {"ok": True}


@app.patch("/conversations/{conversation_id}", response_model=ConversationResponse)
def update_conversation(conversation_id: str, request: UpdateConversationRequest):
    result = db.update_conversation_title(conversation_id, request.title)
    if not result:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return result


# --- Agent Invoke Endpoint ---

@app.post("/invoke", response_model=InvokeResponse)
def invoke_agent_team(request: InvokeRequest):
    # 1. Resolve or create conversation
    if request.conversation_id:
        conversation = db.get_conversation(request.conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        title = request.prompt[:50].strip()
        if len(request.prompt) > 50:
            title += "..."
        conversation = db.create_conversation(title)

    conversation_id = conversation["id"]

    # 2. Save user message
    db.add_message(conversation_id, "human", request.prompt, "HumanMessage")

    # 3. Load full history and convert to LangChain messages
    db_messages = db.get_messages(conversation_id)
    langchain_messages = db.messages_to_langchain(db_messages)

    # 4. Build graph and run
    supervisor_llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
    worker_llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0)
    agent_graph = build_team_graph(supervisor_llm, worker_llm)

    initial_state = {
        "messages": langchain_messages,
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

    # 5. Save agent response
    db.add_message(conversation_id, "ai", final_output, "AIMessage")

    return InvokeResponse(response=final_output, conversation_id=conversation_id)


if __name__ == "__main__":
    uvicorn.run(app, host=HOST, port=PORT)
