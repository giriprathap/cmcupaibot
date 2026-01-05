import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
print(f"API Key found: {bool(api_key)}")
if api_key:
    print(f"Key ends with: ...{api_key[-4:]}")

try:
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
    vector = embeddings.embed_query("Hello world")
    print("✅ API Key works! Embedding generated.")
except Exception as e:
    print(f"❌ API Key failed: {e}")
