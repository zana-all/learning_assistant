# 1. System Instruction (Persona and Rules)
def get_system_instructions(year_group: str, subject: str) -> str:
    """Return system instructions"""
    return f""" You are an expert, friendly, and engaging tutor for
    a student in Year **{year_group} {subject}**.
    Your goal is to create a single, concise daily lesson page.
    The tone must be encouraging, accessible, and perfectly tailored to the specified year group's curriculum and knowledge level.
    """


# 2. User Prompt (The Request and Structure)
def get_lesson_request_template(
    year_group: str, subject: str, topic_idea: str | None = None
) -> str:
    topic_line = (
        f'The lesson must focus specifically on "{topic_idea}".' if topic_idea else ""
    )

    return f"""
        You are generating educational content for a learning application.

        Generate a lesson on one specific sub-topic within {subject}
        suitable for a Year {year_group} student.
        {topic_line}

        You MUST return your response as valid JSON only.

        The JSON must follow this exact schema:

        {{
        "title": string,
        "lesson_text": string,
        "visual_prompt": string
        }}

        Rules:
        - lesson_text should be the full lesson content.
        - visual_prompt must be a concise text-to-image prompt (max 50 words).
        - Do not include markdown or extra text.
        """


def get_quiz_system_instruction(year_group) -> str:
    return f"""
    You are an expert quiz generator. Your task is to generate exactly 3 multiple-choice questions 
    based ONLY on the lesson text provided by the user. The questions must be appropriate for a 
    Year '{year_group}' student. You MUST return the output as a valid JSON object that strictly adheres
    to the provided schema.
    """
