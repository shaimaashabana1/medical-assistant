from backend.gemini_client import generate_json_response

# ==========================================================
# Emergency Detection
# ==========================================================

EMERGENCY_KEYWORDS = [
    "chest pain",
    "can't breathe",
    "difficulty breathing",
    "severe bleeding",
    "stroke",
    "heart attack",
    "anaphylaxis",
    "severe allergic reaction",
    "unconscious",
    "suicide",

    # Arabic
    "ألم في الصدر",
    "وجع في الصدر",
    "مش قادر أتنفس",
    "ضيق تنفس",
    "نزيف شديد",
    "جلطة",
    "سكتة",
    "فقدان الوعي",
    "إغماء",
    "انتحار"
]

EMERGENCY_MESSAGE = """
⚠️ Medical Emergency

Your symptoms may indicate a medical emergency.

Please seek immediate medical care or contact your local emergency services.

This AI assistant cannot safely assess emergency situations.
"""


def check_emergency(user_input: str) -> bool:
    """
    Returns True if the user message contains emergency keywords.
    """

    text = user_input.lower()

    return any(keyword.lower() in text for keyword in EMERGENCY_KEYWORDS)


# ==========================================================
# Gemini Self Review
# ==========================================================

def build_review_prompt(response: str, context: str) -> str:

    return f"""
You are reviewing a medical AI response.

Use ONLY the provided medical context.

Medical Context:

{context}

AI Response:

{response}

Answer ONLY with valid JSON.

{{
    "has_dosage": true/false,
    "final_diagnosis": true/false,
    "hallucination": true/false
}}

Rules:

has_dosage
True only if a specific medication dosage or amount is mentioned.

final_diagnosis
True only if the response claims the disease is confirmed.

hallucination
True only if the response contains medical claims unsupported by the provided context.

Return JSON only.
"""


def review_response(response: str, context: str) -> dict:
    """
    Reviews the generated response using Gemini.
    """

    try:
        return generate_json_response(
            build_review_prompt(response, context)
        )

    except Exception as e:

        print("[Safety Review Error]", e)

        return {
            "has_dosage": False,
            "final_diagnosis": False,
            "hallucination": False
        }


# ==========================================================
# Apply Safety
# ==========================================================

def apply_safety_disclaimer(response: str,
                            review_result: dict) -> str:

    warnings = []

    if review_result.get("has_dosage", False):

        warnings.append(
            "⚠️ Do not rely on any medication dosage without consulting a qualified doctor."
        )

    if review_result.get("hallucination", False):

        warnings.append(
            "⚠️ Some information in the response could not be fully verified using the retrieved medical sources."
        )

    if warnings:

        response += "\n\n"

        response += "\n".join(warnings)

    response += """

----------------------------------------

Medical Disclaimer

This AI assistant provides educational information only.

It is NOT a substitute for professional medical advice,
diagnosis, or treatment.

Always consult a qualified healthcare professional.

If your symptoms become severe or you believe you have a medical emergency,
seek immediate medical care.
"""

    return response