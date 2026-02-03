import json
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import APIError
from typing import Optional

from llm_core.prompt_templates import (
    get_lesson_request_template,
    get_system_instructions,
    get_quiz_system_instruction,
)
from app.models.quiz_models import GeneratedQuiz
from testing.testing_data import TEST_LESSON_OUTPUT, TEST_QUIZ_OBJECT_PERFECT

# Load the API key from the .env file
load_dotenv()
client = genai.Client()

LIVERUN = False


def generate_daily_lesson(
    year_group: str, subject: str, topic_idea: str = "", liverun: bool = LIVERUN
) -> str:
    """Generates the lesson content and a prompt for a visual aid."""

    if not liverun:
        print("returning test results")
        return TEST_LESSON_OUTPUT

    # 3. API Call
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


def generate_quiz_from_lesson(
    lesson_text: str, year_group: str, liverun: bool = LIVERUN
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
