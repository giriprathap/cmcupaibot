
import pandas as pd
import os

files = [
    "data/csvs/player_details.csv",
    "data/csvs/villagemaster.csv",
    "data/csvs/clustermaster.csv",
    "data/csvs/tb_fixtures.csv",
    "data/csvs/tb_events.csv"
]

for f in files:
    try:
        if os.path.exists(f):
            df = pd.read_csv(f, nrows=0)
            print(f"--- {f} ---")
            print(list(df.columns))
            print("\n")
        else:
            print(f"FILE NOT FOUND: {f}")
    except Exception as e:
        print(f"ERROR reading {f}: {e}")
