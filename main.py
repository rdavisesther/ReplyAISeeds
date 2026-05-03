from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")


class GenerateRequest(BaseModel):
    prompt: str


@app.get("/")
def home():
    return {"status": "Backend is running"}


@app.post("/api/generate-reply")
def generate_reply(data: GenerateRequest):
    try:
        response = model.generate_content(data.prompt)

        reply = response.text.strip()

        return {
            "reply": reply
        }

    except Exception as e:
        return {
            "error": str(e)
        }