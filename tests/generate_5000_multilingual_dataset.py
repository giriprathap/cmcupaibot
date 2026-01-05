import os
import re
import json
import random

DATA_DIR = "data/mdFiles"
OUTPUT_FILE = "data/dataset_5000_multilingual.json"
EXCLUSION_FILES = [
    "data/rag qna.txt", 
    "data/training_questions_500.txt"
]
TARGET_COUNT = 5000

questions = []
seen = set()  # Track uniqueness

def normalize_text(text):
    """Normalize text for comparison (lowercase, strip non-alphanumeric)."""
    return re.sub(r'[^a-z0-9]', '', text.lower())

def load_exclusions():
    """Load existing questions to exclude."""
    count = 0
    for file_path in EXCLUSION_FILES:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Extract lines starting with numbers like "1. Question?"
                    # Adjust regex to catch more formats if needed
                    matches = re.findall(r'^\d+\.\s+(.*)$', content, re.MULTILINE)
                    for m in matches:
                        seen.add(normalize_text(m))
                        count += 1
            except Exception as e:
                print(f"⚠️ Error reading {file_path}: {e}")
    print(f"🚫 Loaded {count} existing questions to exclude.")

def add_unique_q(topic, text, language):
    """Add question only if unique."""
    norm_text = normalize_text(text)
    if norm_text not in seen:
        seen.add(norm_text)
        questions.append({
            "id": len(questions) + 1,
            "topic": topic,
            "question": text,
            "language": language
        })
        return True
    return False

print("📂 Loading Data Files...")

# Load Entities - REMOVED SLICING LIMITS to ensure we have enough data
districts = []
mandals = []
villages = []
fixtures = []
events = []

# Read Districts
if os.path.exists(os.path.join(DATA_DIR, "rag_districts.md")):
    with open(os.path.join(DATA_DIR, "rag_districts.md"), "r", encoding="utf-8") as f:
        content = f.read()
        districts = re.findall(r'District \*\*(.*?)\*\*', content)

# Read Mandals
if os.path.exists(os.path.join(DATA_DIR, "rag_mandals.md")):
    with open(os.path.join(DATA_DIR, "rag_mandals.md"), "r", encoding="utf-8") as f:
        content = f.read()
        mandals = re.findall(r'Mandal \*\*(.*?)\*\*', content)

# Read Villages
if os.path.exists(os.path.join(DATA_DIR, "rag_villages.md")):
    with open(os.path.join(DATA_DIR, "rag_villages.md"), "r", encoding="utf-8") as f:
        content = f.read()
        villages = re.findall(r'\*\*(.*?)\*\*', content) # Removed [:500] limit

# Read Fixtures
if os.path.exists(os.path.join(DATA_DIR, "rag_fixtures.md")):
    with open(os.path.join(DATA_DIR, "rag_fixtures.md"), "r", encoding="utf-8") as f:
        content = f.read()
        fixtures = re.findall(r'Fixture ID: (\d+)', content)

# Read Events/Disciplines
if os.path.exists(os.path.join(DATA_DIR, "rag_disciplines.md")):
    with open(os.path.join(DATA_DIR, "rag_disciplines.md"), "r", encoding="utf-8") as f:
        content = f.read()
        events = re.findall(r'\*\*(.*?)\*\*', content) # Removed [:20] limit

# Fallback disciplines
if not events:
    events = ["Athletics", "Badminton", "Basketball", "Boxing", "Football", 
              "Swimming", "Kabaddi", "Kho-Kho", "Volleyball", "Wrestling"]

print(f"   Loaded: {len(districts)} districts, {len(mandals)} mandals, "
      f"{len(villages)} villages, {len(fixtures)} fixtures, {len(events)} events")

load_exclusions()

