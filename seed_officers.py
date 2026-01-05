import pandas as pd
import os

# Paths
dist_master_path = "data/csvs/districtmaster.csv"
output_path = "data/csvs/tb_district_officers.csv"

if os.path.exists(dist_master_path):
    print("Reading District Master...")
    df_dist = pd.read_csv(dist_master_path)
    
    # Normalize columns
    df_dist.columns = df_dist.columns.str.strip().str.lower()
    
    # Create Officers DataFrame
    df_officers = pd.DataFrame()
    df_officers['district_name'] = df_dist['districtname']
    df_officers['special_officer_name'] = "To Be Updated"
    df_officers['contact_no'] = "To Be Updated"
    df_officers['designation'] = "Special Officer"
    
    # Save
    df_officers.to_csv(output_path, index=False)
    print(f"Created {output_path} with {len(df_officers)} rows.")
else:
    print("District Master not found!")
