from backend.prompt_builder import build_diagnosis_prompt

fake_rag_results = [
    {
        "focus_area": "Chest Pain",
        "source": "MedQuAD",
        "text": "Question: What is Chest Pain?\nAnswer: Chest pain can be a sign of a heart problem."
    },
    {
        "focus_area": "Heart Attack",
        "source": "MedQuAD",
        "text": "Question: What are the symptoms of Heart Attack?\nAnswer: Symptoms include chest pain and shortness of breath."
    },
    {
        "focus_area": "Coronary Heart Disease",
        "source": "MedQuAD",
        "text": "Question: What are the symptoms?\nAnswer: A common symptom is chest discomfort."
    },
    {
        "focus_area": "Should Not Appear",
        "source": "MedQuAD",
        "text": "This chunk should be ignored."
    },
]

prompt = build_diagnosis_prompt(
    symptoms="I have chest pain and shortness of breath",
    rag_results=fake_rag_results
)

print(prompt)

print("=" * 60)
print("CHECKS:")

print("[OK] symptoms in prompt" if "I have chest pain and shortness of breath" in prompt else "[FAIL] symptoms missing")

print("[OK] source 1 present" if "Chest Pain" in prompt else "[FAIL] source 1 missing")
print("[OK] source 2 present" if "Heart Attack" in prompt else "[FAIL] source 2 missing")
print("[OK] source 3 present" if "Coronary Heart Disease" in prompt else "[FAIL] source 3 missing")

print("[OK] 4th source correctly excluded" if "Should Not Appear" not in prompt else "[FAIL] 4th source leaked in!")

print("[OK] no leftover placeholders" if "{" not in prompt.replace("{{", "") else "[FAIL] found unresolved { in prompt}")