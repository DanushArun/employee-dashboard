import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from PIL import Image

# Import custom components
from src.components.charts import (
    create_performance_chart,
    create_trend_chart,
    create_comparison_chart,
    create_status_distribution,
    create_zone_distribution
)
from src.utils.database import fetch_core_data, fetch_performance_data

# Page config
st.set_page_config(
    page_title="Employee Performance Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --background-color: #000000;
        --accent-color: #00FF9D;
        --text-color: #FFFFFF;
        --card-bg: #1C1C1C;
        --hover-bg: #2D2D2D;
    }
    
    .stApp {
        background-color: var(--background-color);
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background-color: var(--card-bg);
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    div[data-testid="metric-container"] label {
        color: #888 !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }
    
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
        color: var(--text-color) !important;
    }
    
    /* Status styles */
    .status-pass {
        background-color: rgba(0, 255, 157, 0.2);
        color: #00FF9D;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
    }
    
    .status-fail {
        background-color: rgba(255, 71, 87, 0.2);
        color: #FF4757;
        padding: 8px 16px;
        border-radius: 6px;
        font-weight: 600;
    }
    
    /* Input styling */
    .stSelectbox [data-baseweb="select"] {
        background-color: var(--card-bg) !important;
    }
    
    /* Dropdown styling */
    .stSelectbox [data-baseweb="popover"] {
        background-color: var(--card-bg) !important;
        border: 1px solid var(--accent-color) !important;
    }
    
    .stSelectbox [data-baseweb="select-option"] {
        background-color: var(--card-bg) !important;
    }
    
    .stSelectbox [data-baseweb="select-option"]:hover {
        background-color: var(--hover-bg) !important;
    }
    
    .stSelectbox [data-baseweb="select-option"][aria-selected="true"] {
        background-color: var(--accent-color) !important;
        color: var(--background-color) !important;
    }
    
    /* Search input styling */
    .stSelectbox input {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        background-color: var(--card-bg) !important;
        color: var(--text-color) !important;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: var(--accent-color) !important;
        box-shadow: 0 0 0 1px var(--accent-color) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: rgba(255, 255, 255, 0.5);
    }
    
    /* Remove all focus outlines completely */
    *:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    *:focus-visible {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Remove all focus styling */
    .stSelectbox [data-baseweb="select"]:focus-within {
        border-color: var(--accent-color) !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Date input styling */
    .stDateInput > div {
        background-color: var(--card-bg) !important;
    }
    
    .stDateInput > div:focus-within {
        border-color: var(--accent-color) !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    /* Override Streamlit's default focus styles */
    [data-baseweb="select"] {
        outline: none !important;
        box-shadow: none !important;
    }
    
    [data-baseweb="select"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    [data-baseweb="input"] {
        outline: none !important;
        box-shadow: none !important;
    }
    
    [data-baseweb="input"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Override for dropdown items */
    [data-baseweb="menu"] {
        outline: none !important;
        box-shadow: none !important;
    }
    
    [data-baseweb="select-option"]:focus {
        background-color: var(--accent-color) !important;
        color: var(--background-color) !important;
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Remove all outlines and shadows */
    button:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    input:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    select:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Override Streamlit's default styles */
    .stApp [role="button"]:focus {
        outline: none !important;
        box-shadow: none !important;
    }
    
    /* Calendar styling */
    .streamlit-expanderContent div[data-baseweb="calendar"] {
        background-color: var(--card-bg) !important;
    }
    
    .streamlit-expanderContent div[data-baseweb="calendar"] button {
        color: var(--text-color) !important;
    }
    
    .streamlit-expanderContent div[data-baseweb="calendar"] button:hover {
        background-color: var(--accent-color) !important;
        color: var(--background-color) !important;
    }
    
    .streamlit-expanderContent div[data-baseweb="calendar"] button[aria-selected="true"] {
        background-color: var(--accent-color) !important;
        color: var(--background-color) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Add logo
logo = Image.open('src/assets/ather-logo.png')
st.image(logo, width=130)

# Header with HALO-style font
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    
    .halo-font {
        font-family: 'Orbitron', sans-serif;
        color: #00FF9D;
        margin-bottom: 2rem;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-weight: 700;
        font-size: 2.5rem;
    }
    </style>
    
    <h1 class="halo-font">Employee Performance Dashboard</h1>
""", unsafe_allow_html=True)

# Load and cache data with auto-refresh
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def load_data():
    try:
        # Fetch core data
        core_df = fetch_core_data()
        if core_df.empty:
            st.error("Failed to fetch core data from database")
            return pd.DataFrame()
            
        # Fetch performance data
        perf_df = fetch_performance_data()
        if perf_df.empty:
            st.error("Failed to fetch performance data from database")
            return pd.DataFrame()
            
        # Merge core and performance data
        df = pd.merge(core_df, perf_df, on='employee_id', how='left')
        
        # Fill NaN values
        df = df.fillna(0)
        
        # Normalize metrics to 0-1 range
        df['norm_trainer_grade'] = df['trainer_grade'] / 4.0  # Assuming max grade is 4
        df['norm_training_count'] = df['training_count'] / df['training_count'].max() if df['training_count'].max() > 0 else 0
        df['norm_ul'] = 1 - (df['ul'] / 5.0)  # Lower is better, max assumed 5
        df['norm_pl'] = 1 - (df['pl'] / 5.0)  # Lower is better, max assumed 5
        df['norm_error_count'] = 1 - (df['error_count'] / df['error_count'].max()) if df['error_count'].max() > 0 else 1
        df['norm_kaizen'] = df['kaizen_responsible'] / df['kaizen_responsible'].max() if df['kaizen_responsible'].max() > 0 else 0
        df['norm_flexibility'] = df['flexibility_credit'] / df['flexibility_credit'].max() if df['flexibility_credit'].max() > 0 else 0
        df['norm_teamwork'] = df['teamwork_credit'] / df['teamwork_credit'].max() if df['teamwork_credit'].max() > 0 else 0
        
        # Calculate weighted normalized total score (weights sum to 1)
        df['total_marks'] = (
            df['norm_trainer_grade'] * 0.20 +  # Core competency
            df['norm_training_count'] * 0.10 +  # Learning progress
            df['norm_ul'] * 0.15 +  # Performance metrics
            df['norm_pl'] * 0.15 +
            df['norm_error_count'] * 0.10 +
            df['norm_kaizen'] * 0.15 +  # Initiative and improvement
            df['norm_flexibility'] * 0.075 +  # Soft skills
            df['norm_teamwork'] * 0.075  # Collaboration
        ) * 4.0  # Scale to 0-4.0 range
        
        # Convert month to date
        month_map = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'june': 6, 
            'july': 7, 'aug': 8, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12
        }
        
        df['date'] = df['month'].apply(
            lambda m: pd.Timestamp(f"2025-{month_map.get(str(m).lower(), 1):02d}-01") 
            if isinstance(m, str) and m.lower() in month_map 
            else pd.Timestamp('2025-01-01')
        )
        
        return df
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return pd.DataFrame()

# Add auto-refresh button
if st.button('🔄 Refresh Data'):
    st.cache_data.clear()
    st.rerun()

# Load data
df = load_data()

# Create three columns for filters
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    # Employee ID dropdown with enhanced search
    st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 8px;'>EMPLOYEE ID</p>", unsafe_allow_html=True)
    
    # Add search functionality
    search_term = st.text_input(
        "Search",
        key="search_employee",
        placeholder="Type to search employee IDs...",
        label_visibility="collapsed"
    ).upper()
    
    # Filter employee IDs based on search
    employee_ids = [''] + sorted(df['employee_id'].unique().tolist())
    if search_term:
        filtered_ids = [eid for eid in employee_ids if search_term in str(eid)]
    else:
        filtered_ids = employee_ids
    
    # Employee ID dropdown
    employee_id = st.selectbox(
        "-",
        options=filtered_ids,
        format_func=lambda x: x if x else "Select an Employee ID",
        label_visibility="collapsed"
    )

with col2:
    # Zone selector
    st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 8px;'>ZONE</p>", unsafe_allow_html=True)
    zones = [''] + sorted(df['zone'].unique().tolist())
    zone = st.selectbox(
        "-",
        options=zones,
        format_func=lambda x: x if x else "Select Zone",
        label_visibility="collapsed"
    )

with col3:
    # Date Range
    st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 8px;'>DATE RANGE</p>", unsafe_allow_html=True)
    date_cols = st.columns(2)
    with date_cols[0]:
        start_date = st.date_input("From", value=None, label_visibility="collapsed")
    with date_cols[1]:
        end_date = st.date_input("To", value=None, label_visibility="collapsed")

# Filter data
if employee_id:
    # Start with employee filter
    filtered_df = df[df['employee_id'] == employee_id]
    
    # Apply zone filter if selected
    if zone:
        filtered_df = filtered_df[filtered_df['zone'] == zone]
    
    # Apply date range filter if selected
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['date'] >= pd.to_datetime(start_date)) &
            (filtered_df['date'] <= pd.to_datetime(end_date))
        ]

    # Check if we have data to display
    if isinstance(filtered_df, pd.DataFrame) and not filtered_df.empty:
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Dashboard", "Performance Analysis"])
        
        with tab1:
            # Total Grade (centered)
            _, grade_col, _ = st.columns([1, 2, 1])
            with grade_col:
                st.markdown("""
                    <div style='background: var(--card-bg); border-radius: 12px; text-align: center; padding: 2rem; margin: 2rem 0;'>
                        <h2 style='color: var(--accent-color); font-size: 1.2rem; margin-bottom: 1rem;'>TOTAL GRADE</h2>
                        <div style='font-size: 2.5rem; font-weight: bold;'>{:.1f}/4.0</div>
                    </div>
                """.format(filtered_df['total_marks'].values[0]), unsafe_allow_html=True)

        # OJT Score section
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem; margin-top: 0;'>OJT</h3>", unsafe_allow_html=True)
        ojt_cols = st.columns(4)
        
        with ojt_cols[0]:
            st.metric("TRAINEE GRADE", f"{filtered_df['trainer_grade'].values[0]:.1f}/4.0")
        with ojt_cols[1]:
            st.metric("TRAINER GRADE", f"{filtered_df['trainer_grade'].values[0]:.1f}/4.0")
        with ojt_cols[2]:
            st.metric("STATUS", filtered_df['status'].values[0])
        with ojt_cols[3]:
            st.metric("PERCENTILE", "85%")
        
        # Absenteeism section
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>ABSENTEEISM</h3>", unsafe_allow_html=True)
        abs_cols = st.columns(2)
        with abs_cols[0]:
            st.metric("INDIVIDUAL ABSENTEEISM", f"{filtered_df['ul'].values[0]:.1f}")
        with abs_cols[1]:
            st.metric("ZONAL ABSENTEEISM", f"{filtered_df['pl'].values[0]:.1f}")
        
        # Line Loss section
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>LINE LOSS</h3>", unsafe_allow_html=True)
        line_cols = st.columns(2)
        with line_cols[0]:
            st.metric("LINE LOSS COUNT", int(filtered_df['line_loss'].values[0]))
        with line_cols[1]:
            st.metric("LINE LOSS GRADE", "3.5/4.0")
        
        # Associate Error section
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>ASSOCIATE ERROR</h3>", unsafe_allow_html=True)
        error_cols = st.columns(2)
        with error_cols[0]:
            st.metric("ASSOCIATE ERROR COUNT", int(filtered_df['error_count'].values[0]))
        with error_cols[1]:
            st.metric("ASSOCIATE ERROR GRADE", "3.0/4.0")
        
        # Adherence sections
        adh_cols = st.columns(2)
        with adh_cols[0]:
            st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>WI & PPE ADHERENCE</h3>", unsafe_allow_html=True)
            st.metric("GRADE", "3.8/4.0")
        with adh_cols[1]:
            st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>DWM ADHERENCE</h3>", unsafe_allow_html=True)
            st.metric("GRADE", "3.5/4.0")
        
        # Performance Credits section
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>PERFORMANCE CREDITS</h3>", unsafe_allow_html=True)
        perf_cols = st.columns(4)
        with perf_cols[0]:
            st.metric("KAIZEN GRADE", f"{filtered_df['kaizen_responsible'].values[0]}/4.0")
        with perf_cols[1]:
            st.metric("UNSAFE ACT GRADE", f"{filtered_df['unsafe_act_reported'].values[0]}/4.0")
        with perf_cols[2]:
            st.metric("FLEXIBILITY GRADE", f"{filtered_df['flexibility_credit'].values[0]}/4.0")
        with perf_cols[3]:
            st.metric("TEAMWORK GRADE", f"{filtered_df['teamwork_credit'].values[0]}/4.0")
            
        # Add a note about the scoring system at the bottom of all metrics
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #888; font-size: 12px; text-align: center; margin-top: 10px;'>* Scores are rated on a scale of 0-4, with 4 being the highest.</p>", unsafe_allow_html=True)
