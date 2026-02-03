import json
from typing import Optional
from app.models.quiz_models import GeneratedQuiz

from llm_core.generation_service import generate_daily_lesson, generate_quiz_from_lesson
# adjust the import path to wherever your functions live


def parse_lesson_response(text: str) -> dict:
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON returned by LLM: {e}")


def get_lesson(year_group: str, subject: str, topic_idea: str) -> str:
    res = generate_daily_lesson(
        year_group=year_group,
        subject=subject,
        topic_idea=topic_idea,
    )
    return parse_lesson_response(res)


def get_quiz(lesson_text: str, year_group: str) -> Optional[GeneratedQuiz]:
    return generate_quiz_from_lesson(
        lesson_text=lesson_text,
        year_group=year_group,
    )
