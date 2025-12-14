import os

import oracledb
from dotenv import load_dotenv

load_dotenv()


def get_db_conn():
    """Create and return an Oracle DB connection using environment variables."""
    return oracledb.connect(
        user=os.getenv("ORACLE_DB_USER"),
        password=os.getenv("ORACLE_DB_PASSWORD"),
        dsn=os.getenv("ORACLE_DB_DSN"),
    )


def main():
    """Connect and print column names for a table.

    Uses env vars: TABLE_NAME, OWNER (optional).
    """
    table = os.getenv("TABLE_NAME")
    owner = os.getenv("OWNER")
    if not table:
        raise RuntimeError("TABLE_NAME env var is required")

    query = (
        "SELECT COLUMN_NAME FROM ALL_TAB_COLUMNS WHERE TABLE_NAME = :tbl "
        + ("AND OWNER = :own " if owner else "")
        + "ORDER BY COLUMN_ID"
    )

    try:
        with get_db_conn() as conn:
            with conn.cursor() as cur:
                params = {"tbl": table.upper()}
                if owner:
                    params["own"] = owner.upper()
                cur.execute(query, params)
                for (col_name,) in cur.fetchall():
                    print(col_name)
    except oracledb.Error as exc:
        raise RuntimeError(f"Database error: {exc}") from exc


if __name__ == "__main__":
    main()
