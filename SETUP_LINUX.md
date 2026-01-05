# Linux Setup Instructions

Follow these steps to set up and run the RAG Chatbot on a Linux machine (Ubuntu/Debian).

## 1. Prerequisites
- **Python 3.10+**
  ```bash
  sudo apt update
  sudo apt install python3 python3-venv python3-pip git
  ```
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

# Install dependencies
pip install -r requirements.txt
```

## 3. Configuration (.env)

You need to set up your environment variables. 
Create a file named `.env` in the root folder (`rag-chatbot/.env`) and add your keys:

```bash
# Create the file
touch .env
nano .env
```

**Paste the following inside .env:**

```env
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

Press `Ctrl+X`, then `Y`, then `Enter` to save if using nano.

## 4. Initialize Data (Important!)

The vector database is not shared via Git, so you must build it locally using the provided data.

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
