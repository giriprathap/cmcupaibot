import pandas as pd

file_path = "data/new data/Disciplines_CMCup_2025.xlsx"

try:
    print(f"Reading {file_path}...")
    xls = pd.ExcelFile(file_path)
    print("Sheet Names:", xls.sheet_names)
    
    sheet = "Discipline_Details"
    print(f"\n--- Analyzing Sheet: {sheet} ---")
    df = pd.read_excel(file_path, sheet_name=sheet, header=None)
    print("Shape:", df.shape)
    print("Rows 0-20:\n", df.head(20).to_string())
    
    # Also print any row that has "District" to find the header
    print("\nSearch for 'District' keyword:")
    for i, row in df.iterrows():
        if i > 20: break
        r_str = " ".join([str(val) for val in row.values])
        if "District" in r_str:
            print(f"Row {i}: {r_str}")
except Exception as e:
    print(f"Error: {e}")
