import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ==========================================================
# Load Fine-Tuned Diagnosis Model (Load Once)
# ==========================================================

MODEL_PATH = "models/Qwen-Merged-Diagnosis"

print("Loading Diagnosis Model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float32
)

model.eval()

print("Diagnosis Model Loaded Successfully!")


# ==========================================================
# Diagnose Function
# ==========================================================

def diagnose(symptoms: str) -> dict:
    """
    Input:
        symptoms (str)

    Output:
        {
            "symptoms": "...",
            "disease": "...",
            "confidence": None,
            "matched_symptoms": []
        }
    """

    messages = [
        {
            "role": "system",
            "content":
                "You are a medical assistant. "
                "Return ONLY the most likely disease name."
        },
        {
            "role": "user",
            "content": symptoms
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=30,
            do_sample=False
        )

    response = tokenizer.decode(
        outputs[0],
        skip_special_tokens=True
    )

    if "assistant" in response:
        disease = response.split("assistant")[-1].strip()
    else:
        disease = response.strip()

    result = {
        "symptoms": symptoms,
        "disease": disease,
        "confidence": None,
        "matched_symptoms": []
    }

    return result