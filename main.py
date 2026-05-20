from agent_alpha import AgentAlpha
from agent_beta import AgentBeta
from state.state_class import InvestigationState
from database.insert_state import insert_state
from database.get_message_bodies import get_all_message_bodies


agent_alpha = AgentAlpha()
agent_beta = AgentBeta()


def process_claim(claim: str):

    state = InvestigationState(
        message_body=claim
    )


    alpha_output = agent_alpha.run(user_query=state.message_body)
    state.agent_alpha_output = alpha_output

    if alpha_output and alpha_output.verdict == "FALSE":
        state.db_action = "DISCARD"
        insert_state(state)
        return state


    existing_messages = get_all_message_bodies()

    beta_output = agent_beta.run(
        incoming_claim=state.message_body,
        existing_messages=existing_messages
    )

    state.agent_beta_output = beta_output

    if beta_output.verdict == "SEMANTIC_DUPLICATE":
        state.db_action = "DISCARD"

    elif beta_output.verdict == "CONTRADICTION":
        state.db_action = "FLAG_REVIEW"

    elif beta_output.verdict == "NO_MATCH":

        if alpha_output.verdict == "TRUE":
            state.db_action = "INSERT"

        elif alpha_output.verdict in ["PARTIALLY_TRUE", "UNVERIFIABLE"]:
            state.db_action = "FLAG_REVIEW"


    insert_state(state)

    return state


if __name__ == "__main__":
    claim = "is modi the prime minister of india"

    result = process_claim(claim)

    print(result.model_dump())