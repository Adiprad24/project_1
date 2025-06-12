from fastapi import FastAPI, UploadFile, File, Request
from pydantic import BaseModel
import openai
import base64
import os
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




openai.api_key = os.getenv("OPENAI_API_KEY")  # Get from https://platform.openai.com/account/api-keys

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
