from fastapi import FastAPI, UploadFile, File, Request
from pydantic import BaseModel
import openai
import base64

app = FastAPI()

openai.api_key = "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"  # Get from https://platform.openai.com/account/api-keys

class QuestionRequest(BaseModel):
    question: str
    model: str = "gpt-4o"


@app.get("/")
def root():
    return {"message": "Hello Virtual TA"}


@app.post("/api")
async def answer_question(request: Request):
    data = await request.json()
    question = data.get("question")
    model = data.get("model", "gpt-4o")

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful teaching assistant."},
            {"role": "user", "content": question}
        ]
    )
    return {
        "answer": response["choices"][0]["message"]["content"]
    }
