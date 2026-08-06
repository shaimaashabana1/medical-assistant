# gemini_client.py

import os
import json
from google import genai
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY not found. Please set it in your .env file.")

client = genai.Client(api_key=GEMINI_API_KEY)

MODEL_NAME = "gemini-flash-latest"


def generate_response(prompt: str) -> str:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"[gemini_client] Error calling Gemini API: {e}")
        return "Sorry, something went wrong while generating the response. Please try again."


def generate_json_response(prompt: str) -> dict:
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        raw_text = response.text.strip()

        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            raw_text = raw_text.replace("json", "", 1).strip()

        return json.loads(raw_text)
    except Exception as e:
        print(f"[gemini_client] Error parsing JSON response: {e}")
        return {"has_dosage": True, "final_diagnosis": True, "hallucination": True}

import json

def generate_response_with_review(prompt: str) -> dict:
    """
    Gemini returns BOTH:
    - final response
    - safety review
    """

    full_prompt = f"""
{prompt}

----------------------------------------

After generating the answer,
review your own response.

Return ONLY valid JSON.

JSON format:

{{
    "response":"...",
    "review":{{
        "has_dosage":false,
        "final_diagnosis":false,
        "hallucination":false
    }}
}}

Rules:

- has_dosage:
true ONLY if you mentioned a medication dosage.

- final_diagnosis:
true ONLY if you presented the disease as confirmed.

- hallucination:
true ONLY if you used information NOT supported by the provided sources.

Return JSON ONLY.
"""

    try:

        response = client.models.generate_content(

            model=MODEL_NAME,

            contents=full_prompt

        )

        text = response.text.strip()

        if text.startswith("```"):

            text = text.replace("```json", "")

            text = text.replace("```", "")

        return json.loads(text)

    except Exception as e:

        print(e)

        return {

            "response":

            "Sorry, the AI service is currently unavailable. Please try again later.",

            "review":{

                "has_dosage":False,

                "final_diagnosis":False,

                "hallucination":False

            }

        }