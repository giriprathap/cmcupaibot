import pandas as pd
import os

file_path = "data/new data/MANDAL LEVEL CLUSTER INCHARGE NAME & PH.NO.xlsx"

try:
    # Load raw
    df = pd.read_excel(file_path, header=None)
    
    # Header is at Row 4 (Index 4). Data starts Row 5.
    start_row = 5
        
    output_text = "CM Cup 2025 Mandal Level Cluster Incharge Details:\n\n"
    count = 0
    
    current_mandal = "N/A"
    
    # Load with header at row 3 (0-indexed, so row 4 in Excel)
    df = pd.read_excel(file_path, header=3)
    
    # Identify relevant columns by index (approximate based on inspection)
    # The user script used indices: 1 (Mandal), 4 (Cluster/GP), 5 (Incharge), 6 (Contact)
    # Let's verify column names or use iloc if names are unstable.
    
    # Select columns by integer location to be safe
    # Col 1: Name of the Mandal
    # Col 3: Name of the Clusters (Wait, user script used index 4 for Cluster? Let's check user image)
    # Image: 
    # Col 0: Sl No
    # Col 1: Name of the Mandal
    # Col 2: No of Clusters
    # Col 3: Name of the Clusters (This is the Merged Group Name? e.g. Dammata)
    # Col 4: GP's Name (Akinepalli, etc) -> This is likely what is unique per row
    # Col 5: In charge name
    # Col 6: Contact Number
    
    # User's script used:
    # m_val = row[1] (Mandal)
    # cluster = row[4] (This seems to be GP Name based on valid data "Akinepalli")
    # incharge = row[5]
    # contact = row[6]
    
    # STRATEGY:
    # 1. Forward Fill Mandal (Col 1), Cluster Group (Col 3), Incharge (Col 5), Contact (Col 6)
    # 2. Iterate rows where GP Name (Col 4) is not Na/Null
    
    # Convert to numeric indices for easy handling
    df.iloc[:, 1] = df.iloc[:, 1].ffill() # Mandal
    df.iloc[:, 3] = df.iloc[:, 3].ffill() # Cluster Group Name (Dammata)
    df.iloc[:, 5] = df.iloc[:, 5].ffill() # Incharge
    df.iloc[:, 6] = df.iloc[:, 6].ffill() # Contact
    
    output_text = "CM Cup 2025 Mandal Level Cluster Incharge Details:\n\n"
    count = 0
    
    for i in range(len(df)):
        row = df.iloc[i]
        
        # GP Name is at index 4
        gp_name = row.iloc[4]
        
        # Skip if GP Name is empty (it's likely a header row repetition or empty line)
        if pd.isna(gp_name) or str(gp_name).strip() == '':
            continue
            
        mandal = str(row.iloc[1]).strip()
        # The user was using 'Cluster' to mean GP Name in the text output?
        # "Mandal: Dammapeta | Cluster: Akinepalli..." -> Akinepalli is GP.
        # So we use GP Name as 'Cluster' in the string.
        
        incharge = str(row.iloc[5]).strip().replace('\n', ' ')
        contact = str(row.iloc[6]).strip()
        
        # Clean up "nan" strings
        if incharge.lower() == 'nan': incharge = "N/A"
        if contact.lower() == 'nan': contact = "N/A"
        
        line = f"Mandal: {mandal} | Cluster: {gp_name} | Incharge Details: {incharge} | Contact: {contact}"
        output_text += line + "\n"
        count += 1

    # Save
    output_path = "data/new data/Mandal_Incharges_Cleaned.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_text)
        
    print(f"\n✅ Converted {count} rows. Saved to: {output_path}")
    print("Sample:\n" + output_text[:300])

except Exception as e:
    print(f"Error: {e}")
