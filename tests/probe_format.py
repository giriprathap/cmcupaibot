import os

files = ["data/mdFiles/rag_villages.md", "data/mdFiles/rag_events.md"]

for fp in files:
    print(f"--- HEAD of {fp} ---")
    if os.path.exists(fp):
        with open(fp, "r", encoding="utf-8") as f:
            for i in range(10):
                print(repr(f.readline()))
    else:
        print("File not found.")
