import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "https://api-veronica.drivex.dev")
API_ENDPOINT = os.getenv("API_ENDPOINT", "/api/v1/analytics")
API_KEY = os.getenv("API_KEY", "")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
API_MAX_RETRIES = int(os.getenv("API_MAX_RETRIES", "3"))
API_RETRY_BACKOFF = float(os.getenv("API_RETRY_BACKOFF", "0.5"))
API_AUTH_METHOD = os.getenv("API_AUTH_METHOD", "X-API-Key")  # Authentication method to use

# Derived values for backward compatibility
API_ENDPOINT_BASE_URL = API_BASE_URL
