
from rag.data_store import get_datastore

def check_structure():
    ds = get_datastore()
    if not ds.initialized: ds.init_db()
    
    # Get columns by selecting 1 row
    print("--- Columns of player_details ---")
    df = ds.query("SELECT * FROM player_details LIMIT 1")
    if not df.empty:
        print(df.columns.tolist())
        print(df.iloc[0].to_dict())
    else:
        print("Table empty?")
        # Force get columns if empty? 
        # But we know it has 1000 rows.

    print("\n--- Non-Null vill_gp_name Count ---")
    count = ds.query("SELECT COUNT(*) as c FROM player_details WHERE vill_gp_name IS NOT NULL AND vill_gp_name != ''")
    print(count)


if __name__ == "__main__":
    check_structure()
