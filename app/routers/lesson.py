from fastapi import APIRouter, HTTPException
from app.models.lesson_models import (
    LessonRequest,
    LessonResponse,
    ImageRequest,
    ImageResponse,
)
from services.lesson_service import get_lesson
from services.image_serivce import generate_image_from_prompt
from app.exceptions import ImageGenerationError

router = APIRouter(prefix="/v1", tags=["Lesson"])


@router.post("/lesson")
def lesson(req: LessonRequest) -> LessonResponse:
    lesson_response = get_lesson(
        year_group=req.year_group,
        subject=req.subject,
        topic_idea=req.topic_idea or "",
    )

    return LessonResponse(
        title=lesson_response.get("title"),
        lesson_text=lesson_response.get("lesson_text"),
        visual_prompt=lesson_response.get("visual_prompt"),
        year_group=req.year_group,
        subject=req.subject,
    )


@router.post("/image")
def create_image(req: ImageRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt is required.")
    try:
        img_b64 = generate_image_from_prompt(req.prompt.strip())
        return ImageResponse(image_base64=img_b64)
    except ImageGenerationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
