import os
import json
from typing import Optional
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError, ClientError
from app.exceptions import ImageGenerationError, ConfigurationError, LessonGenerationError
from llm_core.prompt_templates import (
    get_lesson_request_template,
    get_system_instructions,
    get_quiz_system_instruction,
)
from app.models.quiz_models import GeneratedQuiz
from testing.testing_data import TEST_LESSON_OUTPUT, TEST_QUIZ_OBJECT_PERFECT, TEST_IMAGE_BASE64

_client = None
load_dotenv()


def get_genai_client():
    global _client

    if _client is not None:
        return _client

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ConfigurationError(
            "GOOGLE_API_KEY is not set",
            status_code=503,
        )

    _client = genai.Client(api_key=api_key)
    return _client

LIVERUN = False


def generate_daily_lesson(
    year_group: int, subject: str, topic_idea: str = "", liverun: bool = LIVERUN
) -> str:
    """Generates the lesson content and a prompt for a visual aid."""

    if not liverun:
        print("returning test results")
        return TEST_LESSON_OUTPUT

    client = get_genai_client()


    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",  # Use the cost-effective model
            contents=[
                {
                    "role": "user",
                    "parts": [
                        {"text": get_system_instructions(year_group, subject)},
                        {
                            "text": get_lesson_request_template(
                                year_group, subject, topic_idea
                            )
                        },
                    ],
                }
            ],
        )
        return response.text
    except ClientError as e:
        raise LessonGenerationError(
            message=str(e),
            status_code=getattr(e, "status_code", 502),
        ) from e

    except Exception as e:
        raise LessonGenerationError(
            message="Unexpected error while generating lesson.",
            status_code=502,
        ) from e


def generate_quiz_from_lesson(
    lesson_text: str, year_group: int, liverun: bool = LIVERUN
) -> Optional[GeneratedQuiz]:
    """
    Generates a structured quiz based on the lesson text using Pydantic schema.

    :param lesson_text: The BODY of the lesson generated in Phase 1.
    :param year_group: The student's year group for difficulty tuning.
    :return: A Pydantic object containing the quiz, or None on failure.
    """

    if not liverun:
        print("returning test quiz")
        return TEST_QUIZ_OBJECT_PERFECT

    client = get_genai_client()

    # 1. System Instruction (Persona and Constraint)
    system_instruction = get_quiz_system_instruction(year_group)

    # 2. User Prompt (The Context)
    prompt_content = f"""
    Please generate 3 questions based on the following lesson text:
    
    --- LESSON TEXT ---
    {lesson_text}
    --- END LESSON TEXT ---
    
    Ensure the 'correct_answer' field exactly matches one of the 'options'.
    """

    try:
        # 3. API Call with Structured Output Configuration
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                {
                    "role": "user",
                    "parts": [{"text": system_instruction}, {"text": prompt_content}],
                }
            ],
            config=types.GenerateContentConfig(
                # This is the key line: we force the output to be JSON
                response_mime_type="application/json",
                # This tells the LLM the exact structure it must follow
                response_schema=GeneratedQuiz,
            ),
        )

        # 4. Parsing the Output
        # The Gemini API returns the raw JSON text. We manually load it and validate with Pydantic.
        quiz_data = json.loads(response.text)

        # Use the Pydantic model to validate and instantiate the object
        quiz_object = GeneratedQuiz(**quiz_data)

        print("Quiz successfully generated and validated by Pydantic!")
        return quiz_object

    except (APIError, json.JSONDecodeError, Exception) as e:
        print("ERROR: Failed to generate or parse quiz.")
        print(f"Details: {e}")
        # Optionally print the raw text response for debugging
        # print(f"Raw Response: {response.text}")
        return None


def generate_image_from_prompt(prompt: str, liverun: bool = LIVERUN) -> str:

    if not liverun:
        return TEST_IMAGE_BASE64

    client = get_genai_client()
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9",
            ),
        )
        generated = response.generated_images[0]
        image_bytes = generated.image.image_bytes

        if not image_bytes:
            raise ImageGenerationError(message="No Image", status_code=502)

        return image_bytes
    except ClientError as e:
        status_code = getattr(e, "status_code", 400)
        message = str(e)
        raise ImageGenerationError(message=message, status_code=status_code) from e