# Question Templates
# Format: (topic, templates_dict_by_language)
templates = [
    # Location-based
    ("Locations", {
        "English": [
            "Is {entity} a registered district?",
            "Show me details for {entity}.",
            "Which district does {entity} belong to?",
            "Tell me about {entity}.",
            "Information on {entity} district.",
            "Is {entity} part of the CM Cup?",
            "Where is {entity} located?",
            "Give me info on {entity}.",
            "Can you find {entity}?",
            "What do you know about {entity}?",
            "Does {entity} participate in sports?"
        ],
        "Hindi": [
            "{entity} ek registered district hai kya?",
            "Mujhe {entity} ke baare mein batao.",
            "{entity} kis district mein hai?",
            "{entity} ke baare mein jankari do.",
            "{entity} district ki details dikhao.",
            "Kya {entity} CM Cup ka hissa hai?",
            "{entity} kahan hai?",
            "{entity} ki location batao.",
            "{entity} ke baare mein kya jante ho?",
            "Kya {entity} sports mein hai?"
        ],
        "Telugu": [
            "{entity} registered district aa?",
            "{entity} gurinchi cheppandi.",
            "{entity} e district lo undi?",
            "{entity} vishayam cheppandi.",
            "{entity} details ivvandi.",
            "{entity} ekkada undi?",
            "{entity} gurinchi em telusu?",
            "{entity} sports lo undo ledo?"
        ],
        "Hinglish": [
            "{entity} registered district hai kya?",
            "Mujhe {entity} ke details chahiye.",
            "{entity} kis district ka part hai?",
            "{entity} ke bare me info do.",
            "Tell me about {entity} na.",
            "{entity} kahan located hai?",
            "{entity} ki jankari de do bhai.",
            "Kya {entity} CM Cup mein hai?"
        ]
    }),
    # Fixtures
    ("Fixtures", {
        "English": [
            "Who is playing in Fixture ID {entity}?",
            "When is Match ID {entity} scheduled?",
            "Details for Fixture {entity}.",
            "Show me Match {entity} info.",
            "What time is Fixture {entity}?",
            "Where is Match {entity} being played?",
            "Is Fixture {entity} cancelled?"
        ],
        "Hindi": [
            "Fixture ID {entity} mein kaun khel raha hai?",
            "Match ID {entity} kab scheduled hai?",
            "Fixture {entity} ki details do.",
            "Match {entity} ki jankari dikhao.",
            "Fixture {entity} ka time kya hai?",
            "Kya Match {entity} cancel ho gaya?"
        ],
        "Telugu": [
            "Fixture ID {entity} lo evaru aadutunnaru?",
            "Match ID {entity} eppudu schedule ayyindi?",
            "Fixture {entity} details ivvandi.",
            "Match {entity} gurinchi cheppandi.",
            "Fixture {entity} time enti?"
        ],
        "Hinglish": [
            "Fixture ID {entity} me kaun play kar raha hai?",
            "Match {entity} kab hai?",
            "Fixture {entity} ke details dikhao.",
            "Match {entity} ka info chahiye.",
            "Fixture {entity} kitne baje hai?"
        ]
    }),
    # Events/Sports
    ("Events", {
        "English": [
            "List all events for {entity}.",
            "What is the schedule for {entity}?",
            "Are there any {entity} matches today?",
            "Venue for {entity} matches?",
            "When does {entity} start?",
            "Show me {entity} fixtures.",
            "Tell me about {entity} competitions.",
            "Is {entity} included in CM Cup?",
            "How to register for {entity}?"
        ],
        "Hindi": [
            "{entity} ke liye sabhi events list karo.",
            "{entity} ka schedule kya hai?",
            "Kya aaj {entity} ke matches hain?",
            "{entity} matches ka venue kya hai?",
            "{entity} kab shuru hoga?",
            "{entity} fixtures dikhao.",
            "{entity} ke register kaise karein?"
        ],
        "Telugu": [
            "{entity} kosam anni events list cheyandi.",
            "{entity} schedule enti?",
            "Ee roju {entity} matches unnaya?",
            "{entity} matches venue enti?",
            "{entity} eppudu modalaavutundi?",
            "{entity} fixtures chupinchandi."
        ],
        "Hinglish": [
            "{entity} ke liye all events batao.",
            "{entity} ka schedule kya hai?",
            "Aaj {entity} matches hai kya?",
            "{entity} matches kahan hain?",
            "{entity} kab start hoga?",
            "{entity} me register kaise karte hain?"
        ]
    })
]

