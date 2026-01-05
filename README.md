# 🤖 CMCUP-AIBOTS: Multilingual Hybrid RAG Chatbot

An advanced **AI-powered Chatbot** built for the **CM Cup Sports Tournament**. 
This system employs a **Hybrid RAG Strategy** to deliver precise, context-aware answers in **English, Hindi, and Telugu**. It seamlessly switches between direct data lookups for player stats and semantic search for general tournament queries.

---

## ✨ Key Features

- **🧠 Hybrid Intelligence:**
  - **Direct Lookup:** Instantly retrieves volatile data (Player Status, Scores) using Regex matching for accuracy.
  - **RAG (Retrieval-Augmented Generation):** Uses Vector Search (Qdrant) to answer general questions about fixtures, rules, and venues.
  - **LLM Fallback:** Gracefully handles out-of-scope queries using large language models.

- **🌐 Multilingual Support:**
  - Full support for **English**, **Hindi**, and **Telugu**.
  - Automatically detects query language and responds in the same language.

- **🛡️ Robust Architecture:**
  - **Orchestration:** Powered by **LiteLLM** for reliable model switching (OpenAI GPT-4 / Google Gemini).
  - **Vector Database:** **Qdrant** for high-performance similarity search.
  - **API:** Fast and asynchronous **FastAPI** backend.

---

## 🏗️ System Architecture

### 1. The Direct Lookup Layer (High Precision)
*   **Trigger:** Detects a valid **10-digit Mobile Number**.
*   **Source:** `data/csvs/player_details.csv` & related tables.
*   **Action:** Bypasses LLM to fetch exact rows.
*   **Result:** A deterministic "Player Status Card" with zero hallucinations.

### 2. The RAG Layer (Knowledge Base)
*   **Trigger:** General questions (e.g., "When is the Kho-Kho final?").
*   **Pipeline:**
    1.  **Ingestion:** CSVs are converted to narrative Markdown via `process_sql_data.py`.
    2.  **Embedding:** Text is chunked and embedded using **OpenAI/HuggingFace** models.
    3.  **Storage:** Vectors stored locally in `data/qdrant_db`.
    4.  **Retrieval:** Top-k relevant chunks extracted based on query semantic similarity.
    5.  **Generation:** LLM synthesizes an answer using the retrieved context.

---

## 📂 Project Structure

```plaintext
rag-chatbot/
├── api/
│   └── main.py             # FastAPI Application & Routing
├── data/
│   ├── csvs/               # Raw Source Data (CSVs)
│   ├── mdFiles/            # Processed Knowledge Base (Markdown)
│   └── qdrant_db/          # Local Vector Database
├── ingestion/
│   ├── run_ingestion.py    # Main Ingestion Script
│   └── embed_store.py      # Embedding & Storage Logic
├── rag/
│   ├── chain.py            # RAG Pipeline & LiteLLM Config
│   ├── lookup.py           # Direct Player Lookup Logic
│   └── retriever.py        # Qdrant Retriever Configuration
├── tests/                  # Test Suites & Stress Tests
├── process_sql_data.py     # Data Processing Script (CSV -> Markdown)
├── requirements.txt        # Python Dependencies
├── render.yaml             # Render Deployment Config
└── start.sh                # Deployment Startup Script
```

---

## 🛠️ Setup & Installation

We have detailed guides for every operating system:

- 🍎 **[Mac Setup Guide](SETUP_MAC.md)**
- 🪟 **[Windows Setup Guide](SETUP_WINDOWS.md)**
- 🐧 **[Linux Setup Guide](SETUP_LINUX.md)**

### Quick Start (General)

1.  **Clone & Install:**
    ```bash
    git clone <repo_url>
    pip install -r requirements.txt
    ```
2.  **Configure Secrets:**
    Create a `.env` file with your keys:
    ```env
    GOOGLE_API_KEY=AI...      # Required (Gemini Embeddings)
    OPENAI_API_KEY=sk-...     # Optional (Fallback LLM)
    ```
3.  **Build Knowledge Base** (Critical Step):
    ```bash
    # Ingest data (Text + Excel) using Gemini Embeddings
    python ingest_full_gemini.py
    ```
4.  **Run API:**
    ```bash
    uvicorn api.main:app --reload
    ```

---

## 🚀 Deployment

This project is "Deploy Ready" for **Render.com**.

👉 **[Read the Render Deployment Guide](DEPLOYMENT_RENDER.md)**

It includes a `render.yaml` Blueprint for zero-config deployment and a `start.sh` script that handles data persistence and server startup automatically.

---

## 🔌 API Usage

**Base URL:** `http://localhost:8000`

### `POST /ask`

Ask a question to the bot.

**Request:**
```json
{
  "query": "Status for 7416613302"
}
```

**Response (Direct Lookup):**
```json
{
  "response": "Player Name: Ravi Kumar...\nStatus: Selected",
  "source": "sql_database"
}
```

**Request (Multilingual RAG):**
```json
{
  "query": "Kabaddi matches kab hain?"
}
```

**Response:**
```json
{
  "response": "Kabaddi ke matches 28th Dec ko subah 10 baje shuru honge...",
  "source": "rag_knowledge_base"
}
```

---

## 🧪 Testing

Run our built-in test suite to verify the system:

```bash
# Quick System Check
python tests/run_quick_test.py

# Multilingual Stress Test
python tests/test_multilingual.py
```

---

**Built with:** 🦜🔗 LangChain, 🧠 Qdrant, 🚀 FastAPI, and LiteLLM.