from pydantic import BaseModel, Field
import uuid
from typing import Optional, Literal

class VerificationReport(BaseModel):

    verdict: Literal["TRUE", "FALSE", "PARTIALLY_TRUE", "UNVERIFIABLE"]
    confidence: float
    evidence: Optional[list[str]] = None
    sources: Optional[list[str]] = None
    contradicting_sources: Optional[list[str]] = None
    reasoning: str

class AgentBetaReport(BaseModel):
    verdict: Literal[
        "SEMANTIC_DUPLICATE",
        "CONTRADICTION",
        "NO_MATCH"
    ]
    matched_message: Optional[str] = None
    reasoning: str
    
class InvestigationState(BaseModel):

    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    message_body: str
    agent_alpha_output: Optional[VerificationReport] = None
    agent_beta_output: Optional[AgentBetaReport] = None
    db_action: Optional[
        Literal["INSERT", "DISCARD", "FLAG_REVIEW"]
    ] = None