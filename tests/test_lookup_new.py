
import sys
import os
import pandas as pd

# Add project root to path
sys.path.append(os.getcwd())

from rag.lookup import get_player_by_phone, get_player_by_reg_id

def test_lookup():
    print("=== TESTING LOOKUP LOGIC ===")
    
    # 1. Load a real player to test with
    csv_path = "data/csvs/player_details.csv"
    if not os.path.exists(csv_path):
        print("❌ Player CSV not found, skipping extraction test.")
        return

    try:
        df = pd.read_csv(csv_path, dtype=str)
        # normalize
        df.columns = df.columns.str.strip().str.lower()
        
        if df.empty:
            print("⚠️ CSV is empty.")
            return

        # Pick a row with a phone number
        valid_row = df[df['mobile_no'].notna() & (df['mobile_no'] != '')].iloc[0]
        phone = valid_row['mobile_no']
        reg_id = valid_row.get('player_reg_id', 'N/A')
        
        print(f"🧪 Testing with Player: {valid_row.get('player_nm')} (Phone: {phone}, RegID: {reg_id})")
        
        # 2. Test Phone Lookup
        print("\n--- PHONE LOOKUP ---")
        res_phone = get_player_by_phone(phone)
        print(res_phone)
        
        if "No Record" in res_phone:
            print("❌ Phone Lookup Failed (Unexpected)")
        else:
            print("✅ Phone Lookup Success")

        # 3. Test Reg ID Lookup
        if reg_id != 'N/A':
            print("\n--- REG ID LOOKUP ---")
            res_reg = get_player_by_reg_id(reg_id)
            print(res_reg)
            
            if "No Record" in res_reg:
                 print("❌ Reg ID Lookup Failed (Unexpected)")
            else:
                 print("✅ Reg ID Lookup Success")
        else:
            print("⚠️ No Reg ID available to test.")
            
    except Exception as e:
        print(f"❌ Test Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_lookup()
