import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Get the exact folder where qna.py is located
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

# Force Python to load this exact .env file
load_dotenv(ENV_FILE, override=True)

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError(
        f"GEMINI_API_KEY is missing. Python looked here: {ENV_FILE}"
    )

client = genai.Client(api_key=API_KEY)


def answer_question(question: str) -> str:
    prompt = f"""
You are EduGenie, an educational AI assistant.

Answer the student's question clearly and accurately.
Use simple language suitable for a student.

Student question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text.strip()