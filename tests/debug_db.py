import sys
import os
sys.path.append(os.getcwd())
from rag.sql_queries import get_fixture_details, get_geo_details
from rag.data_store import get_datastore

def test():
    try:
        print("Initializing DB...")
        ds = get_datastore()
        ds.init_db()
        print("DB Initialized.")
        
        print("Columns in districtmaster:")
        print(ds.query("SELECT * FROM districtmaster LIMIT 1").columns.tolist())
        
        # Test Fixture
        fid = "295"
        print(f"Testing Fixture {fid}...")
        res = get_fixture_details(fid)
        print(f"Fixture Result: {res}")
        
        # Test Geo
        place = "Sirikonda"
        print(f"Testing Geo {place}...")
        res = get_geo_details(place)
        print(f"Geo Result: {res}")
        
    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
