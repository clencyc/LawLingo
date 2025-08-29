
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

import random
import os
from dotenv import load_dotenv
import logging

# Gemini API integration
import google.generativeai as genai

# Setup logging
logging.basicConfig(
    filename='gemini_api.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

load_dotenv()
GEMINI_API_KEY = 'AIzaSyD8S45OuUJj9gg8S8jLqEFHvXTuRMehfkU'
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

router = APIRouter()

# Example Kenyan law topics and sample data for creativity
KENYAN_LAW_TOPICS = [
    {
        "topic": "Bill of Rights",
        "facts": [
            "Every person has the right to life.",
            "Every person has the right to freedom and security of the person.",
            "Every person has the right to privacy.",
            "Every person has the right to freedom of expression.",
        ],
        "questions": [
            {
                "question": "Which right is guaranteed by the Kenyan Constitution?",
                "options": [
                    "Right to life",
                    "Right to own a private army",
                    "Right to unlimited property",
                    "Right to rule by decree"
                ],
                "correct_answer": 0
            },
            {
                "question": "Which of these is NOT a right under the Bill of Rights?",
                "options": [
                    "Right to privacy",
                    "Right to freedom of expression",
                    "Right to be above the law",
                    "Right to life"
                ],
                "correct_answer": 2
            }
        ]
    },
    {
        "topic": "Structure of Government",
        "facts": [
            "Kenya has three arms of government: Executive, Legislature, Judiciary.",
            "The President is the Head of State and Government.",
            "The National Assembly and Senate form the Parliament."
        ],
        "questions": [
            {
                "question": "How many arms of government does Kenya have?",
                "options": ["Two", "Three", "Four", "One"],
                "correct_answer": 1
            },
            {
                "question": "Who is the Head of State in Kenya?",
                "options": ["Chief Justice", "Speaker of the National Assembly", "President", "Attorney General"],
                "correct_answer": 2
            }
        ]
    }
]


class QuizRequest(BaseModel):
    topic: Optional[str] = None  # e.g., "Bill of Rights"
    num_questions: int = 1

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    topic: str


@router.post("/quiz/generate", response_model=List[QuizQuestion])
async def generate_quiz(request: QuizRequest):
    """
    AI-powered endpoint to generate quiz questions on Kenyan law using Gemini API.
    """
    if not GEMINI_API_KEY:
        raise HTTPException(status_code=500, detail="Gemini API key not configured.")

    topic = request.topic or "Kenyan Constitution"
    num_questions = request.num_questions or 1
    prompt = f"""
    Generate {num_questions} multiple-choice quiz questions about the topic '{topic}' in the Kenyan Constitution. 
    For each question, provide:
    - The question text
    - Four answer options (A, B, C, D)
    - The index (0-based) of the correct answer
    Respond in JSON as a list of objects with keys: question, options, correct_answer.
    """
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        import json
        text = response.text.strip()
        logging.info(f"Gemini response: {text}")
        # Find the first and last brackets to extract JSON
        start = text.find('[')
        end = text.rfind(']')
        if start == -1 or end == -1:
            logging.error(f"No JSON array found in Gemini response: {text}")
            raise ValueError("No JSON array found in Gemini response.")
        json_str = text[start:end+1]
        questions = json.loads(json_str)
        # Validate and return as QuizQuestion list
        return [QuizQuestion(
            question=q["question"],
            options=q["options"],
            correct_answer=q["correct_answer"],
            topic=topic
        ) for q in questions]
    except Exception as e:
        logging.error(f"Gemini API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Gemini API error: {str(e)}")

# Existing daily challenge endpoint (static for now)
@router.get("/challenges/daily")
async def get_daily_challenge(user_id: int = 1):
    return {
        "challenge_id": 1,
        "title": "What is a Constitution?",
        "question": "Which of these is a core function of a constitution?",
        "options": [
            "Define government structure",
            "Set tax rates",
            "Elect the president",
            "None of the above"
        ],
        "correct_answer": 0,
        "xp_reward": 10,
    }