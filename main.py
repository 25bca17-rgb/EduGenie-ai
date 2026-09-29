from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie AI",
    description="AI-powered educational assistant",
    version="1.0.0",
)

# Static files
app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

# HTML templates
templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request},
    )


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": "EduGenie AI",
    }



@app.post("/qa")
async def qa(request: QuestionRequest):
    question = request.question.strip()

    if not question:
        return {"answer": "Please enter a question."}

    try:
        from qna import answer_question

        answer = answer_question(question)

        return {
            "question": question,
            "answer": answer
        }

    except Exception as e:
        return {
            "question": question,
            "answer": f"Error: {str(e)}"
        }   