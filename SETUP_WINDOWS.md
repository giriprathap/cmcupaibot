# Windows 11 Setup Instructions

Follow these steps to set up and run the RAG Chatbot on Windows 11.

## 1. Prerequisites
- **Python 3.10+**: Download and install from [python.org](https://www.python.org/downloads/). **Make sure to check "Add Python to PATH" during installation.**
- **Git**: Download and install from [git-scm.com](https://git-scm.com/download/win).
- **Google API Key**: (Required for Gemini Embeddings)
- **OpenAI API Key**: (Optional, for fallback LLM)
- **VS Code** (Recommended) or PowerShell.

## 2. Clone and Install

Open PowerShell or Command Prompt and run:

```powershell
# Clone the repository
git clone <repository_url>
cd rag-chatbot

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# If you get a permission error, run: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 3. Configuration (.env)

You need to set up your environment variables. 
Create a file named `.env` in the root folder (`rag-chatbot\.env`).

1. Right-click in the folder > New > Text Document.
2. Rename it to `.env` (make sure it's not `.env.txt`).
3. Open it with Notepad.

**Paste the following inside .env:**

```env
GOOGLE_API_KEY=your_google_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

## 4. Initialize Data (Important!)

The vector database for the RAG system must be built locally.

```powershell
# Ensure your virtual environment is active (you should see (venv) in the prompt)

# 1. Ingest all data (Text + Excel) into Qdrant using Gemini Embeddings
python ingest_full_gemini.py
```

Wait for the success message.

## 5. Run the Application

Start the API server:

```powershell
uvicorn api.main:app --reload
```

The API will run at `http://127.0.0.1:8000`.

## 6. Verify

Open a new PowerShell window, activate the venv again, and run:

```powershell
.\venv\Scripts\activate
python tests/run_quick_test.py
```
