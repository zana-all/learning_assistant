from pydantic import BaseModel, Field
from typing import Optional


class ScoreCreate(BaseModel):
    subject: str = Field(min_length=1)
    year_group: int = Field(..., ge=1, le=13)
    topic: Optional[str] = None
    score: int = Field(ge=0)
    total_questions: int = Field(ge=1)


class ScoreCreated(BaseModel):
    id: int


class SubjectSummary(BaseModel):
    subject: str
    attempts: int
    avg_accuracy: float
    best_accuracy: float
    worst_accuracy: float


class ScoreSummary(BaseModel):
    total_attempts: int
    overall_avg_accuracy: float
    by_subject: list[SubjectSummary]
