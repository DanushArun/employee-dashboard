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
from src.utils.database import fetch_core_data, fetch_performance_data, fetch_zone_leaders_data, fetch_r_cadres_data

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

# Helper function to calculate grades based on criteria
def calculate_grade(value, criteria):
    """Calculate grade based on criteria"""
    if criteria == 'audit_nc':
        # 4=100%, 3=85-99%, 2=65-85%, 1=<65%
        if value >= 100:
            return 4.0
        elif value >= 85:
            return 3.0
        elif value >= 65:
            return 2.0
        else:
            return 1.0
    elif criteria == 'submissions':
        # 4=>9, 3=6-9, 2=3-6, 1=<3
        if value >= 9:
            return 4.0
        elif value >= 6:
            return 3.0
        elif value >= 3:
            return 2.0
        else:
            return 1.0
    elif criteria == 'line_loss':
        # 4=0, 3=1-3%, 2=3-5%, 1=>5%
        if value == 0:
            return 4.0
        elif value <= 3:
            return 3.0
        elif value <= 5:
            return 2.0
        else:
            return 1.0
    elif criteria == 'error_count':
        # 4=0, 3=1-3, 2=4-6, 1=>6
        if value == 0:
            return 4.0
        elif value <= 3:
            return 3.0
        elif value <= 6:
            return 2.0
        else:
            return 1.0
    else:
        return 0.0

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
        
        # Calculate grades based on criteria from Excel sheet
        df['audit_nc_grade'] = df.apply(lambda row: calculate_grade(row['audit_nc_score'], 'audit_nc') 
                                       if row['role'] == 'ZONE_LEADER' else 0, axis=1)
        
        df['line_loss_grade'] = df.apply(lambda row: calculate_grade(row['line_loss'], 'line_loss'), axis=1)
        
        df['error_count_grade'] = df.apply(lambda row: calculate_grade(row['error_count'], 'error_count'), axis=1)
        
        df['absenteeism_grade'] = df.apply(lambda row: 
                                          4.0 if row['ul'] == 0 and row['sl'] == 0 else
                                          3.0 if row['ul'] == 0 and row['sl'] <= 1 else
                                          2.0 if row['ul'] <= 1 or row['sl'] <= 2 else
                                          1.0, axis=1)
        
        df['flexibility_grade'] = df.apply(lambda row: calculate_grade(row['flexibility_credit'], 'submissions'), axis=1)
        df['teamwork_grade'] = df.apply(lambda row: calculate_grade(row['teamwork_credit'], 'submissions'), axis=1)
        df['unsafe_act_grade'] = df.apply(lambda row: calculate_grade(row['unsafe_act_reported'], 'submissions'), axis=1)
        df['kaizen_grade'] = df.apply(lambda row: calculate_grade(row['kaizen_responsible'], 'submissions'), axis=1)
        
        # WI & PPE grade (only for R cadres)
        df['wi_ppe_grade'] = df.apply(lambda row: row['wi_ppe_score'] if row['role'] == 'R_CADRE' else 0, axis=1)
        
        # OJT test score (normalized to 4.0)
        df['ojt_test_grade'] = df['ojt_test_score'] / 100 * 4.0
        
        # DWM adherence (only for zone leaders)
        df['dwm_adherence_grade'] = df.apply(lambda row: row['dwm_adherence_score'] 
                                            if row['role'] == 'ZONE_LEADER' else 0, axis=1)
        
        # Calculate total grade based on role
        df['total_marks'] = df.apply(lambda row:
            # For Zone Leaders
            (row['audit_nc_grade'] * 0.10 +
             row['line_loss_grade'] * 0.15 +
             row['error_count_grade'] * 0.10 +
             row['absenteeism_grade'] * 0.15 +
             row['flexibility_grade'] * 0.10 +
             row['teamwork_grade'] * 0.10 +
             row['unsafe_act_grade'] * 0.10 +
             row['kaizen_grade'] * 0.10 +
             row['ojt_test_grade'] * 0.05 +
             row['dwm_adherence_grade'] * 0.05) if row['role'] == 'ZONE_LEADER' else
            # For R Cadres
            (row['line_loss_grade'] * 0.15 +
             row['error_count_grade'] * 0.15 +
             row['absenteeism_grade'] * 0.15 +
             row['flexibility_grade'] * 0.10 +
             row['teamwork_grade'] * 0.10 +
             row['unsafe_act_grade'] * 0.10 +
             row['kaizen_grade'] * 0.10 +
             row['wi_ppe_grade'] * 0.10 +
             row['ojt_test_grade'] * 0.05), axis=1)
        
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

            # Display metrics based on role
            role = filtered_df['role'].values[0]
            
            # Common metrics for both roles
            common_metrics = st.container()
            with common_metrics:
                # Line Loss section
                st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>LINE LOSS</h3>", unsafe_allow_html=True)
                line_cols = st.columns(2)
                with line_cols[0]:
                    st.metric("LINE LOSS COUNT", int(filtered_df['line_loss'].values[0]))
                with line_cols[1]:
                    st.metric("LINE LOSS GRADE", f"{filtered_df['line_loss_grade'].values[0]:.1f}/4.0")
                
                # Associate Error section
                st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>ASSOCIATE ERROR</h3>", unsafe_allow_html=True)
                error_cols = st.columns(2)
                with error_cols[0]:
                    st.metric("ASSOCIATE ERROR COUNT", int(filtered_df['error_count'].values[0]))
                with error_cols[1]:
                    st.metric("ASSOCIATE ERROR GRADE", f"{filtered_df['error_count_grade'].values[0]:.1f}/4.0")
                
                # Absenteeism section
                st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>ABSENTEEISM</h3>", unsafe_allow_html=True)
                abs_cols = st.columns(3)
                with abs_cols[0]:
                    st.metric("UL COUNT", f"{filtered_df['ul'].values[0]:.1f}")
                with abs_cols[1]:
                    st.metric("SL COUNT", f"{filtered_df['sl'].values[0]:.1f}")
                with abs_cols[2]:
                    st.metric("ABSENTEEISM GRADE", f"{filtered_df['absenteeism_grade'].values[0]:.1f}/4.0")
                
                # Performance Credits section
                st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>PERFORMANCE CREDITS</h3>", unsafe_allow_html=True)
                perf_cols = st.columns(4)
                with perf_cols[0]:
                    st.metric("KAIZEN", f"{filtered_df['kaizen_responsible'].values[0]}")
                    st.metric("GRADE", f"{filtered_df['kaizen_grade'].values[0]:.1f}/4.0")
                with perf_cols[1]:
                    st.metric("UNSAFE ACT", f"{filtered_df['unsafe_act_reported'].values[0]}")
                    st.metric("GRADE", f"{filtered_df['unsafe_act_grade'].values[0]:.1f}/4.0")
                with perf_cols[2]:
                    st.metric("FLEXIBILITY", f"{filtered_df['flexibility_credit'].values[0]}")
                    st.metric("GRADE", f"{filtered_df['flexibility_grade'].values[0]:.1f}/4.0")
                with perf_cols[3]:
                    st.metric("TEAMWORK", f"{filtered_df['teamwork_credit'].values[0]}")
                    st.metric("GRADE", f"{filtered_df['teamwork_grade'].values[0]:.1f}/4.0")
                
                # OJT Test Score
                st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>OJT TEST SCORE</h3>", unsafe_allow_html=True)
                ojt_cols = st.columns(2)
                with ojt_cols[0]:
                    st.metric("RAW SCORE", f"{filtered_df['ojt_test_score'].values[0]:.1f}/100")
                with ojt_cols[1]:
                    st.metric("NORMALIZED GRADE", f"{filtered_df['ojt_test_grade'].values[0]:.1f}/4.0")
            
            # Role-specific metrics
            if role == 'ZONE_LEADER':
                zone_leader_metrics = st.container()
                with zone_leader_metrics:
                    # Audit NCs (Zone Leaders only)
                    st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>AUDIT NCs</h3>", unsafe_allow_html=True)
                    audit_cols = st.columns(2)
                    with audit_cols[0]:
                        st.metric("COMPLETION PERCENTAGE", f"{filtered_df['audit_nc_score'].values[0]:.1f}%")
                    with audit_cols[1]:
                        st.metric("AUDIT GRADE", f"{filtered_df['audit_nc_grade'].values[0]:.1f}/4.0")
                    
                    # DWM Adherence (Zone Leaders only)
                    st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>DWM ADHERENCE</h3>", unsafe_allow_html=True)
                    st.metric("GRADE", f"{filtered_df['dwm_adherence_grade'].values[0]:.1f}/4.0")
            
            elif role == 'R_CADRE':
                r_cadre_metrics = st.container()
                with r_cadre_metrics:
                    # WI & PPE (R Cadres only)
                    st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>WI & PPE ADHERENCE</h3>", unsafe_allow_html=True)
                    st.metric("GRADE", f"{filtered_df['wi_ppe_grade'].values[0]:.1f}/4.0")
            
        # Add a note about the scoring system at the bottom of all metrics
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #888; font-size: 12px; text-align: center; margin-top: 10px;'>* Scores are rated on a scale of 0-4, with 4 being the highest.</p>", unsafe_allow_html=True)
