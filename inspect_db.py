import sys
import os

# Ensure we can import from local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag.data_store import DataStore

def inspect():
    print("🔹 Initializing DataStore...")
    ds = DataStore()
    ds.init_db()
    
    print("\n🔹 Querying Player Details...")
    cursor = ds.conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='player_details'")
    if cursor.fetchone():
        print("✅ 'player_details' table found.")
        
        # Get Sample Mobile
        cursor.execute("SELECT mobile_no, player_nm FROM player_details WHERE mobile_no IS NOT NULL AND mobile_no != '' LIMIT 5")
        rows = cursor.fetchall()
        print("\n🔹 Valid Mobile Numbers found in DB:")
        for r in rows:
            print(f"   - {r[0]} (Player: {r[1]})")
    else:
        print("❌ 'player_details' table NOT found.")

if __name__ == "__main__":
    inspect()

