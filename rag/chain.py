from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from rag.retriever import get_retriever
from dotenv import load_dotenv
from rag.llm_manager import ask_llm

load_dotenv()

def get_rag_chain():
    # 1. Setup Retriever
    retriever = get_retriever()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def run_orchestrator(input_dict):
        """
        Custom function to run the RAG logic through our LLM Manager (LiteLLM).
        """
        question = input_dict["question"]
        context = input_dict["context"]
        chat_history = input_dict.get("chat_history", [])
        
        # Call the manager which handles:
        # 1. Language Detection
        # 2. System Prompt Selection
        # 3. Model Fallback (Gemini -> OpenAI)
        result = ask_llm(context, question, chat_history=chat_history)
        return result

    # 4. Build Chain
    # Expects input: {"question": "...", "chat_history": [...]}
    def extract_q(x):
        return x["question"]

    chain = (
        {
            "context": RunnableLambda(extract_q) | retriever | format_docs, 
            "question": RunnableLambda(extract_q),
            "chat_history": RunnableLambda(lambda x: x.get("chat_history", []))
        }
        | RunnableLambda(run_orchestrator)
    )

    return chain