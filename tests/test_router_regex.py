
import re

def test_regex():
    # 1. Strong Rule Keywords
    rule_pattern = r"\b(age|born|birth|criteria|rules|limit|eligible|eligibility)\b"
    
    # 2. General SQL Intents
    sql_intent_pattern = r"(how many|count|total|list|show|who is|what is|find).*(player|registration|venue|match|game|sport|cluster|incharge|hockey|cricket|kabaddi|kho|athletics|volleyball|ball|tennis|cycling|wrestling|karate|taekwondo|gymnastics|swimming|yoga|particip)"
    
    queries = [
        "age cretia for hokey",
        "what is the age criteria for hockey",
        "i was born in 2008 suggest disciplines",
        "age limit for kabaddi",
        "eligible sports for 15 year old",
        "show me hockey players",
        "count total players",
        "random chit chat"
    ]
    
    print("--- Testing Router Logic ---")
    for q in queries:
        # Check Rule Pattern
        if re.search(rule_pattern, q, re.IGNORECASE):
            print(f"Query: '{q}' -> ✅ MATCH (Rule Pattern)")
            continue
            
        # Check General Pattern
        if re.search(sql_intent_pattern, q, re.IGNORECASE):
            print(f"Query: '{q}' -> ✅ MATCH (General SQL Pattern)")
            continue
            
        print(f"Query: '{q}' -> ❌ NO MATCH (RAG Fallback)")

if __name__ == "__main__":
    test_regex()
