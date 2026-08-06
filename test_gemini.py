from backend.gemini_client import generate_response, generate_json_response, generate_response_with_review


# ==========================================================
# Test : generate_response_with_review (اللي فعليًا بيستخدمه الـ pipeline)
# ==========================================================
print("\n" + "=" * 60)
print("TEST 3: generate_response_with_review (real medical prompt)")
print("-" * 60)

fake_prompt = """
You are an AI Medical Assistant.
Explain using ONLY these sources.

Source 1:
Question: What is Chest Pain?
Answer: Chest pain can be a sign of a heart problem and should be checked by a doctor.

User Symptoms: I have chest pain and shortness of breath.

Write a short explanation, possible causes, and a recommendation. Do not mention dosage. Do not confirm a diagnosis.
"""

result = generate_response_with_review(fake_prompt)
print("RESPONSE:")
print(result.get("response"))
print("\nREVIEW:")
print(result.get("review"))

# Checks
checks_passed = True

if "response" not in result or "review" not in result:
    print("[FAIL] Missing 'response' or 'review' key")
    checks_passed = False

if "unavailable" in str(result.get("response", "")).lower():
    print("[FAIL] Got the fallback error message - something went wrong")
    checks_passed = False

review = result.get("review", {})
expected_keys = {"has_dosage", "final_diagnosis", "hallucination"}
if not expected_keys.issubset(review.keys()):
    print(f"[FAIL] review missing keys, has: {review.keys()}")
    checks_passed = False

if checks_passed:
    print("\n[OK] All checks passed")