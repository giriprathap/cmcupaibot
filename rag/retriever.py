from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
import os
from dotenv import load_dotenv

load_dotenv()

def get_retriever():
    # MUST MATCH THE MODEL USED IN INGESTION!
    # Switched to Gemini Embeddings as per user request
    from langchain_google_genai import GoogleGenerativeAIEmbeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    
    client = QdrantClient(path="data/qdrant_db")
    
    # Using a new collection for Gemini to avoid dimension mismatch (OpenAI=1536, Gemini=768)
    vector_store = QdrantVectorStore(
        client=client,
        collection_name="rag_knowledge_base_gemini",
        embedding=embeddings,
    )
    
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 10}
    )