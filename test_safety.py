from backend.safety_layer import check_emergency, apply_safety_disclaimer, EMERGENCY_MESSAGE

# ==========================================================
# Test 1: check_emergency - True
# ==========================================================
print("=" * 60)
print("TEST 1: check_emergency - should be TRUE")
print("-" * 60)

should_be_true = [
    "I have chest pain",
    "I CAN'T BREATHE",  # تتأكدي إن lower() شغالة
    "he had a stroke yesterday",
    "عندي ألم في الصدر",
    "حسيت اني هغمى عليا",
]

for text in should_be_true:
    result = check_emergency(text)
    status = "OK" if result else "FAIL"
    print(f"[{status}] '{text}' -> {result}")


# ==========================================================
# Test 2: check_emergency - False
# ==========================================================
print("\n" + "=" * 60)
print("TEST 2: check_emergency - should be FALSE")
print("-" * 60)

should_be_false = [
    "I have a mild headache",
    "what is diabetes",
    "عندي صداع بسيط",
    "ما هي أعراض البرد",
]

for text in should_be_false:
    result = check_emergency(text)
    status = "OK" if not result else "FAIL"
    print(f"[{status}] '{text}' -> {result}")


# ==========================================================
# Test 3: apply_safety_disclaimer -
# ==========================================================
print("\n" + "=" * 60)
print("TEST 3: apply_safety_disclaimer - no warnings")
print("-" * 60)

review_clean = {"has_dosage": False, "final_diagnosis": False, "hallucination": False}
result = apply_safety_disclaimer("This is a sample response.", review_clean)
print(result)

if "Do not rely on any medication dosage" not in result and "Medical Disclaimer" in result:
    print("[OK] No warning added, disclaimer present")
else:
    print("[FAIL] Something's off")


# ==========================================================
# Test 4: apply_safety_disclaimer - 
# ==========================================================
print("\n" + "=" * 60)
print("TEST 4: apply_safety_disclaimer - with warnings")
print("-" * 60)

review_bad = {"has_dosage": True, "final_diagnosis": False, "hallucination": True}
result = apply_safety_disclaimer("This is a sample response.", review_bad)
print(result)

checks = [
    ("dosage warning present", "Do not rely on any medication dosage" in result),
    ("hallucination warning present", "could not be fully verified" in result),
    ("disclaimer present", "Medical Disclaimer" in result),
]

for label, passed in checks:
    print(f"[{'OK' if passed else 'FAIL'}] {label}")