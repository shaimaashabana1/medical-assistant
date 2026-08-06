import json
import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter

df = pd.read_csv("medquad_clean.csv")
print(f"Loaded {len(df)} records")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=100,
    separators=["\n\n", "\n", ". ", " ", ""]
)

chunks = []
chunk_id = 0

for _, row in df.iterrows():
    answer_pieces = text_splitter.split_text(str(row["answer"]))

    for piece in answer_pieces:
        full_text = f"Question: {row['question']}\nAnswer: {piece}"

        chunks.append({
            "chunk_id": chunk_id,
            "text": full_text,
            "question": row["question"],
            "focus_area": row["focus_area"],
            "source": row["source"]
        })
        chunk_id += 1

print(f"Generated {len(chunks)} chunks")

with open("chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, ensure_ascii=False, indent=4)

print("Chunks saved successfully.")