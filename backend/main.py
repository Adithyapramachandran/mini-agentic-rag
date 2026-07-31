from fastapi import FastAPI
from backend.controller import run_agent

app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Mini Agentic Pipeline API Running"
    }

@app.post("/ask")
def ask(data: dict):

    answer, trace = run_agent(
        data["query"]
    )

    return {
        "answer": answer,
        "trace": trace
    }