import pandas as pd
import os

file_path = "data/new data/MANDAL LEVEL CLUSTER INCHARGE NAME & PH.NO.xlsx"

if os.path.exists(file_path):
    print(f"Loading {file_path}...")
    try:
        xl = pd.ExcelFile(file_path)
        print("Sheet Names:", xl.sheet_names)
        
        for sheet in xl.sheet_names:
            print(f"\n--- Sheet: {sheet} ---")
            df = xl.parse(sheet)
            print("Columns:", df.columns.tolist())
            print(df.head(3))
            
            # Check for keywords
            if any("officer" in str(c).lower() or "special" in str(c).lower() for c in df.columns):
                print(">>> POTENTIAL MATCH FOUND <<<")
            
    except Exception as e:
        print(f"Error reading excel: {e}")
else:
    print("File not found.")
