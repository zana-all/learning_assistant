import json
from app.models.quiz_models import GeneratedQuiz, QuizQuestion

TEST_YEAR = "Year 8"
TEST_SUBJECT = "Science (Physics)"
TEST_TOPIC_IDEA = "How a Simple Electric Circuit Works"

TEST_LESSON_OUTPUT = {
    "title": "Circuit Superheroes: Unlocking the Secrets of Electricity!",
    "lesson_text": (
        "Hi Year 8 Scientists!\n\n"
        "Have you ever wondered how a torch lights up or how your favourite electronic gadgets get their power? "
        "It all comes down to something called an electric circuit. Today, we're going to explore how these amazing "
        "pathways work and what makes electricity flow. Get ready to become a circuit superhero!\n\n"
        "What is a Circuit?\n\n"
        "Imagine a race track for tiny invisible runners called electrons. For these runners to complete their journey "
        "and do some work like lighting a bulb, they need a continuous, complete path. That complete path is what we "
        "call an electric circuit. If the path is broken anywhere, the electrons cannot finish their race and nothing "
        "will happen.\n\n"
        "The Essential Parts of a Simple Circuit\n\n"
        "Every simple circuit needs a few key components working together:\n\n"
        "The Power Source\n"
        "This is usually a battery or a power pack. It provides the energy to push electrons around the circuit and has "
        "a positive and a negative terminal.\n\n"
        "The Conductors\n"
        "These are typically wires made of metal. Wires act like roads, giving electrons an easy path to travel.\n\n"
        "The Load\n"
        "This is the device that uses electrical energy to do something useful, such as a light bulb, motor, or buzzer.\n\n"
        "The Switch\n"
        "A switch allows us to open or close the circuit. When closed, electricity flows. When open, the circuit is broken.\n\n"
        "How Does it All Work?\n\n"
        "For electricity to flow, the circuit must be closed. Electrons move from the negative terminal of the battery, "
        "through the wires and the load, and return to the positive terminal. This movement of electrons is called "
        "electric current.\n\n"
        "Simple Circuit Examples\n\n"
        "A torch uses batteries, wires, a bulb, and a switch. When the switch is pressed, the circuit closes and the "
        "bulb lights up.\n\n"
        "A simple doorbell works by closing a circuit when the button is pressed, allowing electricity to flow to a "
        "buzzer and make a sound.\n\n"
        "Circuits are everywhere once you know what to look for. This is your first step toward understanding how the "
        "electrical world works."
    ),
    "visual_prompt": (
        "A colorful, simple cartoon diagram of a closed electric circuit showing a battery, connecting wires, "
        "a glowing light bulb, and a closed switch, with arrows indicating the flow of electric current."
    ),
}

TEST_LESSON_OUTPUT = json.dumps(TEST_LESSON_OUTPUT)


TEST_QUIZ_DATA_PERFECT = [
    {
        "question": "What is the primary role of the battery in a simple electric circuit?",
        "options": [
            "To act as a switch to break the circuit.",
            "To provide the energy (power source) to push electrons.",
            "To convert electrical energy into light.",
            "To prevent the current from flowing too fast.",
        ],
        "correct_key": "B",
        "explanation": "The battery is the power source, creating the potential difference needed to push the current (electrons) through the circuit.",
    },
    {
        "question": "Which of the following describes a 'closed' circuit?",
        "options": [
            "A path with no battery, so current cannot flow.",
            "A path where the wires are broken, causing a stop in current.",
            "A complete and continuous loop that allows current to flow freely.",
            "A circuit that has a motor but no light bulb.",
        ],
        "correct_key": "C",
        "explanation": "A closed circuit is a complete, unbroken loop. Current can only flow and power the load (like a bulb) when the circuit is closed.",
    },
    {
        "question": "In the analogy where electricity is a river, what do the wires represent?",
        "options": [
            "The Power Source.",
            "The Load (the worker).",
            "The Conductors (the roads).",
            "The Switch (the gatekeeper).",
        ],
        "correct_key": "C",
        "explanation": "Wires are conductors; they act as the roads or pathways for the electrons (the river) to travel from one point of the circuit to another.",
    },
]

TEST_QUIZ_DATA_COMPLEX = [
    {
        "question": "If you are trying to power a small electronic buzzer, which component of the circuit is the buzzer acting as?",
        "options": ["Power Source", "Conductor", "Load", "Switch"],
        "correct_key": "C",  # Testing key C
        "explanation": "The load is any component that consumes (uses) electrical energy to perform a task, such as a buzzer making noise.",
    },
    {
        "question": "Which component is missing if the circuit is otherwise complete but the electrons cannot start their journey?",
        "options": ["The Switch", "The Load", "The Conductor", "The Power Source"],
        "correct_key": "D",  # Testing key D
        "explanation": "The power source (battery) provides the initial energy to start the movement of electrons; without it, the circuit remains dormant.",
    },
    {
        "question": "In a torch, what action typically closes the circuit, allowing the bulb to light up?",
        "options": [
            "Opening the battery casing.",
            "Pressing the button (engaging the switch).",
            "Adding an extra wire.",
            "Replacing the light bulb.",
        ],
        "correct_key": "B",  # Testing key B
        "explanation": "Pressing the button on a torch closes the switch, which completes the circuit, allowing current to flow to the bulb.",
    },
]

TEST_QUIZ_OBJECT_PERFECT = GeneratedQuiz(
    quiz_questions=[QuizQuestion(**q) for q in TEST_QUIZ_DATA_PERFECT]
)

TEST_QUIZ_OBJECT_COMPLEX = GeneratedQuiz(
    quiz_questions=[QuizQuestion(**q) for q in TEST_QUIZ_DATA_COMPLEX]
)
