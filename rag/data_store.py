import sqlite3
import pandas as pd
import os
import glob

class DataStore:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataStore, cls).__new__(cls)
            cls._instance.conn = sqlite3.connect(":memory:", check_same_thread=False)
            cls._instance.cursor = cls._instance.conn.cursor()
            cls._instance.initialized = False
        return cls._instance

    def init_db(self, csv_dir="data/csvs"):
        if self.initialized:
            print("[OK] DataStore already initialized.")
            return

        print("[*] Initializing SQLite Data Store...")
        
        # Load all CSVs
        csv_files = glob.glob(os.path.join(csv_dir, "*.csv"))
        for f in csv_files:
            try:
                table_name = os.path.splitext(os.path.basename(f))[0]
                # Read CSV
                df = pd.read_csv(f, dtype=str)
                # Clean headers: lowercase, strip
                df.columns = df.columns.str.strip().str.lower()
                
                # Write to SQLite
                df.to_sql(table_name, self.conn, if_exists="replace", index=False)
                print(f"   -> Loaded table: {table_name} ({len(df)} rows)")
            except Exception as e:
                print(f"   [!] Error loading {f}: {e}")

        # Create Indices for Performance
        indices = [
            ("player_details", "mobile_no"),
            ("player_details", "player_reg_id"),
            ("player_details", "id"),
            ("villagemaster", "villagename"),
            ("villagemaster", "cluster_id"),
            ("clustermaster", "cluster_id"),
            ("tb_events", "id"),
            ("tb_fixtures", "disc_id")
        ]
        
        for table, col in indices:
            try:
                self.conn.execute(f"CREATE INDEX idx_{table}_{col} ON {table}({col})")
            except Exception:
                pass # Table or col might not exist

        self.create_views()

        self.initialized = True
        print("[OK] DataStore Ready!")

    def create_views(self):
        """
        Create simplified, secure views for the LLM Agent.
        - EXCLUDES Aadhar/Sensitive PII.
        - INCLUDES Mobile/RegID for lookup.
        - Denormalizes data (joins) for easier natural language querying.
        """
        print("[*] Creating Secure SQL Views for AI...")
        
        # 1. view_player_unified
        # Joins: player -> village -> mandal -> district
        # Joins: player -> discipline (sport)
        # Joins: player -> events
        view_query = """
        CREATE VIEW IF NOT EXISTS view_player_unified AS
        SELECT 
            p.player_nm,
            p.player_reg_id,
            p.mobile_no,
            p.gender,
            p.player_age,
            
            -- Location Names
            v.villagename,
            m.mandalname,
            d.districtname,
            c.clustername,
            
            -- Sport/Event Info
            dis.dist_game_nm as sport_name,
            e.event_name,
            f.venue,
            f.match_date

        FROM player_details p
        LEFT JOIN villagemaster v ON p.village_id = v.id
        LEFT JOIN mandalmaster m ON p.mandal_id = m.id  -- Assuming mandal_id key
        LEFT JOIN districtmaster d ON p.district_id = d.districtno -- Assuming district_id maps to districtno
        LEFT JOIN clustermaster c ON v.cluster_id = c.cluster_id
        LEFT JOIN tb_discipline dis ON p.game_id = dis.game_id
        LEFT JOIN tb_events e ON p.event_id = e.id
        LEFT JOIN tb_fixtures f ON p.game_id = f.disc_id 
             AND p.gender = f.gender 
             AND (p.district_id = f.team1_dist_id OR p.district_id = f.team2_dist_id)
        """
        try:
            self.conn.execute(view_query)
            print("   -> Created View: view_player_unified")
        except Exception as e:
            print(f"   [!] Error creating view: {e}")

        # 2. view_sport_rules
        # Simple lookup for rules
        view_rules_query = """
        CREATE VIEW IF NOT EXISTS view_sport_rules AS
        SELECT 
            dist_game_nm as sport_name,
            from_age as min_age,
            to_age as max_age,
            team_size,
            is_team,
            is_para
        FROM tb_discipline
        """
        try:
            self.conn.execute(view_rules_query)
            print("   -> Created View: view_sport_rules")
        except Exception as e:
            print(f"   [!] Error creating view_sport_rules: {e}")


    def query(self, query, params=()):
        return pd.read_sql_query(query, self.conn, params=params)

    def execute(self, query, params=()):
        self.cursor.execute(query, params)
        self.conn.commit()

# Global Accessor
def get_datastore():
    return DataStore()
