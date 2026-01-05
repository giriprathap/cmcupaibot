import sys
import os
import re
import uuid
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# --------------------------------------------------
# 1. Ensure Python can find project root (Render-safe)
# --------------------------------------------------
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

# --------------------------------------------------
# 2. Imports
# --------------------------------------------------
from rag.chain import get_rag_chain
from rag.sql_queries import get_fixture_details, get_geo_details, get_sport_schedule, get_player_venues_by_phone, get_player_venue_by_ack
# Also importing get_player_by_phone from lookup (which uses SQL now)
# rag.lookup imports removed as per privacy policy
from rag.sql_agent import run_sql_agent

# --------------------------------------------------
# 3. Initialize FastAPI App
# --------------------------------------------------
app = FastAPI(
    title="SATG Sports Chatbot API",
    description="Hybrid RAG + SQL Engine for Player Stats & Rules",
    version="1.1.0"
)

# Mount Static Files (Demo UI)
app.mount("/demo", StaticFiles(directory="static", html=True), name="static")

# 4. Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# 5. Models and Globals
# --------------------------------------------------
class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None  # Added for memory

class WhatsAppChatRequest(BaseModel):
    user_message: str
    first_name: Optional[str] = None
    phone_number: Optional[str] = None

# Global RAG Cache (Lazy Loaded)
rag_chain = None

# In-Memory Chat History: {session_id: [(user, bot), ...]}
CHAT_SESSIONS = {}

# MENU STATE MANAGEMENT
SESSION_STATE = {} # {session_id: current_state_str}
SESSION_DATA = {} # {session_id: {key: val}}

# MENU CONSTANTS
MENU_MAIN = "MAIN_MENU"
MENU_REG_ELIGIBILITY = "MENU_REG_ELIGIBILITY"
MENU_SPORTS_MATCHES = "MENU_SPORTS_MATCHES"
MENU_VENUES_OFFICIALS = "MENU_VENUES_OFFICIALS"
MENU_PLAYER_STATUS = "MENU_PLAYER_STATUS"
MENU_HELP_LANGUAGE = "MENU_HELP_LANGUAGE"
MENU_SCHEDULE_OPTIONS = "MENU_SCHEDULE_OPTIONS"

# SUB-MENUS / STATES
MENU_DISCIPLINES = "MENU_DISCIPLINES" # Reused for Level Selection
MENU_LANGUAGE = "MENU_LANGUAGE"       # Reused for Language Selection

# SUB-INTERACTION STATES (Waiting for input)
STATE_WAIT_PHONE = "STATE_WAIT_PHONE"
STATE_WAIT_ACK = "STATE_WAIT_ACK"
STATE_WAIT_LOCATION = "STATE_WAIT_LOCATION"
STATE_WAIT_SPORT_SCHEDULE = "STATE_WAIT_SPORT_SCHEDULE"
STATE_WAIT_SPORT_RULES = "STATE_WAIT_SPORT_RULES"
STATE_WAIT_SPORT_AGE = "STATE_WAIT_SPORT_AGE"
STATE_WAIT_OFFICER_LOC = "STATE_WAIT_OFFICER_LOC" 

# Additional Develop Constants (Preserved for compatibility)
MENU_SELECT_SPORT = "MENU_SELECT_SPORT"
MENU_GAME_OPTIONS = "MENU_GAME_OPTIONS"
MENU_SCHEDULE_GAME_SEARCH = "MENU_SCHEDULE_GAME_SEARCH"

PARENT_MAP = {
    MENU_REG_ELIGIBILITY: MENU_MAIN,
    MENU_SPORTS_MATCHES: MENU_MAIN,
    MENU_VENUES_OFFICIALS: MENU_MAIN,
    MENU_PLAYER_STATUS: MENU_MAIN,
    MENU_HELP_LANGUAGE: MENU_MAIN,
    
    MENU_DISCIPLINES: MENU_SPORTS_MATCHES,
    MENU_SCHEDULE_OPTIONS: MENU_SPORTS_MATCHES,
    MENU_LANGUAGE: MENU_HELP_LANGUAGE,
    
    # Sub-states
    STATE_WAIT_PHONE: MENU_PLAYER_STATUS,
    STATE_WAIT_ACK: MENU_PLAYER_STATUS,
    STATE_WAIT_LOCATION: MENU_VENUES_OFFICIALS,
    STATE_WAIT_OFFICER_LOC: MENU_VENUES_OFFICIALS,
    STATE_WAIT_SPORT_SCHEDULE: MENU_SCHEDULE_OPTIONS,
    STATE_WAIT_SPORT_RULES: MENU_REG_ELIGIBILITY,
    STATE_WAIT_SPORT_AGE: MENU_REG_ELIGIBILITY,
    
    # Enable Develop Logic
    MENU_SELECT_SPORT: MENU_DISCIPLINES,
    MENU_GAME_OPTIONS: MENU_SELECT_SPORT,
    MENU_SCHEDULE_GAME_SEARCH: MENU_SPORTS_MATCHES, 
}


def get_or_init_rag_chain():
    """
    Lazy-load RAG chain.
    This prevents Render startup timeout.
    """
    global rag_chain
    if rag_chain is None:
        print("[INFO] Initializing RAG chain (lazy)...")
        rag_chain = get_rag_chain()
        print("✅ RAG chain initialized")
    return rag_chain

# --------------------------------------------------
# 6. Helpers & Menu Content
# --------------------------------------------------
# --- HELPER: Cluster Search ---
# --- HELPER: Cluster Search ---
import difflib

def search_cluster_incharge(user_query):
    """
    Searches for the cluster name using fuzzy matching.
    """
    try:
        file_path = "data/new data/Mandal_Incharges_Cleaned.txt"
        if not os.path.exists(file_path):
            return "⚠️ Data file not found."
            
        target = user_query.strip().lower()
        results = []
        
        # 1. Collect all valid clusters and their full lines
        cluster_map = {} # {cluster_lower: [line1, line2]}
        
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if "Cluster:" in line:
                    # Parse: Mandal: ... | Cluster: XYZ | ...
                    parts = line.split("|")
                    if len(parts) >= 2:
                        # Extract " Cluster: XYZ " -> "XYZ"
                        c_raw = parts[1].split(":")[1].strip()
                        c_lower = c_raw.lower()
                        
                        if c_lower not in cluster_map:
                            cluster_map[c_lower] = []
                        cluster_map[c_lower].append(line.strip())
        
        # 2. Exact Match Check
        if target in cluster_map:
            results = cluster_map[target]
            found_name = target
        else:
            # 3. Partial/Substring Match (if target > 3 chars)
            if len(target) > 3:
                for c_name in cluster_map:
                    if target in c_name: # target "Akine" in "Akinepalli"
                        results = cluster_map[c_name]
                        found_name = c_name
                        break
            
            # 4. Fuzzy Match (if no exact or partial match)
            if not results:
                all_clusters = list(cluster_map.keys())
                matches = difflib.get_close_matches(target, all_clusters, n=1, cutoff=0.55) # Lowered slightly to 0.55
                
                if matches:
                    found_name = matches[0]
                    results = cluster_map[found_name]
                else:
                    return None

        # 5. Format Output
        if results:
            # Capitalize the found name for display
            display_name = found_name.title() 
            response = f"**Found In-Charge Details for '{display_name}':**\n\n"
            for res in results[:5]: 
                response += f"🔹 {res}\n"
            return response
            
        return None

    except Exception as e:
        return f"Error searching data: {str(e)}"

