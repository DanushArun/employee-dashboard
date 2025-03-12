import requests
import json
from datetime import datetime
import config

# API Configuration
API_ENDPOINT_BASE_URL = config.API_ENDPOINT_BASE_URL
API_KEY = config.API_KEY
API_TIMEOUT = 30  # Increased timeout to 30 seconds

def test_single_endpoint():
    """
    Test a single endpoint with a longer timeout and different auth format
    """
    # Format the API endpoint - try the simplest endpoint
    api_endpoint = f"{API_ENDPOINT_BASE_URL}/api/v1/analytics/records/"
    
    # Use the X-API-Key header method for authentication
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    print(f"\n{'='*80}")
    print(f"Testing endpoint with direct API key")
    print(f"URL: {api_endpoint}")
    print(f"Headers: {headers}")
    print(f"{'='*80}\n")
    
    try:
        # Make the API request with a longer timeout
        response = requests.get(
            api_endpoint, 
            headers=headers, 
            timeout=API_TIMEOUT
        )
        
        # Print status code and reason
        print(f"Status Code: {response.status_code} ({response.reason})")
        
        # Try to parse the response as JSON
        try:
            response_data = response.json()
            print("\nResponse Data:")
            print(json.dumps(response_data, indent=2))
            
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
    print(f"Testing API Endpoint at {API_ENDPOINT_BASE_URL}")
    print(f"Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"API Key: {API_KEY[:5]}...{API_KEY[-5:]}")  # Show only part of the key for security
    
    # Test a single endpoint
    test_single_endpoint()
    
    print("\nAPI testing completed.")
