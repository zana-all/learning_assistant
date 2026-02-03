from typing import Optional
from pydantic import BaseModel, Field


class LessonRequest(BaseModel):
    year_group: int = Field(..., ge=1, le=13)
    subject: str = Field(..., examples=["Maths"])
    topic_idea: Optional[str] = ""


class LessonResponse(BaseModel):
    title: str
    lesson_text: str
    visual_prompt: str
    year_group: int
    subject: str


class ImageRequest(BaseModel):
    prompt: str


class ImageResponse(BaseModel):
    image_base64: Optional[str] = None
