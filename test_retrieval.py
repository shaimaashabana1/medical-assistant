from backend.retrieval import retrieve

results = retrieve("I have chest pain and shortness of breath", top_k=3)
for r in results:
    print(round(r["similarity_score"], 3), "-", r["focus_area"], "-", r["text"][:100])


print("----")

results = retrieve("purple elephant flying spaceship", top_k=3)
for r in results:
    print(round(r["similarity_score"], 3), "-", r["focus_area"], "-", r["text"][:100])