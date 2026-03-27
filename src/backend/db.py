import sqlite3
import uuid
import os
from datetime import datetime, timezone

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

DB_PATH = os.getenv("SQLITE_DB_PATH", os.path.join(os.path.dirname(__file__), "conversations.db"))

MESSAGE_TYPE_MAP = {
    "HumanMessage": HumanMessage,
    "AIMessage": AIMessage,
    "SystemMessage": SystemMessage,
}


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db() -> None:
    conn = _get_connection()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS conversations (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS messages (
                id TEXT PRIMARY KEY,
                conversation_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                message_type TEXT NOT NULL,
                created_at TEXT NOT NULL,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            );
        """)
        conn.commit()
    finally:
        conn.close()


def create_conversation(title: str) -> dict:
    conn = _get_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        conversation_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO conversations (id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
            (conversation_id, title, now, now),
        )
        conn.commit()
        return {"id": conversation_id, "title": title, "created_at": now, "updated_at": now}
    finally:
        conn.close()


def list_conversations() -> list[dict]:
    conn = _get_connection()
    try:
        rows = conn.execute("SELECT * FROM conversations ORDER BY updated_at DESC").fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def get_conversation(conversation_id: str) -> dict | None:
    conn = _get_connection()
    try:
        row = conn.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def delete_conversation(conversation_id: str) -> bool:
    conn = _get_connection()
    try:
        cursor = conn.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def update_conversation_title(conversation_id: str, title: str) -> dict | None:
    conn = _get_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        conn.execute(
            "UPDATE conversations SET title = ?, updated_at = ? WHERE id = ?",
            (title, now, conversation_id),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM conversations WHERE id = ?", (conversation_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def add_message(conversation_id: str, role: str, content: str, message_type: str) -> dict:
    conn = _get_connection()
    try:
        now = datetime.now(timezone.utc).isoformat()
        message_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO messages (id, conversation_id, role, content, message_type, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (message_id, conversation_id, role, content, message_type, now),
        )
        conn.execute(
            "UPDATE conversations SET updated_at = ? WHERE id = ?",
            (now, conversation_id),
        )
        conn.commit()
        return {
            "id": message_id,
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "message_type": message_type,
            "created_at": now,
        }
    finally:
        conn.close()


def get_messages(conversation_id: str) -> list[dict]:
    conn = _get_connection()
    try:
        rows = conn.execute(
            "SELECT * FROM messages WHERE conversation_id = ? ORDER BY created_at ASC",
            (conversation_id,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


def messages_to_langchain(db_messages: list[dict]) -> list:
    langchain_messages = []
    for msg in db_messages:
        msg_class = MESSAGE_TYPE_MAP.get(msg["message_type"])
        if msg_class:
            langchain_messages.append(msg_class(content=msg["content"]))
    return langchain_messages
