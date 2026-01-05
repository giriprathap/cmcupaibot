
from rag.data_store import get_datastore

def main():
    ds = get_datastore()
    if not ds.initialized: ds.init_db()
    
    df = ds.query("SELECT * FROM player_details LIMIT 1")
    print("\nCOLUMNS_START")
    for col in df.columns:
        print(col)
    print("COLUMNS_END_PLAYER")
    
    print("\nCOLUMNS_START_VILLAGE")
    df_v = ds.query("SELECT * FROM villagemaster LIMIT 1")
    for col in df_v.columns:
        print(col)
    print("COLUMNS_END_VILLAGE")

if __name__ == "__main__":
    main()
