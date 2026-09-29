import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Load .env from the EduGenie project folder
BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE, override=True)

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

if not API_KEY:
    raise RuntimeError(
        f"GEMINI_API_KEY is missing. Python looked here: {ENV_FILE}"
    )

client = genai.Client(api_key=API_KEY)


def summarize_text(text: str) -> str:
    """
    Summarize educational text into a concise,
    easy-to-understand version.
    """

    text = text.strip()

    if not text:
        return "Please provide some text to summarize."

    prompt = f"""
You are EduGenie, an educational AI assistant.

Summarize the following educational text for a student.

Requirements:
- Keep the main ideas and important facts.
- Remove unnecessary repetition.
- Use simple and clear language.
- Make the summary concise.
- Do not add information that is not present in the original text.
- Use short paragraphs or bullet points when appropriate.

Text to summarize:
{text}
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        if not response.text:
            return "Unable to generate a summary."

        return response.text.strip()

    except Exception as e:
        return f"Error while generating summary: {str(e)}"