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
        background: rgba(75, 0, 130, 0.7);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .header-title {
        color: white;
        font-family: var(--title-font);
        font-size: 2.5rem;
        font-weight: 600;
        margin-left: 1rem;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* Search bar styling */
    .search-container {
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
    
    /* Override Streamlit's default input styling */
    .stTextInput > div > div > input {
        background-color: #2D2D2D !important;
        color: white !important;
        border-radius: 20px !important;
        padding: 10px 15px !important;
        border: none !important;
        height: 45px !important;
        font-family: var(--body-font) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #888 !important;
        font-family: var(--body-font) !important;
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
    
    /* Date picker styling */
    .stDateInput > div {
        background-color: transparent !important;
        border-radius: 0 !important;
        border: none !important;
        font-family: var(--body-font) !important;
        padding: 0 !important;
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
    }
    
    /* Calendar styling */
    .streamlit-expanderContent div[data-baseweb="calendar"] {
        background-color: #1A1A1A !important;
        font-family: var(--body-font) !important;
    }
    
    .streamlit-expanderContent div[data-baseweb="calendar"] button {
        color: white !important;
        font-family: var(--body-font) !important;
    }
    
    .streamlit-expanderContent div[data-baseweb="calendar"] button:hover {
        background-color: #9370DB !important;
    }
    
    .streamlit-expanderContent div[data-baseweb="calendar"] button[aria-selected="true"] {
        background-color: #9370DB !important;
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
        background-color: #1A1A1A;
        border-radius: 8px;
        padding: 0.5rem;
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

# Mock API call function
def fetch_store_metrics(store_id, date):
    """
    Mock function to fetch store metrics from API
    In production, this would make an actual API call
    """
    # Format the API endpoint
    api_endpoint = f"/api/v1/analytics/stores/metrics/?store_id={store_id}&date={date}"
    
    # In a real implementation, this would be:
    # response = requests.get(api_endpoint)
    # return response.json()
    
    # For now, return mock data
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

# Main function
def main():
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
    search = st.text_input("", placeholder="🔍 Search stores by name...", label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Load stores
    stores = load_stores()
    
    # Filter stores based on search
    if search:
        filtered_stores = [store for store in stores if search.lower() in store['name'].lower()]
    else:
        filtered_stores = stores
    
    # Create a container for the store cards grid
    st.markdown('<div style="margin-top: 50px;">', unsafe_allow_html=True)
    
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
    
    # Create a container for the date input with custom styling - with label
    st.markdown('<div style="display: flex; align-items: center; margin-bottom: 0.5rem;">', unsafe_allow_html=True)
    st.markdown('<span style="margin-right: 10px; font-size: 0.9rem; color: #888; font-family: var(--title-font); text-transform: uppercase; letter-spacing: 0.5px;">DATE:</span>', unsafe_allow_html=True)
    date_col, _ = st.columns([3, 7])
    with date_col:
        selected_date = st.date_input("", datetime.now(), label_visibility="collapsed")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Format date for API call
    formatted_date = selected_date.strftime("%Y-%m-%d")
    
    # Fetch metrics
    metrics = fetch_store_metrics(store_id, formatted_date)
    
    # Section divider
    st.markdown('<hr style="border: 0; height: 1px; background: rgba(75, 0, 130, 0.7); margin: 0.5rem 0;">', unsafe_allow_html=True)
    
    # Display total visitors
    st.markdown('<p style="margin-top: 0.5rem; margin-bottom: 0.25rem; font-family: var(--title-font); font-size: 0.9rem; text-transform: uppercase; letter-spacing: 0.5px; color: #888;">UNIQUE VISITORS</p>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="visitor-count">{metrics['total_visitors']}</div>
        <div class="visitor-date">↑ on {selected_date.strftime("%B %d, %Y")}</div>
    """, unsafe_allow_html=True)
    
    # Section divider
    st.markdown('<hr style="border: 0; height: 1px; background: rgba(75, 0, 130, 0.7); margin: 0.5rem 0;">', unsafe_allow_html=True)
    
    # Visitor count breakdown
    st.markdown('<h3 class="section-title" style="font-size: 1.5rem;">VISITOR COUNT BREAKDOWN</h3>', unsafe_allow_html=True)
    
    # Create columns for table and chart
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # Create table
        st.markdown("""
            <table class="styled-table">
                <thead>
                    <tr>
                        <th>Time Interval</th>
                        <th>Count</th>
                    </tr>
                </thead>
                <tbody>
        """, unsafe_allow_html=True)
        
        for interval, count in metrics['hourly_breakdown'].items():
            st.markdown(f"""
                <tr>
                    <td>{interval}</td>
                    <td>{count}</td>
                </tr>
            """, unsafe_allow_html=True)
        
        st.markdown("""
                </tbody>
            </table>
        """, unsafe_allow_html=True)
    
    with col2:
        # Create chart
        chart_data = pd.DataFrame({
            'Time': list(metrics['hourly_breakdown'].keys()),
            'Count': list(metrics['hourly_breakdown'].values())
        })
        st.bar_chart(chart_data.set_index('Time'), height=320)
    
    # Section divider
    st.markdown('<hr style="border: 0; height: 1px; background: rgba(75, 0, 130, 0.7); margin: 0.5rem 0;">', unsafe_allow_html=True)
    
    # Analytics section
    st.markdown('<h3 class="section-title" style="font-size: 1.5rem;">ANALYTICS</h3>', unsafe_allow_html=True)
    
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
    
    # Last updated
    st.markdown(f"""
        <div class="last-updated">Last updated: {metrics['last_updated']}</div>
    """, unsafe_allow_html=True)

# Run the app
if __name__ == "__main__":
    main()
