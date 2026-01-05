from rag.data_store import get_datastore
import pandas as pd

def audit_schema():
    ds = get_datastore()
    if not ds.initialized:
        ds.init_db()
    
    # Get list of tables
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = ds.query(query)
    
    print("\n=== Database Schema Audit ===\n")
    
    for table in tables['name']:
        print(f"## Table: {table}")
        # Get columns
        col_info = ds.query(f"PRAGMA table_info({table})")
        # Print cid, name, type
        # DataFrame columns usually: cid, name, type, notnull, dflt_value, pk
        for _, row in col_info.iterrows():
            print(f"  - {row['name']} ({row['type']})")
        print("")

if __name__ == "__main__":
    audit_schema()
