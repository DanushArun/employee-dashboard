import requests
import json
from datetime import datetime
import config

# API Configuration
API_ENDPOINT_BASE_URL = config.API_ENDPOINT_BASE_URL
API_KEY = config.API_KEY
API_TIMEOUT = config.API_TIMEOUT

# Load store data to get a valid store_id
def load_store_id():
    try:
        with open('data/stores.json', 'r') as f:
            data = json.load(f)
            if data['stores'] and len(data['stores']) > 0:
                return data['stores'][0]['store_id']
            else:
                return "59"  # Default to store_id 59 if no stores found
    except Exception as e:
        print(f"Error loading store data: {e}")
        return "59"  # Default to store_id 59 if file can't be loaded

def test_store_metrics_endpoint():
    """
    Test the Store Metrics endpoint with different authentication methods
    """
    store_id = load_store_id()
    date = datetime.now().strftime("%Y-%m-%d")
    
    # Format the API endpoint with from_date and to_date parameters
    api_endpoint = f"{API_ENDPOINT_BASE_URL}/api/v1/analytics/stores/metrics/?store_id={store_id}&from_date={date}&to_date={date}"
    
    # Try different authentication methods
    auth_methods = [
        {
            "name": "Api-Key in Authorization header",
            "headers": {
                "Authorization": f"Api-Key {API_KEY}",
                "Content-Type": "application/json"
            },
            "params": {}
        },
        {
            "name": "Bearer token in Authorization header",
            "headers": {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            "params": {}
        },
        {
            "name": "X-API-Key header",
            "headers": {
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            },
            "params": {}
        },
        {
            "name": "API key as query parameter",
            "headers": {
                "Content-Type": "application/json"
            },
            "params": {
                "api_key": API_KEY
            }
        }
    ]
    
    for auth_method in auth_methods:
        print(f"\n{'='*80}")
        print(f"Testing Store Metrics Endpoint with {auth_method['name']}")
        
        # Add params to URL if any
        test_url = api_endpoint
        if auth_method['params']:
            param_str = '&'.join([f"{k}={v}" for k, v in auth_method['params'].items()])
            test_url = f"{api_endpoint}&{param_str}"
        
        print(f"URL: {test_url}")
        print(f"Headers: {auth_method['headers']}")
        print(f"{'='*80}\n")
        
        try:
            # Make the API request
            response = requests.get(
                test_url, 
                headers=auth_method['headers'], 
                timeout=API_TIMEOUT
            )
            
            # Print status code and reason
            print(f"Status Code: {response.status_code} ({response.reason})")
            
            # Try to parse the response as JSON
            try:
                response_data = response.json()
                print("\nResponse Data:")
                print(json.dumps(response_data, indent=2))
                
                # Check if the API returned a success status
                if response.status_code == 200:
                    if response_data.get("status") == "success":
                        print("\n✅ API request successful!")
                    else:
                        print(f"\n⚠️ API returned non-success status: {response_data.get('status')}")
                else:
                    print(f"\n❌ API request failed with status code: {response.status_code}")
                    
            except ValueError:
                print("\nResponse is not valid JSON. Raw response:")
                print(response.text[:1000])  # Print first 1000 chars to avoid overwhelming output
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out. The server took too long to respond.")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error. Could not connect to the API server.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

def test_list_records_endpoint():
    """
    Test the List Records endpoint with different authentication methods
    """
    # Format the API endpoint
    api_endpoint = f"{API_ENDPOINT_BASE_URL}/api/v1/analytics/records/"
    
    # Try different authentication methods
    auth_methods = [
        {
            "name": "Api-Key in Authorization header",
            "headers": {
                "Authorization": f"Api-Key {API_KEY}",
                "Content-Type": "application/json"
            },
            "params": {}
        },
        {
            "name": "Bearer token in Authorization header",
            "headers": {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            "params": {}
        },
        {
            "name": "X-API-Key header",
            "headers": {
                "X-API-Key": API_KEY,
                "Content-Type": "application/json"
            },
            "params": {}
        },
        {
            "name": "API key as query parameter",
            "headers": {
                "Content-Type": "application/json"
            },
            "params": {
                "api_key": API_KEY
            }
        }
    ]
    
    for auth_method in auth_methods:
        print(f"\n{'='*80}")
        print(f"Testing List Records Endpoint with {auth_method['name']}")
        
        # Add params to URL if any
        test_url = api_endpoint
        if auth_method['params']:
            param_str = '&'.join([f"{k}={v}" for k, v in auth_method['params'].items()])
            test_url = f"{api_endpoint}?{param_str}"
        
        print(f"URL: {test_url}")
        print(f"Headers: {auth_method['headers']}")
        print(f"{'='*80}\n")
        
        try:
            # Make the API request
            response = requests.get(
                test_url, 
                headers=auth_method['headers'], 
                timeout=API_TIMEOUT
            )
            
            # Print status code and reason
            print(f"Status Code: {response.status_code} ({response.reason})")
            
            # Try to parse the response as JSON
            try:
                response_data = response.json()
                print("\nResponse Data:")
                print(json.dumps(response_data, indent=2))
                
                # Check if the API returned a success status
                if response.status_code == 200:
                    if response_data.get("status") == "success":
                        print("\n✅ API request successful!")
                    else:
                        print(f"\n⚠️ API returned non-success status: {response_data.get('status')}")
                else:
                    print(f"\n❌ API request failed with status code: {response.status_code}")
                    
            except ValueError:
                print("\nResponse is not valid JSON. Raw response:")
                print(response.text[:1000])  # Print first 1000 chars to avoid overwhelming output
                
        except requests.exceptions.Timeout:
            print("❌ Request timed out. The server took too long to respond.")
        except requests.exceptions.ConnectionError:
            print("❌ Connection error. Could not connect to the API server.")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    print(f"Testing API Endpoints at {API_ENDPOINT_BASE_URL}")
    print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {API_KEY[:5]}...{API_KEY[-5:]}")  # Show only part of the key for security
    
    # Test the Store Metrics endpoint
    test_store_metrics_endpoint()
    
    # Test the List Records endpoint
    test_list_records_endpoint()
    
    print("\nAPI testing completed.")
