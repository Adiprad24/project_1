from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
import os
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Set OpenAI API Key
openai.api_key = os.getenv("OPENAI_API_KEY")  # Make sure this is set in your environment

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request schema
class QuestionRequest(BaseModel):
    question: str
    model: str = "gpt-4o"

# POST route
@app.post("/api")
async def answer_question(data: QuestionRequest):
    try:
        response = openai.ChatCompletion.create(
            model=data.model,
            messages=[
                {"role": "system", "content": "You are a helpful teaching assistant."},
                {"role": "user", "content": data.question}
            ]
        )
        return {"answer": response["choices"][0]["message"]["content"]}

    except openai.error.AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid or expired OpenAI API key.")

    except openai.error.RateLimitError:
        raise HTTPException(status_code=429, detail="Quota exceeded or too many requests.")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
