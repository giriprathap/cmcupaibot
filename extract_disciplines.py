import pandas as pd
import re

file_path = "data/new data/Disciplines_CMCup_2025.xlsx"
sheet_name = "Discipline_Details"

try:
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    
    levels = {
        "GP/Cluster": "GP Level",
        "Mandal": "Mandal Level",
        "Assembly": "Assembly Consituency Level",
        "District": "District Level",
        "State": "State Level"
    }
    
    output_text = "CM Cup 2025 Disciplines by Level:\n\n"
    
    for col, level_name in levels.items():
        if col in df.columns:
            # Extract list
            raw_list = df[col].dropna().astype(str).tolist()
            
            # Clean list: Remove "1. ", "2. ", etc.
            clean_list = []
            for item in raw_list:
                # Remove leading numbers and dots (e.g. "1. Athletics" -> "Athletics")
                item = re.sub(r'^\d+\.\s*', '', item).strip()
                if item and item.lower() != 'nan':
                    clean_list.append(item)
            
            # Remove duplicates and sort
            clean_list = sorted(list(set(clean_list)))
            
            list_str = ", ".join(clean_list)
            output_text += f"{level_name} Disciplines included are: {list_str}.\n\n"
            
    print(output_text)
    
    with open("data/new data/Disciplines_Cleaned.txt", "w", encoding="utf-8") as f:
        f.write(output_text)
        
    print("✅ Saved to data/new data/Disciplines_Cleaned.txt")

except Exception as e:
    print(f"Error: {e}")