# --- MENU TEXT HELPERS ---
def get_menu_text(menu_name):
    if menu_name == MENU_MAIN:
        return (
            "🏆 **Welcome to Telangana Sports Authority – CM Cup 2025**\n\n"
            "1️⃣ Registration & Eligibility 📝\n"
            "2️⃣ Sports & Matches 🏅\n"
            "3️⃣ Venues & Officials 🏟️\n"
            "4️⃣ Player Status 🔍\n"
            "5️⃣ Help & Language 📞\n\n"
            "💡 *Type a number (1–5) to proceed*"
        )
    elif menu_name == MENU_REG_ELIGIBILITY:
        return (
            "📝 **Registration & Eligibility**\n\n"
            "1️⃣ How to Register\n"
            "2️⃣ Eligibility Rules (Age/Criteria)\n"
            "3️⃣ Documents Required\n"
            "4️⃣ Registration Status (Check Info)\n"
            "5️⃣ FAQs\n\n"
            "🔙 *Type 'Back' for Main Menu*"
        )
    elif menu_name == MENU_SPORTS_MATCHES:
        return (
            "🏅 **Sports & Matches**\n\n"
            "1️⃣ Sports Disciplines (By Level)\n"
            "2️⃣ Schedules & Fixtures\n"
            "3️⃣ Medal Tally\n\n"
            "🔙 *Type 'Back' for Main Menu*"
        )
    elif menu_name == MENU_VENUES_OFFICIALS:
        return (
            "🏟️ **Venues & Officials**\n\n"
            "1️⃣ District Officers / Venue In-Charge\n"
            "2️⃣ Venue In-Charge (Cluster/Mandal)\n"
            "\n(Venues details ignored as per instruction)\n"
            "🔙 *Type 'Back' for Main Menu*"
        )
    elif menu_name == MENU_PLAYER_STATUS:
        return (
            "🔍 **Player Status**\n\n"
            "1️⃣ Search by Phone No\n"
            "2️⃣ Search by Acknowledgment No\n\n"
            "🔙 *Type 'Back' for Main Menu*"
        )
    elif menu_name == MENU_HELP_LANGUAGE:
        return (
            "📞 **Help & Language**\n\n"
            "1️⃣ Helpline Numbers\n"
            "2️⃣ Email Support\n"
            "3️⃣ Change Language\n\n"
            "🔙 *Type 'Back' for Main Menu*"
        )
    elif menu_name == MENU_LANGUAGE:
        return (
            "🌐 **Select Language**\n\n"
            "1️⃣ English\n"
            "2️⃣ తెలుగు (Telugu)\n"
            "3️⃣ हिन्दी (Hindi)\n\n"
            "🔙 *Type 'Back' for Previous Menu*"
        )
    elif menu_name == MENU_DISCIPLINES:
        return (
            "📅 **Disciplines - Select Level**\n\n"
            "1️⃣ Gram Panchayat / Cluster Level\n"
            "2️⃣ Mandal Level\n"
            "3️⃣ Assembly Constituency Level\n"
            "4️⃣ District Level\n"
            "5️⃣ State Level\n\n"
            "🔙 *Type 'Back' for Previous Menu*"
        )
    elif menu_name == MENU_SCHEDULE_OPTIONS:
        return (
            "📅 **Schedules & Fixtures**\n\n"
            "1️⃣ Tournament Schedules 🗓️\n"
            "2️⃣ Games Schedules 🏅\n\n"
            "🔙 *Type 'Back' for Previous Menu*"
        )

    return "Menu not found."

def extract_plain_text(resp) -> str:
    """Try to extract a single answer string from various response shapes."""
    if resp is None:
        return ""
    
    # If it's a dict, extract text from it
    if isinstance(resp, dict):
        return _extract_from_dict(resp)
        
    # If it's a list/tuple, extract from first item
    if isinstance(resp, (list, tuple)):
        return _extract_from_list(resp)

    # Convert to string
    s = str(resp).strip()
    
    # RECURSIVE PARSING: If the string ITSELF looks like a JSON dict, parse it!
    # Check for both standard JSON {"key": "val"} and Python Dict {'key': 'val'}
    if (s.startswith("{") and s.endswith("}")):
        # 1. Try JSON
        try:
            import json
            parsed = json.loads(s)
            # Recursively extract from the parsed dict
            return extract_plain_text(parsed)
        except:
            # 2. Try Python Literal (for single quotes)
            try:
                import ast
                parsed = ast.literal_eval(s)
                if isinstance(parsed, dict):
                    return extract_plain_text(parsed)
            except:
                pass
                
    return s

def _extract_from_dict(d: dict) -> str:
    # Preferred scalar keys
    for key in ("response", "answer", "text", "content", "message", "output", "result"):
        v = d.get(key)
        # If we find a value, we must potentially UNWRAP it again if it's a JSON string
        if v:
            return extract_plain_text(v)
            
    for key in ("choices", "outputs", "results"):
        if key in d:
            return extract_plain_text(d[key])
            
    # Heuristic: return the first string value found
    for v in d.values():
        candidate = extract_plain_text(v)
        if candidate and candidate != "None" and len(candidate) > 0:
            return candidate
    return ""

def _extract_from_list(lst) -> str:
    for item in lst:
        candidate = extract_plain_text(item)
        if candidate:
            return candidate
    try:
        return " ".join([str(x) for x in lst])
    except Exception:
        return ""

# --------------------------------------------------
# 7. Health Check
# --------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "SATG Chatbot Engine is Running 🚀"
    }

