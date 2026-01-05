import os
import requests
import json
from langdetect import detect
from dotenv import load_dotenv

load_dotenv()

# Configuration for Exact Models
# User Request: "Gemini 2.5 Flash" and "GPT 5.2" (Pro failed verification)
PRIMARY_MODEL = "gemini-2.5-flash" 
SECONDARY_MODEL = "gpt-5.2"

def get_system_prompt(language: str = "English") -> str:
    """
    Returns the Unified System Prompt.
    The 'language' arg is kept for compatibility but the prompt is largely dynamic or defaults to this master prompt.
    """
    fallback_url = "https://satg.telangana.gov.in/cmcup/"
    
    return f"""You are the Official AI Assistant for the Sports Authority of Telangana (SATG).

    CRITICAL INSTRUCTION - LANGUAGE & SCRIPT MIRRORING:
    1. **Analyze the User's Message** to detect language and script.
    2. **Respond in the EXACT SAME language and script**:
       - **English** -> English
       - **Hindi** (Devanagari) -> Hindi (Devanagari)
       - **Telugu** (Telugu Script) -> Telugu
       - **Hinglish** (Hindi in Roman/English chars) -> **Hinglish** (Roman Hindi).
         - *Example Hinglish Input:* "Kab start hoga?"
         - *Required Hinglish ALL CAPS Response:* "EVENT jald hi SHURU HOGA. Aap WEBSITE check karein."
    
    **OUTPUT FORMAT:**
    - Provide **ONLY** the answer text. 
    - **DO NOT** output JSON, XML, or metadata.
    - **DO NOT** say "Here is the answer in Hinglish". Just give the answer.

    ROLE & TONE:
    - Maintain a FORMAL, PROFESSIONAL, and AUTHORITATIVE tone.
    - Be factual, precise, and direct. 
    - DO NOT use phrases like "According to available documents".
    - DO NOT mention "Context Quality".

    HARD RULES:
    1. **NO GUESSING:** If the answer is not in the Context or Chat History, do not invent it.
    2. **USE CONTEXT & HISTORY:** Answer based on the provided Context and Recent Chat History.
    3. **DIRECT ANSWERS:** Answer the question directly.

    RESPONSE STRATEGY:
    1. **Check History:** Use previous conversation to resolve pronouns (e.g., "it", "he") or answer personal questions (e.g., "What is my name?"). **Priority: HIGH**.
    2. **Analyze Context:** Use the provided context for new facts.
    3. **Website Redirection:** If the context says information is on a website...

    FALLBACK GUIDELINES:
    - **Before falling back**, check if the answer is in the **CHAT HISTORY**. If yes, answer from History.
    - **Type 1: External Source**...
    - **Type 1: External Source** (Context says to check website)
      -> "Yes, you can check for [Topic] on the website under the 'Events' or 'Schedule' section." (Translate this)
    - **Type 2: True Absence** (Context irrelevant)
      -> "I couldn't find specific details about that in the official guidelines. Please check {fallback_url} or contact the helpdesk." (Translate this)
    - **Type 3: Partial Match / Date Mismatch**
      -> "Information for [User's Year] is not available, but for [Available Year]: [Details]..." (Translate this)
    - **Type 4: Out of Scope**
      -> "I am the SATG Sports Assistant. Please ask questions ONLY related to Sports." (Translate this)

    PRIORITY:
    - If you have the answer, give it directly in the User's language.
    - **DETECTED USER LANGUAGE: {language}** -> **YOU MUST RESPOND IN {language.upper()}**.
    """

def detect_language(text: str) -> str:
    try:
        lang_code = detect(text)
        if lang_code == 'hi': return "Hindi"
        elif lang_code == 'te': return "Telugu"
        else: return "English"
    except:
        return "English"

def call_google_api(model, system_prompt, user_query, context, chat_history=[]):
    """
    Direct call to Google Generative Language API
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise Exception("GOOGLE_API_KEY not found")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    # Format History
    history_text = ""
    if chat_history:
        history_text = "\n### RECENT CHAT HISTORY (For Context):\n"
        for role, msg in chat_history:
            history_text += f"{role}: {msg}\n"
        history_text += "\n"

    # Construct prompt
    full_prompt = f"{system_prompt}\n\n{history_text}CONTEXT:\n{context}\n\nUSER QUESTION:\n{user_query}"
    
    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }]
    }
    
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"Google API Error {response.status_code}: {response.text}")
        
    data = response.json()
    try:
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except (KeyError, IndexError):
        raise Exception(f"Unexpected Google Response format: {data}")

def call_openai_api(model, system_prompt, user_query, context, chat_history=[]):
    """
    Direct call to OpenAI API
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY not found")

    url = "https://api.openai.com/v1/chat/completions"
    
    messages = [{"role": "system", "content": f"{system_prompt}\n\nContext:\n{context}"}]
    
    # Inject History
    for role, msg in chat_history:
        # Map 'User'/'AI' to OpenAI roles if needed, or just include as user/assistant
        oai_role = "user" if role == "User" else "assistant"
        messages.append({"role": oai_role, "content": msg})

    messages.append({"role": "user", "content": user_query})
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    
    if response.status_code != 200:
        raise Exception(f"OpenAI API Error {response.status_code}: {response.text}")
        
    data = response.json()
    return data["choices"][0]["message"]["content"]

def ask_llm(context: str, question: str, chat_history: list = [], language: str = None) -> dict:
    """
    Orchestrates the LLM call with manual fallback.
    """
    if not language:
        try:
            language = detect_language(question)
        except:
            language = "English"
        
    system_prompt = get_system_prompt(language)
    
    print(f"DEBUG: Using Primary Model: {PRIMARY_MODEL}")
    
    # 1. Try Primary (Google)
    try:
        answer = call_google_api(PRIMARY_MODEL, system_prompt, question, context, chat_history)
        return {"response": answer, "model_used": PRIMARY_MODEL}
    except Exception as e:
        print(f"[WARN] Primary Model ({PRIMARY_MODEL}) Failed: {str(e)}")
        print(f"DEBUG: Falling back to Secondary Model: {SECONDARY_MODEL}")
        
        # 2. Try Secondary (OpenAI)
        try:
            answer = call_openai_api(SECONDARY_MODEL, system_prompt, question, context, chat_history)
            return {"response": answer, "model_used": SECONDARY_MODEL}
        except Exception as e2:
            print(f"[ERROR] Secondary Model ({SECONDARY_MODEL}) Failed: {str(e2)}")
            return {
                "response": f"I apologize, but I am unable to process your request at the moment due to system connectivity issues. (Primary Err: {str(e)}, Secondary Err: {str(e2)})",
                "model_used": "None"
            }
