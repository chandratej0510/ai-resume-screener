from pydantic import BaseModel
from typing import List

class MatchResult(BaseModel):
    filename: str
    score: float
    summary: str
    skills: List[str]

class MatchResponse(BaseModel):
    results: List[MatchResult]
