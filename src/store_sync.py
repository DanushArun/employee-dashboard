import json
import requests
import config
from datetime import datetime
import streamlit as st
from time import sleep

def fetch_stores_from_api(max_retries=3, retry_delay=2):
    """Fetch stores from the API endpoint with retry mechanism"""
    api_endpoint = f"{config.API_BASE_URL}/api/v1/analytics/stores/"
    
    headers = {
        "X-API-Key": config.API_KEY,
        "Content-Type": "application/json"
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.get(
                api_endpoint,
                headers=headers,
                timeout=config.API_TIMEOUT
            )
            response.raise_for_status()
            return response.json().get('data', [])
        except requests.exceptions.ConnectionError:
            if attempt < max_retries - 1:
                sleep(retry_delay)
                continue
            st.warning("⚠️ Unable to connect to the server. Please check your internet connection.")
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                sleep(retry_delay)
                continue
            st.warning("⚠️ Request timed out. The server might be experiencing high load.")
        except requests.exceptions.HTTPError as e:
            if attempt < max_retries - 1:
                sleep(retry_delay)
                continue
            st.warning(f"⚠️ Server returned an error: {e.response.status_code}")
        except Exception as e:
            if attempt < max_retries - 1:
                sleep(retry_delay)
                continue
            st.warning("⚠️ Unable to fetch store data. Using cached data.")
        return None

def update_stores_file(api_stores):
    """Update the local stores.json file with new store data"""
    if api_stores is None:
        return False
        
    try:
        # Read current stores
        with open('data/stores.json', 'r') as f:
            current_data = json.load(f)
            
        # Get current store IDs
        current_store_ids = {store['store_id'] for store in current_data['stores']}
        
        # Get new store IDs
        new_store_ids = {store['store_id'] for store in api_stores}
        
        # Check if there are any changes
        if current_store_ids == new_store_ids:
            return False
            
        # Update the stores file
        current_data['stores'] = api_stores
        with open('data/stores.json', 'w') as f:
            json.dump(current_data, f, indent=2)
            
        # Log changes
        added = new_store_ids - current_store_ids
        removed = current_store_ids - new_store_ids
        if added:
            st.success(f"✅ New stores added: {', '.join(added)}")
        if removed:
            st.info(f"ℹ️ Stores removed: {', '.join(removed)}")
            
        return True
    except Exception as e:
        st.warning("⚠️ Unable to update store data. Using existing data.")
        return False

def sync_stores():
    """Synchronize stores with the API"""
    api_stores = fetch_stores_from_api()
    if api_stores:
        return update_stores_file(api_stores)
    return False