
import os
from litellm import completion
from dotenv import load_dotenv
import re

load_dotenv()

CONTENT_FILES = [
    r"tests/registration_info.txt",
    r"data/rag qna.txt"
]

OUTPUT_FILE = r"tests/cmcup_questions.txt"

def generate_questions():
    print("🧠 Generating CM Cup Questions using GPT-4o...")
    
    # Read content to inspire questions
    context = ""
    for file_path in CONTENT_FILES:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                context += f.read()[:5000] # Limit to avoid context window issues just in case, though 4o has a lot.
                context += "\n\n"
    
    if not context:
        print("❌ No context found in content files.")
        return

    prompt = f"""
    You are a User Testing Agent. 
    Based on the following information about the Telangana Chief Minister's Cup (CM Cup) and Sports Authority of Telangana (SATS), generate a list of 50 diverse user queries.
    
    Mix of:
    - Short/Simple queries (e.g., "register cm cup")
    - Complex/Long queries (e.g., "how can i register if I am from a village and dont have mobile")
    - Multilingual-style queries (written in English but phrasing might be Indian English)
    - Specific queries about dates, venues, eligibility, fees.
    
    Output ONLY the questions, one per line. No numbering.
    
    Context:
    {context}
    """
    
    try:
        response = completion(
            model="openai/gpt-5.2",
            messages=[{"role": "user", "content": prompt}]
        )
        
        questions_text = response.choices[0].message.content
        
        # Clean up
        questions = []
        for line in questions_text.split("\n"):
            line = line.strip()
            # Remove numbering like "1. " or "- "
            line = re.sub(r"^[\d\-\.\)]+\s*", "", line)
            if line:
                questions.append(line)
        
        # Save
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(questions))
            
        print(f"✅ Generated {len(questions)} questions in {OUTPUT_FILE}")
        
    except Exception as e:
        print(f"❌ Error generating questions: {e}")

if __name__ == "__main__":
    generate_questions()