# --------------------------------------------------
# 8. Main Chat Endpoint (Hybrid Router)
# --------------------------------------------------
async def process_user_query(raw_query: str, session_id: str = None):
    """
    Unified Logic Handler: Menu -> SQL -> RAG
    """
    user_query = raw_query.strip().lower()
    # session_id passed as argument
    
    # ------------------------------------------------
    # 0. MENU STATE MACHINE
    # ------------------------------------------------
    
    # Global Reset Commands
    if user_query in ["hi", "hello", "menu", "start", "restart", "home"]:
        if session_id:
            SESSION_STATE[session_id] = MENU_MAIN
        return {"response": get_menu_text(MENU_MAIN), "source": "menu_system"}
        
    # Get Current State
    current_state = SESSION_STATE.get(session_id, MENU_MAIN) if session_id else MENU_MAIN
    
    # Global Back Command
    if user_query in ["back", "previous", "return", "exit"]:
        # Logic to return to parent
        if current_state == MENU_MAIN:
            return {"response": "You are already at the Main Menu.", "source": "menu_system"}
        else:
            # Look up parent
            parent = PARENT_MAP.get(current_state, MENU_MAIN)
            if session_id:
                SESSION_STATE[session_id] = parent
            return {"response": get_menu_text(parent), "source": "menu_system"}

    # State: WAITING FOR INPUT (Phone, Ack, Location)
    # If we are in a 'waiting' state, we treat the query as the input value
    if current_state == STATE_WAIT_PHONE:
        # Check if it looks like a phone number
        if re.search(r'\b[6-9]\d{9}\b', user_query):
            # Direct Lookup Logic
            phone = re.search(r'\b[6-9]\d{9}\b', user_query).group(0)
            print(f"⚡ Intent: Menu Phone Lookup ({phone})")
            
            # Reset state
            if session_id: SESSION_STATE[session_id] = MENU_REGISTRATION
            
            # SQL Lookup
            registrations = get_player_venues_by_phone(phone)
            
            if not registrations:
                 return {"response": f"ℹ️ No registrations found for **{phone}**. Please check the number or register at the official site.", "source": "sql_database"}
            
            # Logic: 1 Record vs Multi
            if len(registrations) == 1:
                rec = registrations[0]
                venue = rec.get('venue')
                sport = rec.get('sport_name') or rec.get('event_name')
                
                txt = f"### 🏟️ Venue Details for {sport}\n"
                if venue:
                    txt += f"**Venue:** {venue}\n"
                    txt += f"**Date:** {rec.get('match_date') or 'Check Schedule'}\n"
                else:
                    txt += "**Status:** There are no Venue Details available yet.\n"
                    txt += f"You can contact your cluster Incharge:\n"
                    txt += f"👤 **{rec.get('cluster_incharge', 'N/A')}**\n"
                    txt += f"📞 **{rec.get('incharge_mobile', 'N/A')}**\n"
                
                return {"response": txt, "source": "sql_database"}
                
            else:
                # Multiple Records
                txt = f"found **{len(registrations)} registrations** for this number:\n"
                for r in registrations:
                    s = r.get('sport_name') or r.get('event_name')
                    txt += f"- {s}\n"
                
                txt += "\nSince you have multiple events, please provide your **Acknowledgment Number** (e.g., SATGCMC-...) to get specific venue details."
                return {"response": txt, "source": "sql_database"} 
        else:
             return {"response": "❌ Invalid Phone Number. Please enter a 10-digit mobile number starting with 6-9.\n\nType 'Back' to cancel.", "source": "validation_error"}

    # --- MENU NAVIGATION (DIGIT INPUTS) --------------------------------
    if user_query.isdigit():
        choice = int(user_query)
        
        # --- MAIN MENU ---
        if current_state == MENU_MAIN:
            if choice == 1:
                if session_id: SESSION_STATE[session_id] = MENU_REG_ELIGIBILITY
                return {"response": get_menu_text(MENU_REG_ELIGIBILITY), "source": "menu_system"}
            elif choice == 2:
                if session_id: SESSION_STATE[session_id] = MENU_SPORTS_MATCHES
                return {"response": get_menu_text(MENU_SPORTS_MATCHES), "source": "menu_system"}
            elif choice == 3:
                if session_id: SESSION_STATE[session_id] = MENU_VENUES_OFFICIALS
                return {"response": get_menu_text(MENU_VENUES_OFFICIALS), "source": "menu_system"}
            elif choice == 4:
                if session_id: SESSION_STATE[session_id] = MENU_PLAYER_STATUS
                return {"response": get_menu_text(MENU_PLAYER_STATUS), "source": "menu_system"}
            elif choice == 5:
                if session_id: SESSION_STATE[session_id] = MENU_HELP_LANGUAGE
                return {"response": get_menu_text(MENU_HELP_LANGUAGE), "source": "menu_system"}
            else:
                 return {"response": "❌ Invalid Option. Please select 1-5.", "source": "menu_system"}

        # --- 1. REGISTRATION & ELIGIBILITY ---
        elif current_state == MENU_REG_ELIGIBILITY:
            if choice == 1: # How to Register
                return {"response": "📝 **How to Register:**\n\n1. Visit [satg.telangana.gov.in/cmcup](https://satg.telangana.gov.in/cmcup)\n2. Click 'Player Registration'\n3. Fill details & Upload Aadhaar/Photo\n4. Submit & Download Ack Slip.\n\n🔙 *Type 'Back' for Menu*", "source": "static_answer"}
            elif choice == 2: # Eligibility Rules
                if session_id: SESSION_STATE[session_id] = STATE_WAIT_SPORT_AGE
                return {"response": "🎂 **Eligibility Check:**\n\nWhich **Sport** would you like to check? (e.g. Kabaddi, Athletics)", "source": "menu_system"}
            elif choice == 3: # Documents
                return {"response": "📄 **Documents Required:**\n\n• Aadhaar Card\n• Date of Birth Proof (SSC/Birth Cert)\n• Bonafide Certificate\n• Passport Photo\n• Bank Passbook (if applicable)\n\n🔙 *Type 'Back' for Menu*", "source": "static_answer"}
            elif choice == 4: # Registration Status
                return {"response": "ℹ️ **Registration Status:**\n\nYou can check your status in the **Player Status** menu (Option 4 on Main Menu) using your Phone Number or Acknowledgment ID.\n\nWould you like to go there now? (Type 'Back' then '4')", "source": "static_answer"}
            elif choice == 5: # FAQs
                return {"response": "❓ **FAQs:**\n\n• **Is it free?** Yes.\n• **Can I play multiple sports?** Yes, if schedules don't clash.\n• **Who can apply?** Residents of Telangana within age limits.\n\n🔙 *Type 'Back' for Menu*", "source": "static_answer"}
        
        # --- 2. SPORTS & MATCHES ---
        elif current_state == MENU_SPORTS_MATCHES:
            if choice == 1: # Disciplines
                if session_id: SESSION_STATE[session_id] = MENU_DISCIPLINES
                return {"response": get_menu_text(MENU_DISCIPLINES), "source": "menu_system"}
            elif choice == 2: # Schedules
                if session_id: SESSION_STATE[session_id] = MENU_SCHEDULE_OPTIONS
                return {"response": get_menu_text(MENU_SCHEDULE_OPTIONS), "source": "menu_system"}
            elif choice == 3: # Medal Tally
                return {"response": "🥇 **Medal Tally:**\n\nThe CM Cup 2025 has not started yet. Tally will be updated live during the State Level games in Feb 2025.", "source": "static_answer"}

        # --- 3. VENUES & OFFICIALS ---
        elif current_state == MENU_VENUES_OFFICIALS:
            if choice == 1 or choice == 2: # Officers / In-Charge
                if session_id: SESSION_STATE[session_id] = STATE_WAIT_OFFICER_LOC
                return {"response": "👮 **Find Officers / In-Charge:**\n\nPlease enter your **Mandal** or **District** name.", "source": "menu_system"}

        # --- 4. PLAYER STATUS ---
        elif current_state == MENU_PLAYER_STATUS:
            if choice == 1: # Phone
                if session_id: SESSION_STATE[session_id] = STATE_WAIT_PHONE
                return {"response": "📞 Please enter your registered **Phone Number** (10 digits):", "source": "menu_system"}
            elif choice == 2: # Ack No
                if session_id: SESSION_STATE[session_id] = STATE_WAIT_ACK
                return {"response": "🆔 Please enter your **Acknowledgment Number** (e.g. SATGCMC-12345):", "source": "menu_system"}

        # --- 5. HELP & LANGUAGE ---
        elif current_state == MENU_HELP_LANGUAGE:
            if choice == 1: # Helpline
                return {"response": "📞 **Helpline Numbers:**\n\n• State Control Room: 040-12345678\n• Technical Support: 1800-999-9999\n\n(Available 10 AM - 6 PM)", "source": "static_answer"}
            elif choice == 2: # Email
                return {"response": "📧 **Email Support:**\n\n• General Queries: help@telanganasports.gov.in\n• Technical Issues: techsupport@satg.in", "source": "static_answer"}
            elif choice == 3: # Language
                if session_id: SESSION_STATE[session_id] = MENU_LANGUAGE
                return {"response": get_menu_text(MENU_LANGUAGE), "source": "menu_system"}
        
        # --- SUB MENU: SCHEDULES ---
        elif current_state == MENU_SCHEDULE_OPTIONS:
            if choice == 1: # Tournament Schedules
                 return {
                     "response": (
                         "🗓️ **Tournament Schedules (CM Cup 2025)**\n\n"
                         "• **Mandal Level**: Jan 15 - Jan 17\n"
                         "• **Assembly Level**: Jan 20 - Jan 22\n"
                         "• **District Level**: Jan 28 - Jan 30\n"
                         "• **State Level**: Feb 10 - Feb 15\n\n"
                         "🔗 [Click here for detailed PDF](https://satg.telangana.gov.in/cmcup/schedule)\n\n"
                         "🔙 *Type 'Back' for Menu*"
                     ),
                     "source": "static_answer"
                 }
            elif choice == 2: # Games Schedules
                 if session_id: SESSION_STATE[session_id] = STATE_WAIT_SPORT_SCHEDULE
                 return {"response": "🏅 **Games Schedules:**\n\nWhich sport are you looking for? (e.g. Volleyball, Kho-Kho)", "source": "menu_system"}

        # --- SUB MENU: DISCIPLINES (LEVEL Selection) ---
        elif current_state == MENU_DISCIPLINES:
            level_map = {1: "cluster", 2: "mandal", 3: "assembly", 4: "district", 5: "state"}
            if choice in level_map:
                level_name = level_map[choice]
                try:
                    from rag.sql_queries import get_disciplines_by_level
                    games = get_disciplines_by_level(level_name)
                    
                    # Display titles mapping
                    titles = {
                        "cluster": "Cluster / Gram Panchayat Level",
                        "mandal": "Mandal Level",
                        "assembly": "Assembly Constituency Level",
                        "district": "District Level",
                        "state": "State Level"
                    }
                    display_title = titles.get(level_name, level_name.title() + " Level")

                    if games:
                        # Store in Session Data
                        if session_id:
                            SESSION_STATE[session_id] = MENU_SELECT_SPORT
                            SESSION_DATA[session_id] = {"sports": games, "level_title": display_title}

                        txt = f"### 🏅 Sports at {display_title}\n\n"
                        for i, g in enumerate(games, 1):
                            txt += f"{i}. {g}\n"
                        txt += "\nℹ️ *Select a number to view details (Age, Events, Rules)*"
                        return {"response": txt, "source": "sql_database"}
                    else:
                         return {"response": f"ℹ️ No sports found specifically for **{display_title}** in the database.", "source": "sql_database"}
                except Exception as e:
                    print(f"Error fetching disciplines: {e}")
                    return {"response": "❌ An error occurred while fetching disciplines. Please try again.", "source": "error_handler"}

        # --- SUB MENU: SELECT SPORT (Drill Down) ---
        elif current_state == MENU_SELECT_SPORT:
            data = SESSION_DATA.get(session_id, {})
            sports = data.get("sports", [])
            
            # 1. Try Numeric Selection
            selected_sport = None
            if choice and 1 <= choice <= len(sports):
                selected_sport = sports[choice - 1]
            
            # 2. Try Text Selection (Fuzzy-ish)
            if not selected_sport:
                # normalize query
                q_norm = user_query.strip().lower()
                for s in sports:
                    if s.lower() == q_norm or s.lower() in q_norm:
                        selected_sport = s
                        break
            
            if selected_sport:
                # Store selected sport
                if session_id:
                     SESSION_STATE[session_id] = MENU_GAME_OPTIONS
                     SESSION_DATA[session_id]["selected_sport"] = selected_sport
                
                return {
                    "response": (
                        f"🏅 **{selected_sport}** - Options\n\n"
                        "1️⃣ Age Criteria\n"
                        "2️⃣ Events of the Game\n"
                        "3️⃣ Rules of Game\n\n"
                        "🔙 *Type 'Back' to list sports again*"
                    ),
                    "source": "menu_system"
                }
            else:
                 # If input was not a valid selection, fall through or ask again?
                 # Better to ask again within this state or fall through to RAG?
                 # If we return, we block RAG. If we fall through, we lose state context maybe.
                 # Let's return error to keep flow.
                 return {"response": "❌ Invalid Selection. Please select a number or type the exact sport name from the list.", "source": "validation_error"}

        # --- SUB MENU: GAME OPTIONS (Age, Events, Rules) ---
        elif current_state == MENU_GAME_OPTIONS:
            print(f"[DEBUG] Inside MENU_GAME_OPTIONS. Choice: {choice}")
            data = SESSION_DATA.get(session_id, {})
            selected_sport = data.get("selected_sport", "Unknown Sport")
            
            from rag.sql_queries import get_discipline_info, get_categories_by_sport
            
            info = get_discipline_info(selected_sport)
            game_id = info['game_id'] if info else None

            if choice == 1: # Age Criteria
                 print("[DEBUG] Choice 1 Selected")
                 if not game_id:
                      return {"response": f"ℹ️ No detailed age info found for **{selected_sport}**.", "source": "sql_database"}
                 
                 cats = get_categories_by_sport(game_id)
                 if cats:
                     txt = f"### 🎂 Age Criteria for {selected_sport}\n\n"
                     for c in cats:
                         gender_map = {1: "Male", 2: "Female"}
                         g_str = gender_map.get(c['gender'], "Open")
                         txt += f"- **{c['cat_name']}** ({g_str}): {c['from_age']} - {c['to_age']} Years\n"
                     return {"response": txt, "source": "sql_database"}
                 else:
                     return {"response": f"ℹ️ No specific age categories found for **{selected_sport}**.", "source": "sql_database"}

            elif choice == 2: # Events
                if not game_id:
                     return {"response": "ℹ️ Link not available.", "source": "error"}
                
                url = f"https://satg.telangana.gov.in/cmcup/showDisciplineEvents/{game_id}"
                return {
                    "response": (
                        f"🏆 **Events for {selected_sport}**\n\n"
                        f"Please visit the official link below to view all events:\n"
                        f"👉 [View Events for {selected_sport}]({url})"
                    ),
                    "source": "static_link"
                }

            elif choice == 3: # Rules
                 print("[DEBUG] Choice 3 Selected - Invoking RAG")
                 try:
                     query = f"What are the official rules and regulations for {selected_sport}?"
                     print(f"[DEBUG] RAG Rules Query: {query}")
                     
                     # Invoke RAG
                     from rag.chain import get_rag_chain # Ensure import available
                     chain = get_rag_chain()
                     res = chain.invoke({"question": query, "chat_history": []})
                     answer_text = res.get("response", "Content not found.")
                     
                     return {
                        "response": f"📜 **Rules for {selected_sport}**\n\n{answer_text}", 
                        "source": "rag_knowledge_base"
                     }
                 except Exception as e:
                     print(f"RAG Rules Error: {e}")
                     return {"response": f"ℹ️ Could not retrieve detailed rules for **{selected_sport}** at this time.", "source": "error"}

        # --- SUB MENU: LANGUAGE ---
        elif current_state == MENU_LANGUAGE:
             langs = {1: "English", 2: "Telugu", 3: "Hindi"}
             if choice in langs:
                 return {"response": f"✅ Language set to **{langs[choice]}** (Feature in progress).", "source": "menu_system"}
        
        # Catch-all
        return {"response": "❌ Invalid Option. Please select a valid number or type 'Back'.", "source": "menu_system"}

    # ------------------------------------------------
    # TEXT INPUT HANDLING FOR MENUS (Sub-Interactions)
    # ------------------------------------------------
    
    # 1. OFFICER LOCATION SEARCH
    if current_state == STATE_WAIT_OFFICER_LOC and not user_query.isdigit():
        # User entered cluster name?
        result = search_cluster_incharge(user_query)
        if result:
            return {"response": result, "source": "local_data_file"}
        else:
            return {"response": f"❌ I couldn't find a cluster named '**{user_query}**'.\nPlease check the spelling or try another cluster name.", "source": "local_data_file"}

    # 2. SPORT SCHEDULE SEARCH
    if current_state == STATE_WAIT_SPORT_SCHEDULE and not user_query.isdigit():
         from rag.sql_queries import get_discipline_info
         info = get_discipline_info(user_query)
         
         if info and info.get('game_id'):
             sport_name = info.get('sport_name', user_query).title()
             game_id = info['game_id']
             url = f"https://satg.telangana.gov.in/cmcup/viewschedulegames/{game_id}"
             
             return {
                 "response": (
                     f"🗓️ **Schedule for {sport_name}**\n\n"
                     f"You can view the specific schedule and fixtures here:\n"
                     f"👉 [View {sport_name} Schedule]({url})"
                 ),
                 "source": "sql_database"
             }
         else:
             return {"response": f"ℹ️ Could not find a sport named **{user_query}**. Please check the spelling or try another sport.", "source": "sql_database"}

    # 3. SPORT AGE/RULES SEARCH
    if current_state == STATE_WAIT_SPORT_AGE and not user_query.isdigit():
        from rag.sql_queries import get_sport_rules
        rules = get_sport_rules(user_query)
        if rules:
            txt = f"### 🎂 Age Criteria for {rules.get('sport_name')}\n\n"
            txt += f"**Min Age:** {rules.get('min_age')} years\n"
            txt += f"**Max Age:** {rules.get('max_age')} years\n"
            txt += f"**Team Size:** {rules.get('team_size') or 'Individual'}\n"
            txt += f"**Para Event:** {'Yes' if rules.get('is_para')=='1' else 'No'}\n\n"
            txt += "Type another sport to check, or 'Back'."
            return {"response": txt, "source": "sql_database"}
        else:
            return {"response": f"ℹ️ Could not find rules for **{user_query}**. Please check the spelling or try another sport.", "source": "sql_database"}

    # Fallthrough to Logic Interceptors...

            
        # ... Add other handlers as needed ...
    
    # ------------------------------------------------
    # END MENU MACHINE -> FALLTHROUGH TO LOGIC
    # ------------------------------------------------

    # 0. Static Data Interceptor
    # 0.1 Year/Version Mismatch Interceptor (High Priority)
    # If user asks for past years (e.g. 2015, 2024), redirect to 2025.
    year_match = re.search(r'\b(20\d{2})\b', user_query)
    if year_match:
        year = int(year_match.group(1))
        if year != 2025 and ("cm" in user_query or "cup" in user_query):
             return {
                 "response": f"ℹ️ **Note:** I currently only have information for the **Key Minister's Cup (CM Cup) 2025**. I don't have data for {year}.",
                 "source": "logic_interceptor"
             }

    # 0.2 Static Data Interceptor - DISABLED BY USER REQUEST
    # All queries now proceed to logic interceptors, SQL, or RAG LLM.
    pass

    # 0.5 Participation Stats (New)
    # Check for general count queries, but exclude "rules" or "limit" type queries (e.g., "how many players can register")
    stats_keywords = ["total participation", "how many players", "total registration", "total players", "no participation"]
    rule_exclusions = ["can", "limit", "allow", "eligible", "team size", "per team"]
    
    if any(k in user_query for k in stats_keywords) and not any(e in user_query for e in rule_exclusions):
        from rag.sql_queries import get_participation_stats
        count = get_participation_stats()
        return {
            "response": f"📊 **Participation Status:**\n\nA total of **{count} players** have registered for the Chief Minister's Cup (CM Cup) 2025 so far!",
            "model_used": "sql_database"
        }

    # 1. Phone Number match - PRIVACY WARNING

    # 0.6 Registration/Ack Number Link
    if "acknowledgment number" in user_query or "acknowledgement number" in user_query or "ack number" in user_query or "ack no" in user_query:
        if "what is" in user_query or "download" in user_query or "get" in user_query:
            return {
                "response": "📥 **Download Acknowledgment:**\n\nYou can find and download your Acknowledgment Number from the official website:\n\n👉 [Download Enrollment Acknowledgment](https://satg.telangana.gov.in/cmcup/downloadack)",
                "source": "static_rule"
            }

    # 1. Phone Number match - PRIVACY GUARD & VENUE FLOW
    original_query = raw_query.strip() # Keep casing for Reg IDs if needed
    phone_match = re.search(r'\b[6-9]\d{9}\b', original_query)
    
    # 1A. Venue/Status Flow (Exception to Filter)
    venue_intent = re.search(r'(venue|status|game|match|fixture)', user_query)
    
    if phone_match and venue_intent:
        phone = phone_match.group(0)
        print(f"⚡ Intent: Venue Lookup via Phone ({phone})")
        
        # SQL Lookup
        registrations = get_player_venues_by_phone(phone)
        
        if not registrations:
             return {"response": f"ℹ️ No registrations found for **{phone}**. Please check the number or register at the official site.", "source": "sql_database"}
        
        # Logic: 1 Record vs Multi
        if len(registrations) == 1:
            rec = registrations[0]
            venue = rec.get('venue')
            sport = rec.get('sport_name') or rec.get('event_name')
            
            txt = f"### 🏟️ Venue Details for {sport}\n"
            if venue:
                txt += f"**Venue:** {venue}\n"
                txt += f"**Date:** {rec.get('match_date') or 'Check Schedule'}\n"
            else:
                txt += "**Status:** There are no Venue Details available yet.\n"
                txt += f"You can contact your cluster Incharge:\n"
                txt += f"👤 **{rec.get('cluster_incharge', 'N/A')}**\n"
                txt += f"📞 **{rec.get('incharge_mobile', 'N/A')}**\n"
            
            return {"response": txt, "source": "sql_database"}
            
        else:
            # Multiple Records
            txt = f"found **{len(registrations)} registrations** for this number:\n"
            for r in registrations:
                s = r.get('sport_name') or r.get('event_name')
                txt += f"- {s}\n"
            
            txt += "\nSince you have multiple events, please provide your **Acknowledgment Number** (e.g., SATGCMC-...) to get specific venue details."
            return {"response": txt, "source": "sql_database"}

    # 1B. General Privacy Block
    if phone_match:
        print(f"⚡ Intent: Phone Number detected. Triggering Privacy Warning.")
        return {
             "response": "⚠️ **Privacy Notice:**\n\nFor your security, please **do not share personal phone numbers** or sensitive information in this chat. I cannot look up individual player records using phone numbers.\n\nHowever, if you are looking for your **venue details**, please ask 'Venue details for 9876543210'.",
             "source": "privacy_guardrail"
        }
    
    # 1C. Venue Intent BUT NO Phone -> Prompt
    # If user mentions venue/status/game but didn't provide phone, prompt them.
    # We use a broad check but ensure it's not a general question like "Where is the venue for Cricket?" (which might be generic).
    # Heuristic: If query is short OR has "my/check", prompt.
    if venue_intent:
        words = user_query.split()
        # Exclude general queries about levels, dates, or schedule
        is_general_query = any(k in user_query for k in ["level", "date", "when", "schedule", "time", "mandal", "district", "cluster", "state", "village", "gram", "panchayat"])
        
        if (len(words) < 8 or "my" in user_query or "check" in user_query or "know" in user_query) and not is_general_query:
             return {
                 "response": "To check your **Venue** or **Game Status**, please provide your registered **Phone Number**.\n\nExample: *Venue details for 9848012345*",
                 "source": "logic_interceptor"
             }

    # 2. Registration ID / Ack No -> Venue Lookup
    ack_match = re.search(r'\b(SATGCMC(?:\d+)?-\d+)\b', original_query, re.IGNORECASE)
    if ack_match:
        ack_no = ack_match.group(1).upper()
        if venue_intent or True: # Always treat Ack No as a lookup request now? Or only if venue intent? User said "Venue Details - Based on Acknowledgement Details". Let's assume lookup.
             print(f"⚡ Intent: Ack No Lookup ({ack_no})")
             rec = get_player_venue_by_ack(ack_no)
             if rec:
                venue = rec.get('venue')
                sport = rec.get('sport_name') or rec.get('event_name')
                
                # Parse Level
                level_str = "Cluster/Village Level"
                if rec.get('is_state_level') == '1': level_str = "Selected for State Level 🏆"
                elif rec.get('is_district_level') == '1': level_str = "Selected for District Level 🥇"
                elif rec.get('is_mandal_level') == '1': level_str = "Selected for Mandal Level 🥈"
                
                txt = f"### 👤 Player Details Found\n"
                txt += f"**Name:** {rec.get('player_nm', 'N/A')}\n"
                txt += f"**Reg ID:** {rec.get('player_reg_id', ack_no)}\n\n"
                
                # Format Location (Remove None/N/A)
                loc_parts = [
                    rec.get('villagename'),
                    rec.get('mandalname'),
                    rec.get('districtname')
                ]
                # Filter out None, 'None', 'N/A' and join
                clean_locs = [l for l in loc_parts if l and l.lower() not in ['none', 'n/a', '']]
                location_str = ", ".join(clean_locs) if clean_locs else "Location Pending"

                txt += f"**📍 Location:** {location_str}\n"
                txt += f"**🏅 Status:** {level_str}\n\n"
                
                txt += f"**🏟️ Venue Details:**\n"
                txt += f"**Sport:** {sport}\n"
                if venue:
                    txt += f"**Venue:** {venue}\n"
                    txt += f"**Date:** {rec.get('match_date') or 'Check Schedule'}\n"
                else:
                    txt += "**Venue:** Not assigned yet.\n"
                    
                txt += f"\n**👤 Coach/Incharge:**\n"
                
                # HYBRID LOGIC: If SQL returns None for Incharge, ask RAG
                incharge_name = rec.get('cluster_incharge')
                incharge_contact = rec.get('incharge_mobile')
                
                if not incharge_name and rec.get('districtname'):
                    print("⚠️ Hybrid Trigger: SQL missing Incharge. Asking RAG...")
                    try:
                        rag_bot = get_or_init_rag_chain()
                        sport_detail = rec.get('sport_name') or rec.get('event_name') or "sports"
                        
                        # Use available hierarchy for RAG
                        rag_query = f"Who is the {sport_detail} incharge for "
                        if rec.get('mandalname'): rag_query += f"Mandal: {rec.get('mandalname')}, "
                        if rec.get('districtname'): rag_query += f"District: {rec.get('districtname')}?"
                        
                        rag_resp = rag_bot.invoke({"question": rag_query})
                        
                        # Extract simple text from chain response
                        rag_text = rag_resp.get('result', str(rag_resp)) if isinstance(rag_resp, dict) else str(rag_resp)
                        
                        # Filter out generic 'not found' messages to keep UI clean
                        if "couldn't find" in rag_text.lower() or "not available" in rag_text.lower():
                             txt += "**Status:** To be assigned by District Sports Officer.\n"
                        else:
                             txt += f"*(Retrieved via AI)*: {rag_text}\n"

                    except Exception as e:
                        print(f"Hybrid RAG Failed: {e}")
                        txt += "**Status:** Contact District Helpdesk.\n"
                else:
                    txt += f"**Name:** {incharge_name or 'N/A'}\n"
                    txt += f"**Contact:** {incharge_contact or 'N/A'}\n"
                
                
                final_response = {"response": txt, "source": "sql_database"}
                print(f"DEBUG RESPONSE ({ack_no}):\n{txt}")
                return final_response
             else:
                 # Fallthrough to RAG if not found? Or explicit error?
                 pass 


    # 2. Registration ID - REMOVED
    # Player lookup by Reg ID is disabled for privacy reasons.
    # Fallthrough to RAG/General Logic.


    # 3. Match/Fixture ID
    match_match = re.search(r'(?:match|fixture)\s*(?:id|no)?\s*[:#-]?\s*(\d+)', original_query, re.IGNORECASE)
    if match_match:
        fid = match_match.group(1)
        print(f"⚡ Intent: Fixture Lookup (ID: {fid})")
        try:
            res = get_fixture_details(fid)
            if res:
                txt = f"### 🏟️ Match Details (ID: {res['fixture_id']})\n"
                txt += f"**Match No:** {res['match_no']}\n"
                txt += f"**Venue:** {res['venue']}\n"
                txt += f"**Teams:** {res.get('team1_name', 'TBD')} vs {res.get('team2_name', 'TBD')}\n"
                txt += f"**Date:** {res['match_date']} ({res['match_day']}) @ {res['match_time']}\n"
                txt += f"**Round:** {res['round_name']}"
                return {"response": txt, "source": "sql_database"}
            else:
                 return {"response": f"❌ No match found with ID **{fid}**.", "source": "sql_database"}
        except Exception as e:
            print(f"SQL Error: {e}")

    # 4. Sport Schedule (New)
    sport_pattern = r'(?:schedule|events|matches)\s*(?:for|of|in)?\s*([a-zA-Z\s]+)'
    sport_match = re.search(sport_pattern, original_query, re.IGNORECASE)
    if sport_match:
        raw_sport = sport_match.group(1).strip()
        clean_sport = re.sub(r'\s+(matches|events|schedule|today|tomorrow)\b', '', raw_sport, flags=re.IGNORECASE).strip()
        if clean_sport.lower() not in ["the", "this"] and len(clean_sport) > 3:
             print(f"⚡ Intent: Sport Schedule ({clean_sport})")
             try:
                 schedules = get_sport_schedule(clean_sport)
                 if schedules:
                     txt = f"### 📅 {clean_sport.title()} Schedule (Next 5)\n"
                     for m in schedules[:5]:
                         txt += f"- **{m.get('event_name')}**: {m.get('team1_name')} vs {m.get('team2_name')} @ {m.get('venue')}\n"
                     return {"response": txt, "source": "sql_database"}
             except Exception as e:
                 print(f"SQL Error (Schedule): {e}")


    # 5. Geo Query
    NAME_REGEX = r"([a-zA-Z\s\-\(\)]+?)"
    geo_pattern_1 = fr"(?:district|mandal|village)\s*(?:does)?\s*{NAME_REGEX}\s*(?:belong|exist|register|in the db|in database)"
    geo_pattern_2 = fr"is\s+{NAME_REGEX}\s+a\s+(?:village|district|mandal)"
    geo_pattern_3 = fr"details\s*(?:for|about|of)?\s*{NAME_REGEX}"

    geo_match = re.search(geo_pattern_1, original_query, re.IGNORECASE)
    if not geo_match: geo_match = re.search(geo_pattern_2, original_query, re.IGNORECASE)
    if not geo_match: geo_match = re.search(geo_pattern_3, original_query, re.IGNORECASE)

    if geo_match:
        raw_name = geo_match.group(1).strip()
        clean_name = re.sub(r'\s+(district|mandal|village|zila|jilla)\b', '', raw_name, flags=re.IGNORECASE).strip()
        
        if len(clean_name) > 3 and clean_name.lower() not in ["the", "this", "that"]:
            print(f"⚡ Intent: Geo Lookup ({clean_name})")
            try:
                res = get_geo_details(clean_name)
                if res:
                    t = res['type']
                    d = res['data']
                    txt = f"### 📍 Location Found: {d.get('vill_nm') or d.get('mandal_nm') or d.get('dist_nm')}\n"
                    txt += f"**Type:** {t}\n"
                    if t == 'Village':
                        txt += f"**Mandal:** {d.get('parent_mandal')}\n"
                        txt += f"**District:** {d.get('parent_district')}"
                    elif t == 'Mandal':
                        txt += f"**District:** {d.get('parent_district')}"
                    return {"response": txt, "source": "sql_database"}
                else:
                    return {"response": f"🚫 **{clean_name}** could not be found in our Village/Mandal/District database.", "source": "sql_database"}
            except Exception as e:
                print(f"SQL Error: {e}")


    # 5.4 Level Schedule Lookup (Deterministic)
    schedule_pattern = r"(cluster|gp|gram\s*panchayat|mandal|ulb|district|state|assembly).*?(start|end|date|schedule|when|time)"
    schedule_match = re.search(schedule_pattern, original_query, re.IGNORECASE)
    if schedule_match:
        level_keyword = schedule_match.group(1).lower()
        print(f"⚡ Intent: Level Schedule Lookup (Level: {level_keyword})")
        
        # Hardcoded Schedule from 'CM_Cup_2025_RAG_Knowledge.txt'
        # This ensures 100% accuracy vs RAG hallucinations
        schedule_data = {
            "gram": "🗓️ **Grampanchayat Level:** 17 January to 22 January 2026 (6 days)",
            "gp": "🗓️ **Grampanchayat Level:** 17 January to 22 January 2026 (6 days)",
            "cluster": "🗓️ **Grampanchayat/Cluster Level:** 17 January to 22 January 2026 (6 days)",
            "mandal": "🗓️ **Mandal / ULB Level:** 28 January to 31 January 2026 (4 days)",
            "ulb": "🗓️ **Mandal / ULB Level:** 28 January to 31 January 2026 (4 days)",
            "assembly": "🗓️ **Assembly Constituency Level:** 03 February to 07 February 2026 (5 days)",
            "district": "🗓️ **District Level:** 10 February to 14 February 2026 (5 days)",
            "state": "🗓️ **State Level:** 19 February to 26 February 2026 (8 days)"
        }
        
        # Find best match
        response_txt = ""
        for key, val in schedule_data.items():
            if key in level_keyword:
                response_txt = val
                break
        
        if not response_txt:
            # Fallback for 'cluster' mapping if not caught above logic simple match
            if "cluster" in level_keyword: response_txt = schedule_data["cluster"]
            if "gram" in level_keyword: response_txt = schedule_data["gram"]
            if "mandal" in level_keyword: response_txt = schedule_data["mandal"]
            if "district" in level_keyword: response_txt = schedule_data["district"]
            if "state" in level_keyword: response_txt = schedule_data["state"]

        if response_txt:
             return {"response": f"{response_txt}\n\n*Note: Dates are subject to official guidelines.*", "source": "static_rule_engine"}

    # 5.5 Discipline/Level Lookup
    level_pattern = r"(disciplines?|sports?|games?|events?).*?\b(cluster|mandal|district|state)\b\s*(?:level)?"
    level_match = re.search(level_pattern, original_query, re.IGNORECASE)
    if level_match:
        level_name = level_match.group(2).lower()
        print(f"⚡ Intent: Discipline Lookup (Level: {level_name})")
        try:
            from rag.sql_queries import get_disciplines_by_level
            games = get_disciplines_by_level(level_name)
            if games:
                txt = f"### 🏅 Sports at {level_name.title()} Level\n"
                for g in games:
                    txt += f"- {g}\n"
                return {"response": txt, "source": "sql_database"}
            else:
                 # If SQL doesn't have data (e.g. new disciplines not in DB), Fallback to RAG
                 print(f"ℹ️ SQL found no disciplines for {level_name}. Falling back to RAG.")
                 pass 
        except Exception as e:
            print(f"SQL Error: {e}")
            pass

    # 6. Complex SQL Queries (Agentic)
    # Detects questions about counts, lists, specific aggregations (Agentic)
    # 1. Strong Rule Keywords (Age, Born, Criteria) - Trigger SQL immediately (handles typos like 'hokey')
    if re.search(r"\b(age|born|birth|criteria|rules|limit|eligible|eligibility)\b", original_query, re.IGNORECASE):
        print(f"🤖 Intent: Rule/Age Query (Triggering SQL Agent)")
        try:
             sql_response = run_sql_agent(original_query)
             if "I try to query" not in sql_response and "error" not in sql_response.lower():
                 return {"response": sql_response, "source": "sql_agent"}
        except Exception as e:
             print(f"SQL Agent Failed: {e}")

    # 2. General SQL Intents (Count, List, Who is) - Require a target object (player, sport, etc.)
    sql_intent_pattern = r"(how many|count|total|list|show|who is|what is|find).*(player|registration|venue|match|game|sport|cluster|incharge|hockey|cricket|kabaddi|kho|athletics|volleyball|ball|tennis|cycling|wrestling|karate|taekwondo|gymnastics|swimming|yoga|particip)"
    if re.search(sql_intent_pattern, original_query, re.IGNORECASE):
        print(f"🤖 Intent: Complex/Agentic SQL Query")
        try:
            sql_response = run_sql_agent(original_query)
            # if agent fails to understand, it might return a generic error.
            # We can check specific error strings if we want to fallback to RAG.
            if "I try to query" not in sql_response and "error" not in sql_response.lower():
                return {"response": sql_response, "source": "sql_agent"}
        except Exception as e:
            print(f"SQL Agent Failed: {e}")
            # Fallthrough to RAG if SQL agent fails
            pass

    # 7. RAG Fallback
    print(f"[INFO] Intent: General Query")
    
    try:
        # Use Lazy Loaded Chain
        rag = get_or_init_rag_chain()
        if not rag:
             return {"response": "The AI Brain is initializing. Please try again in 10 seconds.", "source": "system"}
        
        # Memory Management
        # session_id passed in args
        chat_history = []
        if session_id:
            chat_history = CHAT_SESSIONS.get(session_id, [])
        
        # Invoke Chain with History
        input_payload = {"question": original_query, "chat_history": chat_history}
        
        # rag.invoke now expects a dict because we updated chain.py
        response_data = rag.invoke(input_payload)
        
        # response_data is a dictionary from ask_llm {"response", "model_used"}
        if isinstance(response_data, dict):
            final_answer = response_data.get("response", "No response")
            model = response_data.get("model_used", "rag")
        else:
             final_answer = str(response_data)
             model = "rag"

        # Update Memory
        if session_id:
            # Append turn: (User, AI)
            chat_history.append(("User", original_query))
            chat_history.append(("AI", final_answer))
            # Keep last 10 turns (20 items)
            CHAT_SESSIONS[session_id] = chat_history[-20:]

        return {"response": final_answer, "source": "rag_knowledge_base", "model_used": model}
    except Exception as e:
        print(f"RAG Crash: {e}")
        return {"response": f"I encountered an error accessing the knowledge base. Error: {str(e)}", "source": "error_handler"}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    # Auto-generate session_id if missing to support tools like Postman
    # However, the client MUST send this back to maintain state!
    current_session_id = request.session_id or str(uuid.uuid4())
    
    response_data = await process_user_query(request.query, current_session_id)
    
    # Inject session_id into response so client knows what to send back
    if isinstance(response_data, dict):
        response_data["session_id"] = current_session_id
        
    return response_data

@app.post("/ask")
async def ask_endpoint(request: ChatRequest):
    return await process_user_query(request.query, request.session_id)

# --------------------------------------------------
# 9. WhatsApp Endpoint
# --------------------------------------------------
@app.post("/whatsappchat")
async def whatsapp_chat_endpoint(request: WhatsAppChatRequest):
    """
    WhatsApp specialized endpoint.
    Uses 'phone_number' as session_id for continuity.
    """
    user_message = (request.user_message or "").strip()
    session_id = request.phone_number  # Use phone number as persistent session ID

    if not user_message:
        raise HTTPException(status_code=400, detail="user_message cannot be empty")

    try:
        # Call the unified logic
        return await process_user_query(user_message, session_id)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Processing Error: {str(e)}")
