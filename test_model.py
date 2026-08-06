import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# ==========================
# 1. Path of merged model
# ==========================
MODEL_PATH = "models/Qwen-Merged-Diagnosis"

# ==========================
# 2. Load tokenizer
# ==========================
print("Loading tokenizer...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# ==========================
# 3. Load model
# ==========================
print("Loading model...")

model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float32
)

model.eval()

print("Model loaded successfully!")

# ==========================
# 4. User symptoms
# ==========================
symptoms = """
I have fever, sore throat, headache and body pain.
"""

# ==========================
# 5. Chat format
# ==========================
messages = [
    {
        "role": "system",
        "content": "You are a medical assistant. Given symptoms, return only the most likely diagnosis."
    },
    {
        "role": "user",
        "content": symptoms
    }
]

# ==========================
# 6. Convert to model input
# ==========================
text = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

inputs = tokenizer(
    text,
    return_tensors="pt"
)

# ==========================
# 7. Generate answer
# ==========================
print("Generating...\n")

with torch.no_grad():

    outputs = model.generate(
        **inputs,
        max_new_tokens=50,
        do_sample=False
    )

# ==========================
# 8. Decode output
# ==========================
response = tokenizer.decode(
    outputs[0],
    skip_special_tokens=True
)

print(response)