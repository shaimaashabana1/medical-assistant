from backend.pipeline import run_pipeline

# ==========================================================
# Test 1: حالة طوارئ - المفروض يقف بدري ومايكملش الـ pipeline
# ==========================================================
print("=" * 60)
print("TEST 1: Emergency case")
print("-" * 60)

result = run_pipeline("I have severe chest pain and can't breathe")
print(result)

if result.get("status") == "emergency":
    print("[OK] Correctly detected as emergency, pipeline stopped early")
else:
    print("[FAIL] Should have returned status='emergency'")


# ==========================================================
# Test 2: حالة عادية - المفروض يعدي بكل الـ steps
# ==========================================================
print("\n" + "=" * 60)
print("TEST 2: Normal medical query")
print("-" * 60)

result = run_pipeline("I have a mild headache and slight fever")

print("STATUS:", result.get("status"))
print("\nRETRIEVED CHUNKS COUNT:", len(result.get("retrieved_chunks", [])))
print("\nREVIEW:", result.get("review"))
print("\nFINAL RESPONSE:")
print(result.get("response"))

# Checks
checks = [
    ("status is 'success'", result.get("status") == "success"),
    ("has retrieved_chunks", len(result.get("retrieved_chunks", [])) == 5),
    ("has review dict", isinstance(result.get("review"), dict)),
    ("response is not empty", len(result.get("response", "")) > 0),
    ("response contains disclaimer", "Medical Disclaimer" in result.get("response", "")),
    ("no leftover fine-tuned diagnosis key", "diagnosis" not in result),
]

print("\n--- CHECKS ---")
for label, passed in checks:
    print(f"[{'OK' if passed else 'FAIL'}] {label}")


# ==========================================================
# Test 3: سؤال عربي - full flow
# ==========================================================
print("\n" + "=" * 60)
print("TEST 3: Arabic query - full flow")
print("-" * 60)

result = run_pipeline("عندي كحة وسخونية من يومين")

print("STATUS:", result.get("status"))
print("\nFINAL RESPONSE:")
print(result.get("response"))

if result.get("status") == "success" and len(result.get("response", "")) > 0:
    print("\n[OK] Arabic query completed the full pipeline")
else:
    print("\n[FAIL] Something broke on Arabic input")