
import sqlite3
import json

DB_NAME = "sentinels.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def get_all_message_bodies():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT message_body
    FROM messages
    WHERE db_action NOT IN ('DISCARD', 'FLAG_REVIEW')
       OR db_action IS NULL
""")

    rows = cursor.fetchall()

    conn.close()

    return [row["message_body"] for row in rows]