from groq import Groq
from pydantic import BaseModel
from typing import Optional, Literal
import os

from state.state_class import AgentBetaReport


class AgentBeta:

    def __init__(self):
        self.client = Groq(
            api_key=os.environ.get("GROQ_API_KEY")
        )

    def run(self, incoming_claim: str, existing_messages: list[str]):

        context = "\n".join(existing_messages)

        completion = self.client.chat.completions.create(
            model="openai/gpt-oss-120b",
            temperature=0.1,
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": f"""
You are Agent Beta.
Return ONLY valid JSON.

Compare the incoming claim with existing accepted claims.

Rules:
1. Same meaning as an existing accepted claim → SEMANTIC_DUPLICATE
2. Opposite/conflicting meaning with an accepted claim → CONTRADICTION
3. No relevant match found → NO_MATCH

Output JSON must follow this schema:
{AgentBetaReport.model_json_schema()}
"""
                },
                {
                    "role": "user",
                    "content": f"""
Incoming claim:
{incoming_claim}

Existing claims:
{context}
"""
                }
            ]
        )

        return AgentBetaReport.model_validate_json(
            completion.choices[0].message.content
        )