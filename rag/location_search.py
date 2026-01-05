from rag.data_store import get_datastore
import pandas as pd
import os

def search_district_officer(district_name):
    """
    Search for Special Officers by District Name using users (1).csv and districtmaster.csv.
    """
    try:
        # Load Data
        users_path = "data/new data/users (1).csv"
        dist_map_path = "data/csvs/districtmaster.csv"
        
        if not os.path.exists(users_path) or not os.path.exists(dist_map_path):
             return None
             
        df_users = pd.read_csv(users_path)
        df_dist = pd.read_csv(dist_map_path)
        
        # Clean District Names for matching
        df_dist['DistrictName_clean'] = df_dist['DistrictName'].astype(str).str.strip().str.lower()
        query_dist = district_name.strip().lower()
        
        # Find District ID
        dist_match = df_dist[df_dist['DistrictName_clean'] == query_dist]
        
        if dist_match.empty:
            # Try fuzzy match if exact match fails
            import difflib
            all_dists = df_dist['DistrictName_clean'].tolist()
            matches = difflib.get_close_matches(query_dist, all_dists, n=1, cutoff=0.7)
            if matches:
                dist_match = df_dist[df_dist['DistrictName_clean'] == matches[0]]
            else:
                return None
                
        dist_id = dist_match.iloc[0]['DistrictNo']
        real_dist_name = dist_match.iloc[0]['DistrictName']
        
        # Filter Users for this District and Role (DYSO = 2)
        # Note: 'dyso_dist' in users matches 'DistrictNo'
        officer = df_users[
            (df_users['dyso_dist'] == dist_id) & 
            (df_users['role_id'] == 2)
        ]
        
        if officer.empty:
            return {
                "district_name": real_dist_name, 
                "special_officer_name": "Not Assigned", 
                "contact_no": "N/A", 
                "designation": "District Sports Officer"
            }
            
        rec = officer.iloc[0]
        return {
            "district_name": real_dist_name,
            "special_officer_name": rec['name'],
            "contact_no": str(rec['dyso_cont_no']),
            "designation": rec['dyso_dept'] # Using department/designation field
        }

    except Exception as e:
        print(f"Error in search_district_officer: {e}")
        return None

def search_cluster_incharge(query_name):
    """
    Search for Cluster In-charge details.
    Logic:
    1. Try to find the input as a Cluster Name.
    2. If not found, try to find the input as a Village Name, map to Cluster, then find Cluster.
    """
    ds = get_datastore()
    if not ds.initialized:
        ds.init_db()
        
    q_str = query_name.strip().lower()
    
    # 1. Direct Cluster Search
    sql_cluster = """
    SELECT clustername, incharge_name, mobile_no
    FROM clustermaster
    WHERE LOWER(clustername) LIKE ?
    """
    df_cluster = ds.query(sql_cluster, (f"%{q_str}%",))
    
    if not df_cluster.empty:
        return {
            "type": "Cluster",
            "data": df_cluster.to_dict(orient="records")[0]
        }
        
    # 2. Village Mapping Search
    # Find village, get cluster_id, then get cluster info
    sql_village = """
    SELECT v.villagename, c.clustername, c.incharge_name, c.mobile_no
    FROM villagemaster v
    JOIN clustermaster c ON v.cluster_id = c.cluster_id
    WHERE LOWER(v.villagename) LIKE ?
    """
    df_village = ds.query(sql_village, (f"%{q_str}%",))
    
    if not df_village.empty:
        return {
            "type": "Village",
            "mapped_cluster": df_village.iloc[0]['clustername'],
            "data": df_village.to_dict(orient="records")[0]
        }
        
    return None
