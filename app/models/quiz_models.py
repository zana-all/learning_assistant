from pydantic import BaseModel, Field
from typing import List, Literal


class QuizRequest(BaseModel):
    lesson_text: str
    year_group: str = Field(..., examples=["Year 8"])


AnswerKey = Literal["A", "B", "C", "D"]


class QuizQuestion(BaseModel):
    """Schema for a single multiple-choice quiz question."""

    # Field descriptions help the LLM understand what to generate
    question: str = Field(description="The multiple-choice question text.")
    options: List[str] = Field(
        description="A list of 4 possible answer choices (A, B, C, D)."
    )
    correct_key: AnswerKey = Field(
        description="The key representing the correct answer (must be 'A', 'B', 'C', or 'D')."
    )
    explanation: str = Field(
        description="A concise, educational explanation for why the answer is correct."
    )


class GeneratedQuiz(BaseModel):
    """The complete quiz, containing a list of questions."""

    quiz_questions: List[QuizQuestion] = Field(
        description="A list of 3 quiz questions based ONLY on the provided lesson text."
    )