# General/Policy questions (no entity substitution)
# These will be mutated with iteration numbers if needed, but we have enough entities now.
general_qs = [
    ("Policy", {
        "English": [
            "What is the cash award for Olympic Gold?",
            "What is the vision for 2025?",
            "Incentives for coaches?",
            "Reservation policy for athletes?",
            "Travel allowance rules?",
            "Who is the CM of Telangana?",
            "Registration process for CM Cup?",
            "Contact number for helpdesk?",
            "What are the eligibility criteria?",
            "Budget for infrastructure?"
        ],
        "Hindi": [
            "Olympic Gold ke liye cash award kya hai?",
            "2025 ka vision kya hai?",
            "Coaches ke liye incentives kya hain?",
            "Athletes ke liye reservation policy kya hai?",
            "Travel allowance ke niyam kya hain?",
            "Telangana ke CM kaun hain?",
            "CM Cup ke liye registration kaise karein?",
            "Helpdesk ka contact number kya hai?"
        ],
        "Telugu": [
            "Olympic Gold kosam cash award enti?",
            "2025 vision enti?",
            "Coaches kosam incentives entavi?",
            "Athletes kosam reservation policy enti?",
            "Travel allowance niyamalu entavi?",
            "Telangana CM evaru?",
            "CM Cup registration ela cheyali?",
            "Helpdesk contact number enti?"
        ],
        "Hinglish": [
            "Olympic Gold ka cash award kya hai?",
            "2025 vision kya hai?",
            "Coaches ko kya incentives hain?",
            "Athletes ke liye reservation policy?",
            "Travel allowance rules kya hain?",
            "Telangana CM kaun hai?",
            "CM Cup registration kaise kare?"
        ]
    })
]

print("🔄 Generating Questions...")

# Generate entity-based questions
for topic, lang_templates in templates:
    if topic == "Locations":
        # Combine all location entities
        entities = districts + mandals + villages
        random.shuffle(entities) # Shuffle to get variety
    elif topic == "Fixtures":
        entities = fixtures
        random.shuffle(entities)
    elif topic == "Events":
        entities = events
        random.shuffle(entities)
    else:
        entities = []
    
    # We want to distribute questions across languages and entities
    for entity in entities:
        # Pick 2 random languages per entity to avoid exhaustion
        langs = ["English", "Hindi", "Telugu", "Hinglish"]
        selected_langs = random.sample(langs, k=2) 
        
        for lang in selected_langs:
            # Pick a random template
            template = random.choice(lang_templates[lang])
            q_text = template.replace("{entity}", str(entity))
            add_unique_q(topic, q_text, lang)
            
            if len(questions) >= TARGET_COUNT:
                break
        if len(questions) >= TARGET_COUNT:
            break
    if len(questions) >= TARGET_COUNT:
        break

# Fill remaining with General questions if needed
if len(questions) < TARGET_COUNT:
    print(f"   Note: Entity questions exhausted at {len(questions)}. Filling with General questions...")
    iteration = 0
    while len(questions) < TARGET_COUNT:
        iteration += 1
        for topic, lang_qs in general_qs:
            for lang in ["English", "Hindi", "Telugu", "Hinglish"]:
                for q_base in lang_qs[lang]:
                    q_text = q_base
                    if iteration > 1:
                        # Add a minimal variation to make it unique string-wise
                        # e.g., append spaces or punctuation variants, but here just suffix is safer
                        q_text = f"{q_base} " + ("?" * (iteration % 3)) 
                    add_unique_q(topic, q_text, lang)
                    if len(questions) >= TARGET_COUNT:
                        break
                if len(questions) >= TARGET_COUNT:
                    break
            if len(questions) >= TARGET_COUNT:
                break
        if len(questions) >= TARGET_COUNT:
            break

# Shuffle final dataset
random.shuffle(questions)
questions = questions[:TARGET_COUNT]

# Renumber IDs
for i, q in enumerate(questions):
    q["id"] = i + 1

print(f"✅ Generated {len(questions)} unique questions.")
print(f"   Unique count (including exclusions): {len(seen)}")

# Language distribution
lang_counts = {}
for q in questions:
    lang_ = q["language"]
    lang_counts[lang_] = lang_counts.get(lang_, 0) + 1

print("   Language Distribution:")
for lang_, count in sorted(lang_counts.items()):
    print(f"      {lang_}: {count} ({count/len(questions)*100:.1f}%)")

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, indent=2, ensure_ascii=False)

print(f"💾 Saved to {OUTPUT_FILE}")
