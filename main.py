import re
from llm_core.generation_service import generate_daily_lesson, generate_quiz_from_lesson
from testing.testing_data import *


RUN_LIVE_LLM_LESSON_GENERATION = False


def parse_lesson_output(lesson_text: str) -> dict:
    """
    Parses the lesson string output based on the rigid tags used in the prompt.
    Uses non-greedy matching to capture content accurately between tags.
    """
    data = {}

    # 1. Title Match: Capture everything after **TITLE:** and before the next **BODY:** tag.
    # We use a non-greedy match (.*?) to stop before the next tag.
    title_match = re.search(
        r"\*\*TITLE:\*\*\s*(.*?)\s*\*\*BODY:\*\*", lesson_text, re.DOTALL
    )
    if title_match:
        data["title"] = title_match.group(1).strip()

    # 2. Body Match: Capture everything after **BODY:** and before **VISUAL-PROMPT:**
    # We are flexible with any characters (including newlines) between them.
    body_match = re.search(
        r"\*\*BODY:\*\*\s*(.*?)\s*\*\*VISUAL-PROMPT:\*\*", lesson_text, re.DOTALL
    )
    if body_match:
        # The body often contains trailing Markdown elements (like the '---' you noticed).
        # We perform one extra strip to remove common tail noise like '---' or newlines.
        data["body"] = body_match.group(1).strip().strip("---").strip()

    # 3. Visual Prompt Match: Capture everything after **VISUAL-PROMPT:** to the end of the text.
    visual_match = re.search(r"\*\*VISUAL-PROMPT:\*\*\s*(.*)$", lesson_text, re.DOTALL)
    if visual_match:
        data["visual_prompt"] = visual_match.group(1).strip()

    # Fallback to handle malformed output where a tag is completely missing
    if not all(k in data for k in ["title", "body", "visual_prompt"]):
        print("Warning: One or more tags were not found. Falling back to simple split.")
        # You could add your simple split fallback here if necessary, but the regex should handle most cases.
    return data


# --- MAIN WORKFLOW ---
def run_tutor_workflow():
    print(f"--- Running AI Tutor for {TEST_YEAR} {TEST_SUBJECT} ---")

    # 1. Lesson Generation (or use Test Data)
    print(f"1. Generating Lesson (LIVE API CALL: {RUN_LIVE_LLM_LESSON_GENERATION})...")
    lesson_raw_output = generate_daily_lesson(
        TEST_YEAR, TEST_SUBJECT, RUN_LIVE_LLM_LESSON_GENERATION
    )

    # 2. Parsing the Lesson Content
    print("2. Parsing Lesson Content...")
    lesson_data = parse_lesson_output(lesson_raw_output)

    # Check if we got the core lesson content (the BODY)
    if not lesson_data.get("body"):
        print("FAILED: Could not parse lesson body. Exiting.")
        return

    # Print the extracted parts
    print(f"   > TITLE: {lesson_data.get('title', 'N/A')}")
    print(f"   > VISUAL PROMPT: {lesson_data.get('visual_prompt', 'N/A')[:50]}...")

    # 3. Quiz Generation (API Call)
    print(f"\n3. Generating Quiz (LIVE API CALL: {RUN_LIVE_LLM_LESSON_GENERATION})...")

    # We pass the extracted BODY content to the quiz generator
    quiz_object = generate_quiz_from_lesson(
        lesson_data["body"], TEST_YEAR, RUN_LIVE_LLM_LESSON_GENERATION
    )

    # 4. Displaying/Using the Results
    if quiz_object and quiz_object.quiz_questions:
        print("\n---Daily Page Ready ---")
        print(f"Lesson Title: {lesson_data.get('title')}")
        print("--- Lesson Content (BODY) Displayed Here ---")

        print("\n--- QUIZ TIME ---")

        # Demonstrating how to use the structured quiz data
        for i, q in enumerate(quiz_object.quiz_questions):
            print(f"Q{i + 1}: {q.question}")
            # Note: We display the options using their index for the user
            for j, option_text in enumerate(q.options):
                print(f"   {['A', 'B', 'C', 'D'][j]}. {option_text}")

            # --- Answer Check Logic (for your backend) ---
            # Simulate user choosing the 2nd option (Index 1, which is key 'B')
            simulated_user_choice_key = "B"

            is_correct = simulated_user_choice_key == q.correct_key

            print(
                f"   [DEV CHECK] Correct Key: {q.correct_key} | User Chose: {simulated_user_choice_key} | Correct: {is_correct}"
            )

            if is_correct:
                print(f"   CORRECT! Explanation: {q.explanation}")
            else:
                print(
                    f"   INCORRECT. The correct answer was {q.correct_key}. Explanation: {q.explanation}"
                )

    else:
        print("\nFINAL FAILURE: Could not generate a valid quiz.")


if __name__ == "__main__":
    run_tutor_workflow()
