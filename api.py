from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agents.coordinator import process


app = FastAPI(title="LocalMind API")


app.add_middleware(
  CORSMiddleware,
  allow_origins=["http://localhost:5173"],
  allow_credentials=False,
  allow_methods=["GET","POST"],
  allow_headers=["Content-Type"]
)

class TaskRequest(BaseModel):
  question: str


from typing import Any
class TaskResponse(BaseModel):
  answer: str
  events: list[dict[str, Any]]


@app.get("api/health")
def health():
  return {"status": "online"}


@app.post("/api/task", response_model=TaskResponse)
def run_task(request: TaskRequest):
    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    events = []

    def capture_event(event):
        events.append(event)

    try:
        result = process(
            question,
            on_event=capture_event
        )

        return TaskResponse(
            answer=str(result),
            events=events
        )

    except Exception:
        import logging
        logging.exception("LocalMind task failed")

        raise HTTPException(
            status_code=500,
            detail="Agent execution failed"
        )