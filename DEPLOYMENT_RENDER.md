# Deploying to Render.com

This project is configured for easy deployment on Render.

## Option 1: Zero-Config Deployment (Recommended)

1. **Push** the latest code to your GitHub repository (already done!).
2. Log in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** and select **Blueprint**.
4. Connect your GitHub account and select this repository (**rag-chatbot**).
5. Render will detect the `render.yaml` file.
6. Click **Apply**.
7. **Important**: You will be prompted to enter your Environment Variables:
   - `GOOGLE_API_KEY`: [Required for Gemini Config]
   - `OPENAI_API_KEY`: [Optional Fallback]
8. Click **Create Web Service**.

Render will automatically:
- Install dependencies from `requirements.txt`.
- Run `start.sh` which:
    1. Converts CSVs to Markdown.
    2. Builds the Vector DB.
    3. Starts the API server.

## Option 2: Manual Setup

If you prefer to set it up manually without the blueprint:

1. Create a new **Web Service**.
2. Connect your repository.
3. Use the following settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `chmod +x start.sh && ./start.sh`
4. Add Environment Variables:
   - `OPENAI_API_KEY`: [Your Key]
   - `PYTHON_VERSION`: `3.10.12` (or similar)
5. Click **Deploy**.

## Troubleshooting

- **Deployment Logs**: Check the logs in the Render dashboard. You should see "Running Vector Ingestion..." followed by "Starting Uvicorn Server...".
- **Port**: Render automatically attempts to bind to port 10000 (handled by `$PORT` in the script).
