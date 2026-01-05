import pandas as pd
import os

# Paths
CSV_DIR = r"./data/csvs"
MD_DIR = r"./data/mdFiles"

os.makedirs(MD_DIR, exist_ok=True)

def clean_text(text):
    if pd.isna(text) or text == "NULL":
        return "Unknown"
    return str(text).strip()

def process_districts():
    print("Processing Districts...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "districtmaster.csv"))
        lines = []
        for _, row in df.iterrows():
            line = f"District **{clean_text(row.get('DistrictName'))}** (ID: {row.get('DistrictNo')}) has Code '{clean_text(row.get('Dist_code'))}'."
            lines.append(line)
        
        with open(os.path.join(MD_DIR, "rag_districts.md"), "w", encoding="utf-8") as f:
            f.write("# District Information\n\n" + "\n".join(lines))
        print("✅ Districts Done.")
    except Exception as e:
        print(f"❌ Districts Failed: {e}")

def load_mandal_map():
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "mandalmaster.csv"))
        # Map ID -> MandalName (mandalmaster uses 'ID')
        return dict(zip(df['ID'], df['MandalName']))
    except Exception as e:
        print(f"⚠️ Could not load mandal map: {e}")
        return {}

def load_discipline_map():
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "tb_discipline.csv"))
        # Map game_id -> dist_game_nm
        return dict(zip(df['game_id'], df['dist_game_nm']))
    except Exception as e:
        print(f"⚠️ Could not load discipline map: {e}")
        return {}

def load_district_map():
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "districtmaster.csv"))
        # Map DistrictNo -> DistrictName
        return dict(zip(df['DistrictNo'], df['DistrictName']))
    except Exception as e:
        print(f"⚠️ Could not load district map: {e}")
        return {}

DISTRICT_MAP = load_district_map()
MANDAL_MAP = load_mandal_map()
DISCIPLINE_MAP = load_discipline_map()

