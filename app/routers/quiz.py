from fastapi import APIRouter, HTTPException
from services.lesson_service import get_quiz
from app.models.quiz_models import QuizRequest
from app.models.quiz_models import GeneratedQuiz

router = APIRouter(prefix="/v1", tags=["Quiz"])


@router.post("/quiz", response_model=GeneratedQuiz)
def quiz(req: QuizRequest):
    quiz_obj = get_quiz(
        lesson_text=req.lesson_text,
        year_group=req.year_group,
    )
    if quiz_obj is None:
        raise HTTPException(status_code=502, detail="Quiz generation failed.")
    return quiz_obj
