import pandas as pd
import re
import os

# Paths
TEXT_FILE = r"data/new data/Mandal_Incharges_Cleaned.txt"
CLUSTER_CSV = r"data/csvs/clustermaster.csv"
MANDAL_CSV = r"data/csvs/mandalmaster.csv"

def clean_name(name):
    """Normalize string for matching."""
    if pd.isna(name): return ""
    return str(name).strip().lower().replace(" ", "")

def parse_text_data(file_path):
    """Parses the text file into a dictionary keyed by (Mandal, Cluster)."""
    data_map = {}
    
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip() or "Mandal:" not in line:
                continue
                
            # Parse Line
            # Format: Mandal: Name | Cluster: Name | Incharge Details: Name | Contact: Number
            try:
                parts = line.split("|")
                mandal = parts[0].split(":")[1].strip()
                cluster = parts[1].split(":")[1].strip()
                name_part = parts[2].split(":")[1].strip()
                contact = parts[3].split(":")[1].strip()
                
                # Clean keys
                key = (clean_name(mandal), clean_name(cluster))
                data_map[key] = {
                    "incharge_name": name_part,
                    "mobile_no": contact
                }
            except Exception as e:
                print(f"Skipping line due to error: {line.strip()} -> {e}")
                
    return data_map

def main():
    print(f"Loading data...")
    
    # 1. Load Mandal & District Maps
    mandal_df = pd.read_csv(MANDAL_CSV, dtype=str)
    # Map MandalName -> DistrictNo
    mandal_to_dist = {}
    for _, row in mandal_df.iterrows():
        m_name = clean_name(row['MandalName'])
        d_no = str(row['DistrictNo']).strip()
        mandal_to_dist[m_name] = d_no
        
    print(f"Mapped {len(mandal_to_dist)} Mandals to Districts.")
    
    # 2. Parse Text Data and Link to District
    raw_data = parse_text_data(TEXT_FILE)
    cluster_dist_map = {} # (cluster, dist_id) -> info
    
    skipped = 0
    mapped = 0
    
    # Debug: Print first 5 mapped keys
    print("Debug: Sample Mapped Keys (from Text):")
    
    # Manual Fixes for Typos in Text File
    manual_fixes = {
        "annapureddipally": "annapureddypalli",
        "sujathanagar": "sujatha nagur", # Check if this is needed, or just cleaner
        # Add others if found
    }
    
    for (mandal_name, cluster_name), info in raw_data.items():
        # Apply manual fix
        mandal_name = manual_fixes.get(mandal_name, mandal_name)
        
        dist_id = mandal_to_dist.get(mandal_name)
        if dist_id:
            key = (cluster_name, dist_id)
            cluster_dist_map[key] = info
            if mapped < 5:
                print(f"   Key: {key} (Mandal: {mandal_name})")
            mapped += 1
        else:
            if skipped < 5:
                print(f"   Skipped Mandal Lookup: '{mandal_name}'")
            skipped += 1
            
    print(f"Text Data: Mapped {mapped} clusters to districts. Skipped {skipped}.")
    
    # 3. Load Cluster CSV
    cluster_df = pd.read_csv(CLUSTER_CSV, dtype=str)
    print(f"Loaded {len(cluster_df)} clusters from CSV.")
    
    updated_count = 0
    miss_count = 0
    
    # 4. Iterate and Update
    for index, row in cluster_df.iterrows():
        # Clean CSV Data
        c_name = clean_name(row['clustername'])
        d_id = str(row['dist_id']).strip()
        
        # Try Match
        key = (c_name, d_id)
        
        if key in cluster_dist_map:
            info = cluster_dist_map[key]
            cluster_df.at[index, 'incharge_name'] = info['incharge_name']
            cluster_df.at[index, 'mobile_no'] = info['mobile_no']
            updated_count += 1
        else:
            if miss_count < 10:
                print(f"   Miss: CSV Key {key} not found in Text Map.")
            miss_count += 1
            
    print(f"Updated {updated_count} rows in clustermaster. Missed {miss_count} rows.")
    
    # 5. Save
    cluster_df.to_csv(CLUSTER_CSV, index=False)
    print(f"Saved updated CSV to {CLUSTER_CSV}")

if __name__ == "__main__":
    main()