def process_mandals():
    print("Processing Mandals...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "mandalmaster.csv"))
        lines = []
        for _, row in df.iterrows():
            dist_id = row.get('DistrictNo')
            dist_name = DISTRICT_MAP.get(dist_id, f"ID {dist_id}")
            
            line = f"Mandal **{clean_text(row.get('MandalName'))}** is in District **{dist_name}** (ID: {dist_id}). It falls under Assembly Constituency **{clean_text(row.get('ac_name'))}**."
            lines.append(line)
        
        with open(os.path.join(MD_DIR, "rag_mandals.md"), "w", encoding="utf-8") as f:
            f.write("# Mandal Information\n\n" + "\n".join(lines))
        print("✅ Mandals Done.")
    except Exception as e:
        print(f"❌ Mandals Failed: {e}")

def process_villages():
    print("Processing Villages...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "villagemaster.csv"))
        lines = []
        # Limiting output if too huge, but RAG can handle text. For safety, let's dump all.
        for _, row in df.iterrows():
            mandal_id = row.get('MandalNo')
            dist_id = row.get('DistNo')
            
            mandal_name = MANDAL_MAP.get(mandal_id, f"ID {mandal_id}")
            dist_name = DISTRICT_MAP.get(dist_id, f"ID {dist_id}")
            
            line = f"Village **{clean_text(row.get('VillageName'))}** belongs to Mandal **{mandal_name}** (ID: {mandal_id}) in District **{dist_name}** (ID: {dist_id})."
            lines.append(line)
        
        with open(os.path.join(MD_DIR, "rag_villages.md"), "w", encoding="utf-8") as f:
            f.write("# Village Information\n\n" + "\n".join(lines))
        print("✅ Villages Done.")
    except Exception as e:
        print(f"❌ Villages Failed: {e}")

def process_clusters():
    print("Processing Clusters...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "clustermaster.csv"))
        lines = []
        for _, row in df.iterrows():
            mandal_id = row.get('mand_id')
            dist_id = row.get('dist_id')
            
            mandal_name = MANDAL_MAP.get(mandal_id, f"ID {mandal_id}")
            dist_name = DISTRICT_MAP.get(dist_id, f"ID {dist_id}")

            line = f"Cluster **{clean_text(row.get('clustername'))}** (ID: {row.get('cluster_id')}) is in Mandal **{mandal_name}** (ID: {mandal_id}), District **{dist_name}** (ID: {dist_id})."
            lines.append(line)
        
        with open(os.path.join(MD_DIR, "rag_clusters.md"), "w", encoding="utf-8") as f:
            f.write("# Cluster Information\n\n" + "\n".join(lines))
        print("✅ Clusters Done.")
    except Exception as e:
        print(f"❌ Clusters Failed: {e}")

def process_disciplines():
    print("Processing Disciplines (Sports)...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "tb_discipline.csv"))
        lines = []
        for _, row in df.iterrows():
            age_range = f"{clean_text(row.get('from_age'))} to {clean_text(row.get('to_age'))}"
            
            # Category Logic
            is_para = str(row.get('is_para', '0')).strip()
            category = "Para Sports" if is_para == '1' else "General Sports"
            
            # Rules Logic
            rules = clean_text(row.get('rules_pdf'))
            rules_str = f"Rules PDF: {rules}" if rules != "Unknown" else "Rules PDF: Not Available"
            
            # Category Number for Reference
            cat_no = row.get('cat_no')

            line = f"Sport: **{clean_text(row.get('dist_game_nm'))}** (ID: {row.get('game_id')}). Category: **{category}** (Cat No: {cat_no}). Age Eligibility: {age_range} years. Team Size: {clean_text(row.get('team_size'))} players. {rules_str}."
            lines.append(line)
        
        with open(os.path.join(MD_DIR, "rag_disciplines.md"), "w", encoding="utf-8") as f:
            f.write("# Sports Discipline Details\n\n" + "\n".join(lines))
        print("✅ Disciplines Done.")
    except Exception as e:
        print(f"❌ Disciplines Failed: {e}")

def process_events():
    print("Processing Events...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "tb_events.csv"))
        lines = []
        for _, row in df.iterrows():
            disc_id = row.get('discipline_id')
            disc_name = DISCIPLINE_MAP.get(disc_id, f"Sports ID {disc_id}")
            
            line = f"Event **{clean_text(row.get('event_name'))}** belongs to Sport: **{disc_name}** (ID: {disc_id}). Category: {clean_text(row.get('cat_no'))}."
            lines.append(line)
        
        with open(os.path.join(MD_DIR, "rag_events.md"), "w", encoding="utf-8") as f:
            f.write("# Sports Event List\n\n" + "\n".join(lines))
        print("✅ Events Done.")
    except Exception as e:
        print(f"❌ Events Failed: {e}")

def process_fixtures():
    print("Processing Fixtures...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "tb_fixtures.csv"))
        lines = []
        for _, row in df.iterrows():
            match_name = clean_text(row.get('match_no'))
            
            # Resolve Team Names
            t1_id = row.get('team1_dist_id')
            t2_id = row.get('team2_dist_id')
            
            t1_name = DISTRICT_MAP.get(t1_id, f"District ID {t1_id}") if pd.notna(t1_id) else "TBD"
            t2_name = DISTRICT_MAP.get(t2_id, f"District ID {t2_id}") if pd.notna(t2_id) else "TBD"
            
            # Use TBD for unknown match names
            # Clean match name: remove "Match" prefix if present to avoid "Match Match- 1"
            match_name_clean = match_name.replace("Match", "").replace("-", "").strip()
            # If it became empty or just a number, label it nicely
            if match_name_clean.isdigit():
                 display_match_name = f"Match {match_name_clean}"
            elif match_name.lower().startswith("match"):
                 display_match_name = match_name # Keep original if complex
            else:
                 display_match_name = f"Match {match_name}"

            # Remove double "Match Match" if it slipped through
            if "Match Match" in display_match_name:
                display_match_name = display_match_name.replace("Match Match", "Match")
                
            line = f"- **{display_match_name}** (ID: {row.get('fixture_id')}) is scheduled for **{clean_text(row.get('match_day'))}** at **{clean_text(row.get('match_time'))}**. Venue: {clean_text(row.get('venue'))}. Teams: **{t1_name}** vs **{t2_name}**."
            lines.append(line)
        
        with open(os.path.join(MD_DIR, "rag_fixtures.md"), "w", encoding="utf-8") as f:
            f.write("# Tournament Fixtures / Schedule\n\n" + "\n".join(lines))
        print("✅ Fixtures Done.")
    except Exception as e:
        print(f"❌ Fixtures Failed: {e}")

def process_players():
    print("Processing Players...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "player_details.csv"))
        lines = []
        for _, row in df.iterrows():
            player_name = clean_text(row.get('player_nm'))
            father_name = clean_text(row.get('father_nm'))
            
            game_id = row.get('game_id')
            discipline = DISCIPLINE_MAP.get(game_id, f"Sport ID {game_id}")
            
            dist_id = row.get('district_id')
            district = DISTRICT_MAP.get(dist_id, f"District ID {dist_id}")
            
            mandal_id = row.get('mandal_id')
            mandal = MANDAL_MAP.get(mandal_id, f"Mandal ID {mandal_id}")
            
            line = f"Player **{player_name}** (Father: {father_name}) plays **{discipline}**. Represents District **{district}**, Mandal **{mandal}**."
            lines.append(line)
            
        with open(os.path.join(MD_DIR, "rag_players.md"), "w", encoding="utf-8") as f:
            f.write("# Player Details\n\n" + "\n".join(lines))
        print("✅ Players Done.")
    except Exception as e:
        print(f"❌ Players Failed: {e}")

def process_categories():
    print("Processing Categories...")
    try:
        df = pd.read_csv(os.path.join(CSV_DIR, "tb_category.csv"))
        lines = []
        for _, row in df.iterrows():
            cat_name = clean_text(row.get('cat_name'))
            gender_code = row.get('gender')
            gender_map = {1: "Male", 2: "Female"}
            gender = gender_map.get(gender_code, "Mixed/Open")
            
            disc_id = row.get('discipline_id')
            discipline = DISCIPLINE_MAP.get(disc_id, f"Sport ID {disc_id}")
            
            age_range = f"{clean_text(row.get('from_age'))} to {clean_text(row.get('to_age'))}"
            
            line = f"Category **{cat_name}** (ID: {row.get('id')}) is for **{discipline}** ({gender}). Age Eligibility: {age_range} years."
            lines.append(line)
            
        with open(os.path.join(MD_DIR, "rag_categories.md"), "w", encoding="utf-8") as f:
            f.write("# Sports Categories and Age Limits\n\n" + "\n".join(lines))
        print("✅ Categories Done.")
    except Exception as e:
        print(f"❌ Categories Failed: {e}")

if __name__ == "__main__":
    process_districts()
    process_mandals()
    process_villages()
    process_clusters()
    process_disciplines()
    process_events()
    process_fixtures()
    process_players()
    process_categories()
    print("\n🎉 All CSVs processed into Markdown files for RAG!")
