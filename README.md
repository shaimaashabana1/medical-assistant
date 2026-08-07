# 🩺 AI Medical Assistant

An AI-powered medical assistant that provides safe, source-grounded health information using **Retrieval-Augmented Generation (RAG)**, **Google Gemini**, and a dedicated **multi-layer safety system**.

> ⚠️ Disclaimer: For educational purposes only. Not a substitute for professional medical advice, diagnosis, or treatment.

---

## Overview

Instead of letting an LLM answer medical questions purely from its own internal knowledge (risking hallucination and outdated information), this system:

1. **Retrieves** relevant medical context from a trusted dataset (MedQuAD) via semantic vector search.
2. **Generates** a response with Google Gemini, strictly grounded in the retrieved sources.
3. **Reviews and filters** the response through a safety layer — preventing dosage recommendations, confirmed diagnoses, and unverified claims.

An **emergency detection layer** short-circuits the pipeline immediately for potentially life-threatening symptoms, bypassing the LLM entirely.

---

## Architecture

```
User Input
    │
    ▼
[1] Emergency Check ───────► If detected: return static emergency message immediately
    │
    ▼
[2] RAG Retrieval (FAISS + sentence-transformers)
    │
    ▼
[3] Prompt Construction (rules + retrieved sources)
    │
    ▼
[4] Gemini Generation + Self-Review (single API call)
    │
    ▼
[5] Safety Disclaimer & Warning Injection
    │
    ▼
Final Response
```

---

## Project Structure

```
MedicalAssistant/
├── backend/
│   ├── pipeline.py          # Orchestrates the full request flow
│   ├── retrieval.py         # Embedding + FAISS vector search
│   ├── prompt_builder.py    # Builds the structured prompt for Gemini
│   ├── gemini_client.py     # Handles all Gemini API communication
│   └── safety_layer.py      # Emergency detection + safety disclaimers
├── data/                     # MedQuAD dataset + chunked JSON
├── vector_store/              # FAISS index + chunk metadata
├── chunking.py                # Offline script: builds chunks.json from raw CSV
├── app_streamlit.py            # Streamlit UI (entry point)
├── requirements.txt
└── .env                        # API keys (not committed)
```

---

## Tech Stack

- **Python**, **Google Gemini API**, **FAISS**, **sentence-transformers** (`all-MiniLM-L6-v2`), **LangChain** (chunking), **Streamlit**, **MedQuAD dataset**

---

## Setup

```bash
git clone https://github.com/shaimaashabana1/medical-assistant.git
cd medical-assistant
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

Run:
```bash
streamlit run app_streamlit.py
```

> On first run, `retrieval.py` builds the FAISS index automatically from `data/chunks.json` if it doesn't exist yet.

---

## Testing

| Module | Test File |
|---|---|
| Retrieval | `test_retrieval.py` |
| Prompt Builder | `test_prompt.py` |
| Gemini Client | `test_gemini.py` |
| Safety Layer | `test_safety.py` |
| Full Pipeline | `test_pipeline.py` |

---

## Safety Design

Three independent layers, not a single point of control:

1. **Prompt-level constraints** — explicit rules against inventing information, confirming diagnoses, or giving dosages.
2. **LLM self-review** — Gemini flags its own response for dosage mentions, confirmed-diagnosis language, and unsupported claims, in the same API call as generation.
3. **Rule-based post-processing** — deterministic emergency keyword detection and disclaimer injection, independent of the LLM.

---

## Known Limitations

- Embedding model (`all-MiniLM-L6-v2`) retrieves English queries well but Arabic queries weakly. Planned: multilingual embedding model.
- Emergency detection covers formal Arabic but may miss colloquial phrasing.
- MedQuAD is English-only; multilingual support relies on the embedding layer bridging the gap at retrieval time.