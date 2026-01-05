#!/bin/bash

# 1. Process CSVs to Markdown
echo "🔄 [1/3] Converting CSVs to Markdown..."
python process_sql_data.py

# 2. Ingest Data to Qdrant (Local) - Using Gemini Embeddings
echo "🧠 [2/3] Building Vector Database..."
python ingest_full_gemini.py

# 3. Start API Server
echo "🚀 [3/3] Starting Uvicorn Server..."
# Render sets the PORT environment variable
uvicorn api.main:app --host 0.0.0.0 --port $PORT
