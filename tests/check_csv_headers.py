import pandas as pd
import os

CSV_DIR = r"c:\Users\Rishabh\Desktop\RISHABH AI LEARNING\rag-chatbot\data\csvs"
files = ["mandalmaster.csv", "districtmaster.csv", "villagemaster.csv", "clustermaster.csv", "tb_discipline.csv"]

for f in files:
    try:
        path = os.path.join(CSV_DIR, f)
        df = pd.read_csv(path)
        print(f"--- {f} ---")
        print(list(df.columns))
    except Exception as e:
        print(f"Error reading {f}: {e}")
