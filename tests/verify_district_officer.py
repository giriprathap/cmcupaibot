
import sys
import os

# Ensure project root is in path
sys.path.append(os.getcwd())

from rag.location_search import search_district_officer

def test_lookup(district):
    print(f"--- Testing: {district} ---")
    res = search_district_officer(district)
    print(res)
    if res:
        print("✅ Match Found")
    else:
        print("❌ No Match")
    print("\n")

if __name__ == "__main__":
    # 1. Exact Match
    test_lookup("Warangal")
    
    # 2. Case Insensitive
    test_lookup("badradri kothagudem") # Spelling in CSV is "Bhadradri kothagudem"
    
    # 3. Fuzzy
    test_lookup("Jagtial") # CSV: Jagithyal
    
    # 4. Unknown
    test_lookup("Mars Colony")
