# backend/pipeline.py

from backend.safety_layer import (
    check_emergency,
    apply_safety_disclaimer,
    EMERGENCY_MESSAGE,
)

from backend.retrieval import retrieve
from backend.prompt_builder import build_diagnosis_prompt
from backend.gemini_client import generate_response_with_review


def run_pipeline(user_input: str) -> dict:
    """
    Complete Medical Assistant Pipeline (RAG + Gemini + Safety).
    """

    # ==========================================================
    # Step 1 : Emergency Check
    # ==========================================================

    if check_emergency(user_input):
        return {
            "status": "emergency",
            "response": EMERGENCY_MESSAGE
        }

    # ==========================================================
    # Step 2 : Retrieve Medical Context
    # ==========================================================

    rag_results = retrieve(user_input, top_k=5)

    # ==========================================================
    # Step 3 : Build Prompt
    # ==========================================================

    prompt = build_diagnosis_prompt(
        symptoms=user_input,
        rag_results=rag_results
    )

    # ==========================================================
    # Step 4 : Generate Response + Safety Review (One API Call)
    # ==========================================================

    gemini_result = generate_response_with_review(prompt)

    response = gemini_result["response"]
    review = gemini_result["review"]

    # ==========================================================
    # Step 5 : Apply Safety Disclaimer
    # ==========================================================

    final_response = apply_safety_disclaimer(
        response,
        review
    )

    # ==========================================================
    # Return Result
    # ==========================================================

    return {
        "status": "success",
        "symptoms": user_input,
        "retrieved_chunks": rag_results,
        "review": review,
        "response": final_response
    }