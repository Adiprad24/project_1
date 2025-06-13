from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from openai import OpenAI, APIConnectionError, AuthenticationError, RateLimitError, OpenAIError
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY not set in environment.")

client = OpenAI(api_key=api_key)

class QuestionRequest(BaseModel):
    question: str
    model: str = "gpt-4o"

@app.post("/api")
async def answer_question(data: QuestionRequest):
    try:
        response = client.chat.completions.create(
            model=data.model,
            messages=[
                {"role": "system", "content": "You are a helpful teaching assistant."},
                {"role": "user", "content": data.question}
            ]
        )
        return {"answer": response.choices[0].message.content}

    except AuthenticationError:
        raise HTTPException(status_code=401, detail="Invalid or expired OpenAI API key.")
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded or quota used up.")
    except APIConnectionError:
        raise HTTPException(status_code=503, detail="OpenAI service unavailable.")
    except OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
