import sqlite3
import json

DB_NAME = "sentinels.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def recreate_table():
    conn = get_connection()
    cursor = conn.cursor()

    # delete old table if it exists
    cursor.execute("DROP TABLE IF EXISTS messages")

    # create fresh table
    cursor.execute("""
CREATE TABLE messages (
    message_id TEXT PRIMARY KEY,
    message_body TEXT NOT NULL,
    agent_alpha_output TEXT,
    agent_beta_output TEXT,
    db_action TEXT
)
    """)

    conn.commit()
    conn.close()


recreate_table()