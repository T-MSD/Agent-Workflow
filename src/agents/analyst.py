import os

import oracledb
from dotenv import load_dotenv
from langchain_core.tools import tool

from ..state import AgentState
from .agent import BaseAgent

load_dotenv()
SYSTEM_PROMPT = """You are an expert data analyst.
Your role is to access a database, retrieve data, and perform analysis.
You must generate the correct SQL query based on the user's request to fetch the necessary information.
"""


class Analyst(BaseAgent):
    def __init__(self, model):
        super().__init__(
            model=model,
            name="Analyst",
            system_prompt=SYSTEM_PROMPT,
            tools=[get_schema],
        )

    def run(self, state: AgentState):
        return super().run(state)


def _get_connection():
    """Create and return an Oracle DB connection using environment variables."""
    return oracledb.connect(
        user=os.getenv("ORACLE_DB_USER"),
        password=os.getenv("ORACLE_DB_PASSWORD"),
        dsn=os.getenv("ORACLE_DB_DSN"),
    )


@tool
def get_schema() -> str:
    """
    Used exclusively to get the table schema.
    """

    table = os.getenv("TABLE_NAME")
    if not table:
        raise RuntimeError("TABLE_NAME env var is required")

    owner = os.getenv("ORACLE_DB_USER")

    query = """
        SELECT
            column_name,
            data_type
        FROM
            all_tab_columns
        WHERE
            owner = :owner 
            AND table_name = :table_arg
        """

    try:
        with _get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, owner=owner, table_arg=table)
                results = cur.fetchall()
                return str(results)
    except oracledb.Error as exc:
        raise RuntimeError(f"Database error: {exc}") from exc
