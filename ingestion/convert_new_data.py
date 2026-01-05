
import os
import glob
import pandas as pd

SOURCE_DIR = "data/new data"
OUTPUT_FILE = "data/mdFiles/CM_Cup_2025_New_Data.md"

def convert_to_markdown():
    print(f"🚀 Starting conversion from '{SOURCE_DIR}' to '{OUTPUT_FILE}'...")
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        # Header
        outfile.write("# CM Cup 2025: Supplementary Rules, Schedules, and Contact Info\n\n")
        outfile.write("> **Note:** This document is automatically aggregated from various source files (Text & Excel).\n\n")

        # 1. Process Text Files
        txt_files = glob.glob(os.path.join(SOURCE_DIR, "*.txt"))
        for txt_path in txt_files:
            filename = os.path.basename(txt_path)
            print(f"📄 Processing Text File: {filename}")
            
            outfile.write(f"## Source Document: {filename}\n\n")
            try:
                with open(txt_path, "r", encoding="utf-8") as infile:
                    content = infile.read()
                    outfile.write(content + "\n\n")
                    outfile.write("---\n\n")
            except Exception as e:
                print(f"❌ Error reading {filename}: {e}")

        # 2. Process Excel File
        xlsx_files = glob.glob(os.path.join(SOURCE_DIR, "*.xlsx"))
        for xlsx_path in xlsx_files:
            filename = os.path.basename(xlsx_path)
            print(f"📊 Processing Excel File: {filename}")
            
            outfile.write(f"## Source Data: {filename}\n\n")
            
            try:
                xls = pd.ExcelFile(xlsx_path)
                for sheet_name in xls.sheet_names:
                    print(f"   ➡ Sheet: {sheet_name}")
                    df = pd.read_excel(xlsx_path, sheet_name=sheet_name)
                    
                    outfile.write(f"### Sheet: {sheet_name}\n\n")
                    
                    # Heuristic: If it looks like cluster data, format nicely
                    if "cluster" in sheet_name.lower():
                        outfile.write("#### Cluster Mappings\n")
                        # Iterate rows
                        for idx, row in df.iterrows():
                            # Dynamically build string based on available columns
                            # Expected: clust_id, dist_id, mandalname, clustername (maybe mapped from id?), incharge?
                            # Let's just dump the row as a list item
                            line_items = []
                            for col in df.columns:
                                val = str(row[col]).strip()
                                if val and val.lower() != "nan":
                                    line_items.append(f"**{col}:** {val}")
                            
                            if line_items:
                                outfile.write("- " + ", ".join(line_items) + "\n")
                        outfile.write("\n")
                        
                    elif "discipline" in sheet_name.lower():
                        outfile.write("#### Disciplines & Details\n")
                        # Dump as table or list? List is often better for RAG chunks than wide tables.
                        for idx, row in df.iterrows():
                            line_items = []
                            for col in df.columns:
                                val = str(row[col]).strip()
                                if val and val.lower() != "nan":
                                    # Basic cleanup
                                    val = val.replace("\n", " ") 
                                    line_items.append(f"**{col}:** {val}")
                             
                            if line_items:
                                outfile.write("- " + "; ".join(line_items) + "\n")
                        outfile.write("\n")
                    else:
                        # Generic fallback: Markdown Table
                        if len(df) > 0:
                            outfile.write(df.to_markdown(index=False))
                            outfile.write("\n\n")
                            
                    outfile.write("---\n\n")
                    
            except Exception as e:
                print(f"❌ Error processing Excel {filename}: {e}")

    print(f"✅ Conversion Complete! Created: {OUTPUT_FILE}")

if __name__ == "__main__":
    convert_to_markdown()
