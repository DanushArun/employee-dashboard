import streamlit as st
import pandas as pd
import json
import datetime
import requests
from PIL import Image
import os
import io
import base64
from datetime import datetime, timedelta
import config

# Page config
st.set_page_config(
    page_title="Veronica Admin Dashboard",
    page_icon="src/assets/drivex-logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS with Google Fonts import
st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main theme colors */
    :root {
        --background-color: #000000;
        --accent-color: #8A2BE2;
        --text-color: #FFFFFF;
        --card-bg: #1C1C1C;
        --hover-bg: #2D2D2D;
        --purple-glass: rgba(75, 0, 130, 0.7);
        --button-color: #9370DB;
        --title-font: 'Orbitron', sans-serif; /* Digital/tech font for titles */
        --body-font: 'Inter', sans-serif; /* Clean sans-serif for body text */
    }
    
    .stApp {
        background-color: var(--background-color);
        font-family: var(--body-font);
    }
    
    /* Header with glass effect */
    .header-container {
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.3) 0%, rgba(45, 0, 75, 0.5) 100%);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 12px 32px rgba(75, 0, 130, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.08);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top right, rgba(138, 43, 226, 0.1), transparent 70%), 
                  radial-gradient(circle at bottom left, rgba(75, 0, 130, 0.1), transparent 70%);
        z-index: 0;
        pointer-events: none;
    }
    
    .header-container::after {
        content: "";
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: linear-gradient(45deg, 
                  rgba(255, 255, 255, 0) 0%, 
                  rgba(255, 255, 255, 0.03) 50%, 
                  rgba(255, 255, 255, 0) 100%);
        transform: rotate(30deg);
        pointer-events: none;
        z-index: 1;
        left: 0;
        right: 0;
        bottom: 0;
        background: radial-gradient(circle at top right, rgba(255, 255, 255, 0.15), transparent 70%);
        pointer-events: none;
    }
    
    .header-title {
        color: white;
        font-family: var(--title-font);
        font-size: 1.8rem;
        font-weight: 600;
        margin-left: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Search bar styling */
    .search-container {
        margin-bottom: 1rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    /* Override Streamlit's default input styling */
    .stTextInput {
        width: 100%;
    }
    
    .stTextInput > div {
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.5) 0%, rgba(45, 0, 75, 0.6) 100%) !important;
        border-radius: 25px !important;
        padding: 0 !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 8px 32px rgba(75, 0, 130, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        transition: all 0.3s ease !important;
        position: relative;
        overflow: hidden !important;
    }
    
    .stTextInput > div:hover {
        border: 1px solid rgba(138, 43, 226, 0.4) !important;
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.3) !important;
        transform: translateY(-2px) !important;
    }
    
    .stTextInput > div:focus-within {
        border: 1px solid rgba(138, 43, 226, 0.6) !important;
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.4) !important;
    }
    
    .stTextInput > div > div {
        background-color: transparent !important;
        width: 100% !important;
    }
    
    .stTextInput > div > div > input {
        background-color: transparent !important;
        color: white !important;
        padding: 10px 45px 10px 20px !important;
        border: none !important;
        height: 45px !important;
        font-family: var(--body-font) !important;
        font-size: 1rem !important;
        letter-spacing: 0.5px !important;
        width: 100% !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5) !important;
        font-family: var(--body-font) !important;
        font-weight: 300 !important;
    }
    
    /* Add search icon using pseudo-element with SVG for better styling */
    .stTextInput > div::after {
        content: "";
        position: absolute;
        right: 20px;
        top: 50%;
        transform: translateY(-50%);
        width: 18px;
        height: 18px;
        background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='rgba(255, 255, 255, 0.5)' viewBox='0 0 24 24'%3E%3Cpath d='M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z'/%3E%3C/svg%3E");
        background-repeat: no-repeat;
        background-size: contain;
        z-index: 10;
        pointer-events: none;
    }
    
    /* Hide dropdown menu and all related elements EXCEPT date picker */
    .stSelectbox,
    [data-baseweb="select"],
    [data-baseweb="select-option"],
    [data-baseweb="menu"],
    [data-baseweb="list"],
    .stSelectbox [data-testid="stWidgetLabel"],
    div[data-baseweb="select-dropdown"],
    div[data-baseweb="select-dropdown-container"],
    div[data-baseweb="select-dropdown-listbox"],
    div[data-baseweb="menu"] {
        display: none !important;
        opacity: 0 !important;
        visibility: hidden !important;
        pointer-events: none !important;
        height: 0 !important;
        width: 0 !important;
        overflow: hidden !important;
        position: absolute !important;
        z-index: -1 !important;
    }
    
    /* Ensure date picker popover is visible */
    .stDateInput [data-baseweb="popover"],
    .stDateInput div[data-baseweb="calendar"] {
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
        height: auto !important;
        width: auto !important;
        overflow: visible !important;
        position: absolute !important;
        z-index: 1000 !important;
        background-color: #1A1A1A !important;
    }
    
    /* Store card styling */
    .store-card {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 0.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .store-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    .store-name {
        font-family: var(--body-font);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        color: white;
    }
    
    .store-id {
        font-family: var(--body-font);
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 0;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: rgba(75, 0, 130, 0.2) !important;
        color: white !important;
        border-radius: 4px !important;
        padding: 0.3rem 0.8rem !important;
        font-family: var(--body-font) !important;
        font-weight: 400 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px) !important;
        font-size: 0.9rem !important;
    }
    
    .stButton > button:hover {
        background-color: rgba(75, 0, 130, 0.4) !important;
        transform: translateY(-1px) !important;
    }
    
    /* Enhanced Date picker styling */
    .stDateInput > div {
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.2) 0%, rgba(45, 0, 75, 0.3) 100%) !important;
        border: 1px solid rgba(138, 43, 226, 0.2) !important;
        border-radius: 12px !important;
        min-height: 48px !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        box-shadow: 0 4px 16px rgba(138, 43, 226, 0.1) !important;
    }
    
    .stDateInput > div > div > div > div {
        background-color: transparent !important;
        color: white !important;
        font-family: var(--body-font) !important;
    }
    
    .stDateInput input {
        color: white !important;
        font-family: var(--body-font) !important;
        font-size: 0.9rem !important;
        padding: 8px !important;
    }
    
    /* Remove all purple outlines and borders from date picker - more comprehensive */
    .stDateInput > div:focus-within,
    .stDateInput > div:hover,
    .stDateInput > div:active,
    .stDateInput > div:focus,
    .stDateInput [data-baseweb="input"]:focus-within,
    .stDateInput [data-baseweb="input"]:hover,
    .stDateInput [data-baseweb="input"]:active,
    .stDateInput [data-baseweb="input"]:focus {
        border: 1px solid rgba(40, 40, 40, 0.8) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2) !important;
        outline: none !important;
    }
    
    /* Remove focus outline from input */
    .stDateInput input:focus,
    .stDateInput [data-baseweb="input"] input:focus,
    .stDateInput [data-baseweb="input"]:focus-within input {
        outline: none !important;
        box-shadow: none !important;
        border-color: transparent !important;
    }
    
    /* Override any BaseWeb styles that might be causing the purple outline */
    [data-baseweb="input"]:focus-within,
    [data-baseweb="base-input"]:focus-within {
        border-color: rgba(40, 40, 40, 0.8) !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Enhanced Calendar styling */
    div[data-baseweb="calendar"],
    div[data-baseweb="popover"] {
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.3) 0%, rgba(45, 0, 75, 0.4) 100%) !important;
        border-radius: 16px !important;
        padding: 16px !important;
        border: 1px solid rgba(138, 43, 226, 0.2) !important;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3) !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        font-family: var(--body-font) !important;
        display: block !important;
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
        height: auto !important;
        width: auto !important;
        overflow: visible !important;
        position: absolute !important;
        z-index: 1000 !important;
    }
    
    div[data-baseweb="calendar"] button,
    div[data-baseweb="popover"] button {
        color: rgba(255, 255, 255, 0.9) !important;
        font-family: var(--body-font) !important;
        font-size: 0.9rem !important;
        border-radius: 8px !important;
        transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        margin: 2px !important;
        width: 36px !important;
        height: 36px !important;
    }
    
    div[data-baseweb="calendar"] button:hover,
    div[data-baseweb="popover"] button:hover {
        background: rgba(138, 43, 226, 0.2) !important;
        color: rgba(255, 255, 255, 1) !important;
        transform: scale(1.1) !important;
    }
    
    div[data-baseweb="calendar"] button[aria-selected="true"],
    div[data-baseweb="popover"] button[aria-selected="true"] {
        background: linear-gradient(135deg, rgba(138, 43, 226, 0.8) 0%, rgba(75, 0, 130, 0.9) 100%) !important;
        color: white !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 12px rgba(138, 43, 226, 0.3) !important;
    }
    
    div[data-baseweb="calendar"] thead button,
    div[data-baseweb="popover"] thead button {
        color: rgba(255, 255, 255, 0.7) !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
        font-size: 0.8rem !important;
    }
    
    div[data-baseweb="calendar"] thead button:hover,
    div[data-baseweb="popover"] thead button:hover {
        background: transparent !important;
        color: rgba(138, 43, 226, 1) !important;
        transform: none !important;
    }
    
    /* Visitor count styling */
    .visitor-count {
        font-family: var(--body-font);
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    
    .visitor-date {
        font-family: var(--body-font);
        color: #00FF00;
        font-size: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* Table styling */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin-bottom: 1rem;
        background-color: #1A1A1A;
        border-radius: 8px;
        overflow: hidden;
        font-family: var(--body-font);
    }
    
    .styled-table th {
        background-color: rgba(75, 0, 130, 0.3);
        color: white;
        padding: 0.75rem;
        text-align: left;
        font-weight: 500;
        font-family: var(--body-font);
    }
    
    .styled-table td {
        padding: 0.75rem;
        border-bottom: 1px solid #333;
        color: white;
        font-family: var(--body-font);
    }
    
    .styled-table tr:last-child td {
        border-bottom: none;
    }
    
    /* Chart styling */
    .stChart {
        margin: 0 !important;
        padding: 0 !important;
        transform: scale(0.95) !important;
    }

    .stChart text {
        fill: white !important;
        font-family: var(--body-font) !important;
        font-size: 6px !important;
        letter-spacing: -0.5px !important;
    }

    .stChart .gtitle,
    .stChart .legend text {
        font-size: 8px !important;
        letter-spacing: -0.4px !important;
    }

    .stChart .xaxislayer-above text,
    .stChart .yaxislayer-above text {
        font-size: 6px !important;
        letter-spacing: -0.5px !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    .stChart .plot-container {
        margin: 0 !important;
        padding: 0 !important;
    }

    .stChart .main-svg {
        transform-origin: center !important;
        margin: -10px !important;
    }
    
    /* Analytics cards */
    .analytics-card {
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.5rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .analytics-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
    }
    
    .analytics-title {
        font-family: var(--title-font);
        color: #888;
        font-size: 0.9rem;
        margin-bottom: 0.25rem;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .analytics-value {
        font-family: var(--body-font);
        font-size: 2.5rem;
        font-weight: 700;
        color: white;
    }
    
    /* Section titles */
    .section-title {
        font-family: var(--title-font);
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Last updated text */
    .last-updated {
        font-family: var(--body-font);
        color: #888;
        font-size: 0.9rem;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    /* Override all text to use our fonts */
    body, p, h1, h2, h3, h4, h5, h6, span, div {
        font-family: var(--body-font);
    }
    
    /* Apply title font to section titles */
    h1, h2, h3.section-title {
        font-family: var(--title-font);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: var(--background-color) !important;
        border-right: 1px solid rgba(75, 0, 130, 0.3) !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h1 {
        color: white !important;
        font-family: var(--title-font) !important;
        font-size: 1.5rem !important;
        margin-bottom: 1rem !important;
        letter-spacing: 1px !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown h2, 
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #CCC !important;
        font-family: var(--title-font) !important;
        font-size: 1rem !important;
        margin-top: 1.5rem !important;
        margin-bottom: 0.5rem !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Checkbox styling */
    [data-testid="stSidebar"] [data-testid="stCheckbox"] {
        accent-color: var(--accent-color) !important;
    }
    
    /* Slider styling */
    [data-testid="stSidebar"] [data-testid="stSlider"] > div > div {
        background-color: rgba(75, 0, 130, 0.3) !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stSlider"] > div > div > div > div {
        background-color: var(--accent-color) !important;
    }
    
    /* Caption styling */
    [data-testid="stSidebar"] .stMarkdown small {
        color: #888 !important;
        font-style: italic !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .analytics-card {
            min-width: 100%;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Load store data
@st.cache_data
def load_stores():
    try:
        with open('data/stores.json', 'r') as f:
            data = json.load(f)
            return data['stores']
    except Exception as e:
        st.error(f"Error loading store data: {e}")
        return []

API_ENDPOINT_BASE_URL = config.API_ENDPOINT_BASE_URL
API_KEY = config.API_KEY
API_TIMEOUT = config.API_TIMEOUT
API_MAX_RETRIES = config.API_MAX_RETRIES
API_RETRY_BACKOFF = config.API_RETRY_BACKOFF

# Initialize session state for refresh tracking and API status
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = datetime.now()
if 'api_status' not in st.session_state:
    st.session_state.api_status = "unknown"  # unknown, connected, error
if 'api_error' not in st.session_state:
    st.session_state.api_error = ""
if 'use_mock_data' not in st.session_state:
    st.session_state.use_mock_data = False  # Default to real API data

# Helper function to get fallback data when API fails
def get_fallback_data():
    """Return fallback data when API fails"""
    return {
        "total_visitors": 0,
        "hourly_breakdown": {
            "10:00-11:00": 0,
            "11:00-12:00": 0,
            "12:00-13:00": 0,
            "13:00-14:00": 0,
            "14:00-15:00": 0,
            "15:00-16:00": 0,
            "16:00-17:00": 0,
            "17:00-18:00": 0,
            "18:00-19:00": 0,
            "19:00-20:00": 0
        },
        "analytics": {
            "unique_visitors": 0,
            "test_ride_count": 0,
            "qr_code_count": 0,
            "callstore_count": 0
        },
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Generate mock data for demo purposes
def get_mock_data(store_id, date):
    """Generate realistic mock data for demo purposes"""
    # Seed the random number generator with the store_id and date for consistent results
    import random
    seed = int(store_id) + int(datetime.strptime(date, "%Y-%m-%d").timestamp())
    random.seed(seed)
    
    # Generate random visitor counts for each hour
    total_visitors = random.randint(50, 200)
    
    # Create hourly breakdown with a realistic distribution
    # Morning hours have fewer visitors, afternoon and evening have more
    hourly_breakdown = {
        "10:00-11:00": random.randint(1, 10),
        "11:00-12:00": random.randint(5, 15),
        "12:00-13:00": random.randint(10, 25),
        "13:00-14:00": random.randint(15, 30),
        "14:00-15:00": random.randint(20, 35),
        "15:00-16:00": random.randint(25, 40),
        "16:00-17:00": random.randint(30, 45),
        "17:00-18:00": random.randint(35, 50),
        "18:00-19:00": random.randint(25, 40),
        "19:00-20:00": random.randint(15, 30)
    }
    
    # Ensure the sum of hourly breakdown is close to total_visitors
    total_hourly = sum(hourly_breakdown.values())
    if total_hourly > 0:  # Avoid division by zero
        scale_factor = total_visitors / total_hourly
        hourly_breakdown = {k: int(v * scale_factor) for k, v in hourly_breakdown.items()}
    
    # Generate analytics data
    test_ride_count = random.randint(int(total_visitors * 0.1), int(total_visitors * 0.3))
    qr_code_count = random.randint(int(total_visitors * 0.2), int(total_visitors * 0.5))
    callstore_count = random.randint(int(total_visitors * 0.05), int(total_visitors * 0.15))
    
    return {
        "total_visitors": total_visitors,
        "hourly_breakdown": hourly_breakdown,
        "analytics": {
            "unique_visitors": total_visitors,
            "test_ride_count": test_ride_count,
            "qr_code_count": qr_code_count,
            "callstore_count": callstore_count
        },
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

# Real API call function with caching
@st.cache_data(ttl=60)  # Cache for 60 seconds
def fetch_store_metrics(store_id, date):
    """
    Fetch store metrics from the API with error handling and retries
    """
    # If using mock data, return mock data instead of making API call
    if st.session_state.use_mock_data:
        st.session_state.api_status = "connected"  # Set status to connected for mock data
        st.session_state.api_error = ""
        return get_mock_data(store_id, date)
    
    # Format the API endpoint with from_date and to_date parameters (both set to the same date)
    api_endpoint = f"{API_ENDPOINT_BASE_URL}/api/v1/analytics/stores/metrics/?store_id={store_id}&from_date={date}&to_date={date}"
    
    # Use the X-API-Key header method for authentication
    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }
    
    try:
        # Create a session with retry capability
        session = requests.Session()
        retry_strategy = requests.packages.urllib3.util.retry.Retry(
            total=API_MAX_RETRIES,
            backoff_factor=API_RETRY_BACKOFF,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = requests.adapters.HTTPAdapter(max_retries=retry_strategy)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Make the API request
        response = session.get(
            api_endpoint, 
            headers=headers, 
            timeout=API_TIMEOUT
        )
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the response
        api_response = response.json()
        
        # Check if the API returned a success status
        if api_response.get("status") != "success":
            error_msg = api_response.get('message', 'Unknown error')
            st.error(f"API Error: {error_msg}")
            st.session_state.api_status = "error"
            st.session_state.api_error = error_msg
            return get_fallback_data()
        
        # Extract and format the data
        data = api_response.get("data", {})
        
        # Format the response to match the expected structure
        formatted_data = {
            "total_visitors": data.get("unique_visitors", 0),
            "hourly_breakdown": get_hourly_breakdown(data),
            "analytics": {
                "unique_visitors": data.get("unique_visitors", 0),
                "test_ride_count": data.get("test_ride", 0),  # API field is test_ride
                "qr_code_count": data.get("qr_code", 0),      # API field is qr_code
                "callstore_count": data.get("call_store", 0)  # API field is call_store
            },
            "last_updated": data.get("last_updated", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        
        # Update API status to connected
        st.session_state.api_status = "connected"
        st.session_state.api_error = ""
        
        return formatted_data
        
    except requests.exceptions.RequestException as e:
        error_msg = str(e)
        st.error(f"API Request Error: {error_msg}")
        st.session_state.api_status = "error"
        st.session_state.api_error = error_msg
        return get_fallback_data()
    except ValueError as e:
        error_msg = str(e)
        st.error(f"JSON Parsing Error: {error_msg}")
        st.session_state.api_status = "error"
        st.session_state.api_error = error_msg
        return get_fallback_data()
    except Exception as e:
        error_msg = str(e)
        st.error(f"Unexpected Error: {error_msg}")
        st.session_state.api_status = "error"
        st.session_state.api_error = error_msg
        return get_fallback_data()

def get_hourly_breakdown(data):
    """
    Extract hourly breakdown from API response or create default structure
    """
    # Create a default structure with all hours set to 0
    default_structure = {
        "10:00-11:00": 0,
        "11:00-12:00": 0,
        "12:00-13:00": 0,
        "13:00-14:00": 0,
        "14:00-15:00": 0,
        "15:00-16:00": 0,
        "16:00-17:00": 0,
        "17:00-18:00": 0,
        "18:00-19:00": 0,
        "19:00-20:00": 0
    }
    
    # If the API provides hourly breakdown in the old format, use it
    if "hourly_breakdown" in data:
        return data["hourly_breakdown"]
    
    # If the API provides hourly data in the new format, convert it
    if "hourly_data" in data:
        hourly_data = data["hourly_data"]
        result = default_structure.copy()
        
        # Map from API format (e.g., "10-11") to dashboard format (e.g., "10:00-11:00")
        for hour_range, values in hourly_data.items():
            if isinstance(values, list) and len(values) > 0:
                # Extract the visitor count (first element in the list)
                visitor_count = values[0]
                
                # Convert hour format: "10-11" -> "10:00-11:00"
                start_hour, end_hour = hour_range.split("-")
                formatted_hour_range = f"{start_hour}:00-{end_hour}:00"
                
                # Update the result with the actual value
                if formatted_hour_range in result:
                    result[formatted_hour_range] = visitor_count
        
        return result
    
    # Otherwise, return the default structure
    return default_structure

# Main function
def main():
    # Add sidebar for settings
    with st.sidebar:
        st.title("Settings")
        
        # Data Source toggle
        st.subheader("Data Source")
        use_mock = st.checkbox("Use Demo Data", value=st.session_state.use_mock_data, 
                              help="Toggle between real API data and demo data")
        if use_mock != st.session_state.use_mock_data:
            st.session_state.use_mock_data = use_mock
            # Clear cache to force refresh with new data source
            fetch_store_metrics.clear()
            st.rerun()
        
        # Add note about demo mode
        if st.session_state.use_mock_data:
            st.markdown("""
                <div style="font-size: 0.8rem; color: #FFA500; margin-bottom: 1rem; padding: 8px; border-radius: 4px; background-color: rgba(255, 165, 0, 0.1); border: 1px solid rgba(255, 165, 0, 0.3);">
                    <strong>Demo Mode:</strong> Using realistic mock data since the API is currently unavailable.
                </div>
            """, unsafe_allow_html=True)
        
        # API Status indicator
        st.subheader("API Status")
        
        # Display API status with appropriate color
        if st.session_state.api_status == "connected":
            st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #00FF00; margin-right: 8px;"></div>
                    <span style="color: #00FF00; font-weight: 500;">Connected</span>
                </div>
            """, unsafe_allow_html=True)
        elif st.session_state.api_status == "error":
            st.markdown(f"""
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #FF4757; margin-right: 8px;"></div>
                    <span style="color: #FF4757; font-weight: 500;">Error</span>
                </div>
                <div style="font-size: 0.8rem; color: #FF4757; margin-bottom: 1rem; opacity: 0.8; overflow-wrap: break-word;">
                    {st.session_state.api_error}
                </div>
            """, unsafe_allow_html=True)
        else:  # unknown
            st.markdown("""
                <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                    <div style="width: 12px; height: 12px; border-radius: 50%; background-color: #FFA500; margin-right: 8px;"></div>
                    <span style="color: #FFA500; font-weight: 500;">Unknown</span>
                </div>
            """, unsafe_allow_html=True)
        
        # Auto-refresh settings
        st.subheader("Data Refresh")
        auto_refresh = st.checkbox("Auto-refresh data", value=True)
        refresh_interval = st.slider("Refresh interval (seconds)", 
                                    min_value=10, 
                                    max_value=300, 
                                    value=60,
                                    step=10)
        
        # Manual refresh button
        if st.button("Refresh Now", use_container_width=True):
            st.session_state.last_refresh = datetime.now()
            st.rerun()
        
        # Display last refresh time
        st.caption(f"Last refreshed: {st.session_state.last_refresh.strftime('%H:%M:%S')}")
    
    # Check if it's time to auto-refresh
    if auto_refresh and (datetime.now() - st.session_state.last_refresh).total_seconds() > refresh_interval:
        st.session_state.last_refresh = datetime.now()
        st.rerun()
    
    # Check if we're in the store detail view
    if 'store_id' in st.session_state and st.session_state.store_id:
        show_store_detail(st.session_state.store_id)
    else:
        show_main_page()

def show_main_page():
    # Header with logo and title
    try:
        logo = Image.open('src/assets/drivex-logo.png')
        logo_bytes = io.BytesIO()
        logo.save(logo_bytes, format='PNG')
        logo_base64 = base64.b64encode(logo_bytes.getvalue()).decode()
        
        st.markdown(f"""
            <div class="header-container">
                <img src="data:image/png;base64,{logo_base64}" alt="DriveX Logo" width="150">
                <h1 class="header-title">Veronica Admin Dashboard</h1>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Error loading logo: {e}")
        st.markdown("""
            <div class="header-container">
                <h1 class="header-title">Veronica Admin Dashboard</h1>
            </div>
        """, unsafe_allow_html=True)
    
    # Search bar
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    search = st.text_input("Search", placeholder="Search stores by name...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Load stores
    stores = load_stores()
    
    # Filter stores based on search
    if search:
        filtered_stores = [store for store in stores if search.lower() in store['name'].lower()]
    else:
        filtered_stores = stores
    
    # Create a container for the store cards grid
    st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
    
    # Create a layout with 2 columns - left column for grid (75% width) and right column empty (25% width)
    # This pushes the content to the left side of the page
    left_col, _ = st.columns([3, 1])
    
    with left_col:
        # Chunk the stores list into groups of 3 for the grid
        store_chunks = [filtered_stores[i:i+3] for i in range(0, len(filtered_stores), 3)]
        
        # For each row of stores
        for chunk in store_chunks:
            # Create 3 columns for the stores in this row
            cols = st.columns(3)
            
            # For each store in this row
            for i, store in enumerate(chunk):
                with cols[i]:
                    # Store card
                    st.markdown(f"""
                        <div class="store-card">
                            <div class="store-name">{store['name']}</div>
                            <div class="store-id">ID: {store['store_id']}</div>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # View Analytics button
                    if st.button("View Analytics", key=f"view_{store['store_id']}", use_container_width=True):
                        st.session_state.store_id = store['store_id']
                        st.session_state.store_name = store['name']
                        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_store_detail(store_id):
    # Get store name
    store_name = st.session_state.get('store_name', 'Store')
    
    # Back button with custom styling - translucent glass effect
    if st.button("← Back", key="back_button"):
        st.session_state.store_id = None
        st.rerun()
    
    # Header with logo and store name
    try:
        logo = Image.open('src/assets/drivex-logo.png')
        logo_bytes = io.BytesIO()
        logo.save(logo_bytes, format='PNG')
        logo_base64 = base64.b64encode(logo_bytes.getvalue()).decode()
        
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                <img src="data:image/png;base64,{logo_base64}" alt="DriveX Logo" width="100">
                <h2 style="margin-left: 1rem; font-family: var(--title-font); font-size: 1.5rem;">{store_name}</h2>
            </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.markdown(f"""
            <div style="display: flex; align-items: center; margin-top: 0.5rem; margin-bottom: 0.5rem;">
                <h2 style="font-family: var(--title-font); font-size: 1.5rem;">{store_name}</h2>
            </div>
        """, unsafe_allow_html=True)
    
    # Create a modern glass-morphic date picker container
    st.markdown("""<div style="display: flex; align-items: center; gap: 1rem; margin: 1rem 0;">
        <span style="margin-top: 0.5rem; margin-bottom: 0.25rem; font-family: var(--title-font); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: #888888;">DATE</span>
        <div style="flex: 1; max-width: 150px;">""", unsafe_allow_html=True)
    
    selected_date = st.date_input(
        "Select Date",
        datetime(2025, 3, 5),  # Set default date to March 5th, 2025
        label_visibility="collapsed",
        key="modern_date_picker"
    )
    
    st.markdown("""</div></div>""", unsafe_allow_html=True)
    
    # Add custom CSS for the date picker
    st.markdown("""
    <style>
    .date-picker-container {
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.2) 0%, rgba(45, 0, 75, 0.3) 100%);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px rgba(75, 0, 130, 0.2);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .date-label {
        font-family: var(--title-font);
        font-size: 0.75rem;
        color: rgba(255, 255, 255, 0.7);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    /* Modern date input styling */
    .stDateInput > div {
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.3) 0%, rgba(45, 0, 75, 0.4) 100%) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        transition: all 0.3s ease !important;
    }
    
    .stDateInput > div:hover {
        border-color: var(--accent-color) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2) !important;
    }
    
    .stDateInput input {
        color: var(--text-color) !important;
        font-family: var(--body-font) !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.5px !important;
        padding: 0.75rem 1rem !important;
    }
    
    div[data-baseweb="calendar"] {
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.3) 0%, rgba(45, 0, 75, 0.4) 100%) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 8px 32px rgba(75, 0, 130, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Format date for API call
    formatted_date = selected_date.strftime("%Y-%m-%d")
    
    # Fetch metrics with loading indicator
    with st.spinner("Fetching real-time data..."):
        metrics = fetch_store_metrics(store_id, formatted_date)
    
    # Section divider
    st.markdown('<hr style="border: 0; height: 1px; background: rgba(75, 0, 130, 0.7); margin: 0.5rem 0;">', unsafe_allow_html=True)
    
    # Display total visitors
    st.markdown('<span style="margin-top: 0.5rem; margin-bottom: 0.25rem; font-family: var(--title-font); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: #888888;">UNIQUE VISITORS</span>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="visitor-count">{metrics['total_visitors']}</div>
        <div class="visitor-date">↑ on {selected_date.strftime("%B %d, %Y")}</div>
    """, unsafe_allow_html=True)
    
    # Section divider
    st.markdown('<hr style="border: 0; height: 1px; background: rgba(75, 0, 130, 0.7); margin: 0.5rem 0;">', unsafe_allow_html=True)
    
    # Analytics section - MOVED HERE
    st.markdown('<span style="margin-top: 0.5rem; margin-bottom: 0.25rem; margin-right: 10px; font-family: var(--title-font); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.5px; color: #888888;">ANALYTICS</span>', unsafe_allow_html=True)
    
    # Create analytics cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="analytics-card">
                <div class="analytics-title">Unique Visitors</div>
                <div class="analytics-value">{metrics['analytics']['unique_visitors']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="analytics-card">
                <div class="analytics-title">Test Ride Count</div>
                <div class="analytics-value">{metrics['analytics']['test_ride_count']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="analytics-card">
                <div class="analytics-title">QR Code Count</div>
                <div class="analytics-value">{metrics['analytics']['qr_code_count']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="analytics-card">
                <div class="analytics-title">Callstore Count</div>
                <div class="analytics-value">{metrics['analytics']['callstore_count']}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Section divider
    st.markdown('<hr style="border: 0; height: 1px; background: rgba(75, 0, 130, 0.7); margin: 0.5rem 0;">', unsafe_allow_html=True)
    
    # Visitor count breakdown - MOVED AFTER ANALYTICS
    st.markdown('<span style="margin-top: 1.5rem; margin-bottom: 1rem; margin-right: 10px; font-family: var(--title-font); font-size: 1.2rem; text-transform: uppercase; letter-spacing: 1px; color: #FFFFFF; font-weight: bold; display: block; text-align: center;">VISITOR COUNT BREAKDOWN</span>', unsafe_allow_html=True)
    
    # Add subtitle with instructions for better photo capture
    st.markdown('<span style="margin-bottom: 1rem; font-family: var(--body-font); font-size: 0.65rem; color: #AAAAAA; display: block; text-align: center;">Tap chart to zoom or use controls for better visibility</span>', unsafe_allow_html=True)
    
    # Create chart data
    # Convert 24-hour format to 12-hour format for time intervals
    def convert_to_12hour_format(time_str):
        start_time, end_time = time_str.split('-')
        
        # Convert start time
        start_hour = int(start_time.split(':')[0])
        start_suffix = 'am' if start_hour < 12 else 'pm'
        start_hour = start_hour if start_hour <= 12 else start_hour - 12
        start_hour = 12 if start_hour == 0 else start_hour
        
        # Convert end time
        end_hour = int(end_time.split(':')[0])
        end_suffix = 'am' if end_hour < 12 else 'pm'
        end_hour = end_hour if end_hour <= 12 else end_hour - 12
        end_hour = 12 if end_hour == 0 else end_hour
        
        return f"{start_hour}:00{start_suffix}-{end_hour}:00{end_suffix}"
    
    # Convert time intervals to 12-hour format
    formatted_times = [convert_to_12hour_format(time) for time in metrics['hourly_breakdown'].keys()]
    
    chart_data = pd.DataFrame({
        'Time': formatted_times,
        'Count': list(metrics['hourly_breakdown'].values())
    })
    
    # Custom chart with styling - enhanced with glassy effect
    st.markdown('''
    <style>
    /* Custom styling for the chart with glassy effect */
    .stChart > div > div > div {
        background-color: black !important;
        border-radius: 12px !important;
        padding: 10px !important;
        border: 1px solid rgba(138, 43, 226, 0.3) !important;
        box-shadow: 0 8px 32px rgba(138, 43, 226, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
    }
    
    /* Chart container with glass effect */
    [data-testid="stChart"] {
        background: linear-gradient(135deg, rgba(75, 0, 130, 0.2) 0%, rgba(45, 0, 75, 0.3) 100%) !important;
        border-radius: 12px !important;
        padding: 20px !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 8px 32px rgba(75, 0, 130, 0.2) !important;
        backdrop-filter: blur(10px) !important;
        -webkit-backdrop-filter: blur(10px) !important;
        margin-bottom: 20px !important;
        position: relative !important;
        overflow: hidden !important;
    }
    
    /* Add subtle glow effect */
    [data-testid="stChart"]::before {
        content: "" !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: radial-gradient(circle at top right, rgba(138, 43, 226, 0.1), transparent 70%), 
                  radial-gradient(circle at bottom left, rgba(75, 0, 130, 0.1), transparent 70%);
        z-index: 0 !important;
        pointer-events: none !important;
    }
    
    /* Make axis labels white and improve readability */
    .stChart text {
        fill: white !important;
        font-family: var(--body-font) !important;
        font-size: 8px !important;
        font-weight: 500 !important;
        letter-spacing: -0.3px !important;
    }
    
    /* Ensure x-axis labels are horizontal and properly spaced */
    .stChart .xaxislayer-above text {
        text-anchor: middle !important;
        transform: rotate(0deg) !important;
        font-size: 8px !important;
        letter-spacing: -0.3px !important;
        margin: 0 8px !important;
    }
    
    /* Make grid lines purple with glowing effect */
    .stChart line {
        stroke: rgba(138, 43, 226, 0.6) !important;
        stroke-width: 1px !important;
        filter: drop-shadow(0 0 2px rgba(138, 43, 226, 0.5)) !important;
    }
    
    /* Make the chart bars purple with gradient */
    .stChart path.bar {
        fill: url(#purpleGradient) !important;
        stroke: rgba(255, 255, 255, 0.1) !important;
        stroke-width: 1px !important;
        filter: drop-shadow(0 0 3px rgba(138, 43, 226, 0.5)) !important;
    }
    
    /* Ensure x-axis labels are horizontal and readable */
    .stChart .xaxislayer-above text {
        text-anchor: middle !important;
        transform: rotate(0deg) !important;
    }
    </style>
    ''', unsafe_allow_html=True)
    
    # Create the full-width chart with enhanced styling using Plotly for better customization
    import plotly.express as px
    import plotly.graph_objects as go
    
    # Create a Plotly figure with custom styling
    fig = px.bar(
        chart_data, 
        x='Time', 
        y='Count',
        height=500,  # Increased height for better readability
    )
    
    # Customize the figure
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=60, r=40, t=30, b=150),  # Further increased bottom margin for labels
        font=dict(
            family='Inter, sans-serif',
            size=16,
            color='white'
        ),
        xaxis=dict(
            showgrid=True,
            gridcolor='rgba(138, 43, 226, 0.3)',
            tickangle=0,  # Keep labels horizontal as requested
            title=None,
            tickfont=dict(size=12),  # Slightly larger font for better readability
            # Show all labels as requested
            tickmode='array',
            tickvals=chart_data['Time'].tolist(),
            # Format labels to be more compact and readable - just show hour numbers
            ticktext=[f"{time.split('-')[0].split(':')[0]}{time.split('-')[0][-2:]}-{time.split('-')[1].split(':')[0]}{time.split('-')[1][-2:]}" 
                     for time in chart_data['Time']],
            ticklen=8,  # Longer tick marks
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(138, 43, 226, 0.3)',
            title=None,
            range=[0, max(max(chart_data['Count'] * 1.2), 15)],  # Add 20% headroom
            tickfont=dict(size=16),  # Larger tick font
            ticklen=8,  # Longer tick marks
        ),
        hoverlabel=dict(
            bgcolor='rgba(75, 0, 130, 0.9)',  # More opaque for better contrast
            font_size=18,  # Larger hover font
            font_family='Inter, sans-serif',
            bordercolor='white',
        ),
        bargap=0.7,  # Even more spacing between bars for better label visibility
    )
    
    # Update the bar color and add effects
    fig.update_traces(
        marker_color='rgba(138, 43, 226, 0.9)',  # More opaque for better visibility
        marker_line_color='rgba(255, 255, 255, 0.5)',  # Brighter outline
        marker_line_width=2,  # Thicker outline
        hovertemplate='<b>%{x}</b><br>Visitors: %{y}<extra></extra>',
        width=0.7,  # Control bar width
        textposition='outside',  # Show values above bars
        texttemplate='%{y}',  # Show the count value
        textfont=dict(
            size=18,  # Large text font
            color='white',
            family='Inter, sans-serif',
        ),
    )
    
    # Display the chart with zoom capabilities
    st.plotly_chart(fig, use_container_width=True, config={
        'displayModeBar': True,
        'modeBarButtonsToAdd': ['zoomIn2d', 'zoomOut2d', 'resetScale2d'],
        'modeBarButtonsToRemove': ['select2d', 'lasso2d'],
        'displaylogo': False,
        'toImageButtonOptions': {
            'format': 'png',
            'filename': 'visitor_breakdown',
            'height': 700,  # Larger export height
            'width': 1000,  # Larger export width
            'scale': 3  # Higher resolution for photos
        }
    })
    
    # Section divider
    st.markdown('<hr style="border: 0; height: 1px; background: rgba(75, 0, 130, 0.7); margin: 0.5rem 0;">', unsafe_allow_html=True)
    
    # Last updated
    st.markdown(f"""
        <div class="last-updated">Last updated: {metrics['last_updated']}</div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
