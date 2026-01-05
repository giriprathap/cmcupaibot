# Mac Setup Instructions

Follow these steps to set up and run the RAG Chatbot on a MacBook.

## 1. Prerequisites
- **Python 3.10+** (Install via Homebrew: `brew install python`)
- **Git**
- **Google API Key** (Required for Gemini Embeddings)
- **OpenAI API Key** (Optional, for fallback LLM)

## 2. Clone and Install

Open your Terminal and run:

```bash
# Clone the repository (if you haven't already)
git clone <repository_url>
cd rag-chatbot

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies (ensure you have openpyxl installed for Excel processing)
pip install -r requirements.txt
```

## 3. Configuration (.env)

You need to set up your environment variables. 
Create a file named `.env` in the root folder (`rag-chatbot/.env`) and add your keys:

```bash
# Create the file
touch .env
open .env
```

**Paste the following inside .env:**

```env
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

> **Note:** The system now defaults to **Gemini Embeddings**, so `GOOGLE_API_KEY` is critical.

## 4. Initialize Data (Important!)

The vector database includes recent Excel data ingestion. You must run the specialized script:

```bash
# 1. Ingest all data (Text + Excel) into Qdrant using Gemini Embeddings
# Make sure you are in the root folder 'rag-chatbot'
python ingest_full_gemini.py
```

You should see a success message indicating `data/qdrant_db` has been created.

## 5. Run the Application

Start the API server:

```bash
uvicorn api.main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

## 6. Verify

You can test if it's working by opening another terminal (remember to `source venv/bin/activate`) and running:

```bash
python tests/run_quick_test.py
```

## 7. How to Query (RAG Engine)

You can use the dedicated `/ask` endpoint to query the RAG engine directly.

**Using curl (Terminal):**

```bash
curl -X POST "http://127.0.0.1:8000/ask" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the rules for red cards?"}'
```

**Response:**
```json
{
  "response": "A red card results in the player being sent off...",
  "source": "rag_knowledge_base"
}
```
