from fastapi import FastAPI
from pydantic import BaseModel
from app.agent import run_agent
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

app = FastAPI(
    title="Enterprise IT Service Assistant",
    description="AI-powered IT Service and Asset Operations Assistant",
    version="1.0.0"
)
BASE_DIR = Path(__file__).resolve().parent.parent

STATIC_DIR = BASE_DIR / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static"
)


class ChatRequest(BaseModel):
    message:str

@app.post("/chat")
def chat(request: ChatRequest):
    response = run_agent(request.message)

    return{
        "response": response
    }

@app.post("/api/chat")
def frontend_chat(request: ChatRequest):
    result = run_agent(
        request.message,
        include_activity=True
    )

    return {
        "answer": result["answer"],
        "trace": result["trace"]
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")