
from state.state_class import InvestigationState
import sqlite3
import json
# from state.state_class import InvestigationState, VerificationReport

DB_NAME = "sentinels.db"


def get_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn




def insert_state(state: InvestigationState):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO messages (
            message_id,
            message_body,
            agent_alpha_output,
            agent_beta_output,
            db_action
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        state.message_id,
        state.message_body,
        state.agent_alpha_output.model_dump_json()
            if state.agent_alpha_output else None,

        state.agent_beta_output.model_dump_json()
            if state.agent_beta_output else None,

        state.db_action
    ))

    conn.commit()
    conn.close()