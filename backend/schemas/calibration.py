from pydantic import BaseModel
from typing import Literal

class ResonatorAnalysis(BaseModel):
    has_clear_resonance: Literal["yes", "no", "uncertain"]
    confidence: float
    explanation: str
    detected_issues: list[str]
    suggested_next_steps: list[str]
