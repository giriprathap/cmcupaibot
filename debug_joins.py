
from rag.data_store import get_datastore
import pandas as pd

def check_joins():
    ds = get_datastore()
    if not ds.initialized: ds.init_db()
    
    print("--- Player Details Sample (vill_gp_name) ---")
    query_p = "SELECT vill_gp_name, player_nm FROM player_details LIMIT 10"
    df_p = ds.query(query_p)
    print(df_p)
    
    print("\n--- Village Master Sample (villagename) ---")
    query_v = "SELECT villagename FROM villagemaster LIMIT 10"
    df_v = ds.query(query_v)
    print(df_v)
    
    print("\n--- Testing Join ---")
    query_join = """
    SELECT 
        p.player_nm,
        p.vill_gp_name,
        v.villagename,
        v.cluster_id
    FROM player_details p
    LEFT JOIN villagemaster v ON TRIM(LOWER(p.vill_gp_name)) = TRIM(LOWER(v.villagename))
    LIMIT 10
    """
    df_join = ds.query(query_join)
    print(df_join)

if __name__ == "__main__":
    check_joins()
