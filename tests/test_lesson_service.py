import json
import pytest

from services.lesson_service import parse_lesson_response


def test_parse_lesson_response_valid_json():
    payload = {
        "title": "Circuit Superheroes",
        "lesson_text": "A lesson about circuits.",
        "visual_prompt": "A simple diagram of a circuit.",
    }
    text = json.dumps(payload)

    parsed = parse_lesson_response(text)

    assert parsed["title"] == "Circuit Superheroes"
    assert "circuits" in parsed["lesson_text"].lower()
    assert parsed["visual_prompt"]


def test_parse_lesson_response_invalid_json_raises():
    bad = "{not valid json"
    with pytest.raises(Exception):
        parse_lesson_response(bad)
