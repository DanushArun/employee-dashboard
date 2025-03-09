import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from PIL import Image

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

# Load and cache data
@st.cache_data
def load_data():
    # Read the Test Data.csv file
    with open('data/Test Data.csv', 'r') as f:
        content = f.read()
    
    # Split by lines
    lines = content.split('\n')
    
    # Extract different sections
    core_section = []
    ul_pl_section = []
    zone_loss_section = []
    error_count_section = []
    unsafe_act_section = []
    kaizen_section = []
    flexibility_section = []
    teamwork_section = []
    
    current_section = core_section
    for line in lines:
        if not line.strip():
            continue
            
        if "Month,Employee ID,UL" in line:
            current_section = ul_pl_section
            ul_pl_section.append(line)
        elif "Month,Employee ID,ZONE,LINE LOSS" in line:
            current_section = zone_loss_section
            zone_loss_section.append(line)
        elif "Month,Employee ID,ZONE,ERROR COUNT" in line:
            current_section = error_count_section
            error_count_section.append(line)
        elif "Month,Employee ID,UNSAFE ACT REPORTED" in line:
            current_section = unsafe_act_section
            unsafe_act_section.append(line)
        elif "Month,Employee ID,KAIZEN RESPONSIBLE" in line:
            current_section = kaizen_section
            kaizen_section.append(line)
        elif "Month,Employee ID,FLEXIBILITY CREDIT" in line:
            current_section = flexibility_section
            flexibility_section.append(line)
        elif "Month,Employee ID,TEAMWORK CREDIT" in line:
            current_section = teamwork_section
            teamwork_section.append(line)
        else:
            current_section.append(line)
    
    # Parse core data
    core_data = []
    for i, line in enumerate(core_section):
        if i == 0:  # Skip header
            continue
            
        parts = line.split(',')
        if len(parts) >= 4:
            employee_id = parts[0].strip()
            training_grade = parts[1].strip()
            training_count = parts[2].strip()
            status = parts[3].strip()
            
            core_data.append({
                'employee_id': employee_id,
                'trainer_grade': float(training_grade) if training_grade.isdigit() else 0,
                'training_count': int(training_count) if training_count.isdigit() else 0,
                'status': status.capitalize()
            })
        else:
            # Handle fixed-width format
            if len(line) >= 10:
                employee_id = line[:4].strip()
                training_grade = line[4:6].strip()
                training_count = line[6:8].strip()
                status = line[8:].strip()
                
                core_data.append({
                    'employee_id': employee_id,
                    'trainer_grade': float(training_grade) if training_grade.isdigit() else 0,
                    'training_count': int(training_count) if training_count.isdigit() else 0,
                    'status': status.capitalize()
                })
    
    # Parse UL/PL data
    ul_pl_data = {}
    for i, line in enumerate(ul_pl_section):
        if i == 0:  # Skip header
            continue
            
        parts = line.split(',')
        if len(parts) >= 4:
            month = parts[0].strip().lower()
            employee_id = parts[1].strip()
            ul = parts[2].strip()
            pl = parts[3].strip()
            
            ul_pl_data[employee_id] = {
                'month': month,
                'ul': float(ul) if ul.isdigit() else 0,
                'pl': float(pl) if pl.isdigit() else 0
            }
    
    # Parse Zone/Line Loss data
    zone_loss_data = {}
    for i, line in enumerate(zone_loss_section):
        if i == 0:  # Skip header
            continue
            
        parts = line.split(',')
        if len(parts) >= 4:
            month = parts[0].strip().lower()
            employee_id = parts[1].strip()
            zone = parts[2].strip()
            line_loss = parts[3].strip()
            
            zone_loss_data[employee_id] = {
                'month': month,
                'zone': int(zone) if zone.isdigit() else 0,
                'line_loss': float(line_loss) if line_loss.isdigit() else 0
            }
    
    # Parse Error Count data
    error_count_data = {}
    for i, line in enumerate(error_count_section):
        if i == 0:  # Skip header
            continue
            
        parts = line.split(',')
        if len(parts) >= 4:
            month = parts[0].strip().lower()
            employee_id = parts[1].strip()
            zone = parts[2].strip()
            error_count = parts[3].strip()
            
            error_count_data[employee_id] = {
                'month': month,
                'zone': int(zone) if zone.isdigit() else 0,
                'error_count': int(error_count) if error_count.isdigit() else 0
            }
    
    # Parse Unsafe Act data
    unsafe_act_data = {}
    for i, line in enumerate(unsafe_act_section):
        if i == 0:  # Skip header
            continue
            
        parts = line.split(',')
        if len(parts) >= 4:
            month = parts[0].strip().lower()
            employee_id = parts[1].strip()
            reported = parts[2].strip()
            responsible = parts[3].strip()
            
            unsafe_act_data[employee_id] = {
                'month': month,
                'unsafe_act_reported': int(reported) if reported.isdigit() else 0,
                'unsafe_act_responsible': int(responsible) if responsible.isdigit() else 0
            }
    
    # Parse Kaizen data
    kaizen_data = {}
    for i, line in enumerate(kaizen_section):
        if i == 0:  # Skip header
            continue
            
        parts = line.split(',')
        if len(parts) >= 3:
            month = parts[0].strip().lower()
            employee_id = parts[1].strip()
            kaizen = parts[2].strip()
            
            kaizen_data[employee_id] = {
                'month': month,
                'kaizen_responsible': int(kaizen) if kaizen.isdigit() else 0
            }
    
    # Parse Flexibility data
    flexibility_data = {}
    for i, line in enumerate(flexibility_section):
        if i == 0:  # Skip header
            continue
            
        parts = line.split(',')
        if len(parts) >= 3:
            month = parts[0].strip().lower()
            employee_id = parts[1].strip()
            flexibility = parts[2].strip()
            
            flexibility_data[employee_id] = {
                'month': month,
                'flexibility_credit': int(flexibility) if flexibility.isdigit() else 0
            }
    
    # Parse Teamwork data
    teamwork_data = {}
    for i, line in enumerate(teamwork_section):
        if i == 0:  # Skip header
            continue
            
        parts = line.split(',')
        if len(parts) >= 3:
            month = parts[0].strip().lower()
            employee_id = parts[1].strip()
            teamwork = parts[2].strip()
            
            teamwork_data[employee_id] = {
                'month': month,
                'teamwork_credit': int(teamwork) if teamwork.isdigit() else 0
            }
    
    # Create main DataFrame
    df = pd.DataFrame(core_data)
    
    # Add additional metrics
    for employee_id in df['employee_id']:
        # UL/PL metrics
        if employee_id in ul_pl_data:
            df.loc[df['employee_id'] == employee_id, 'ul'] = ul_pl_data[employee_id]['ul']
            df.loc[df['employee_id'] == employee_id, 'pl'] = ul_pl_data[employee_id]['pl']
            df.loc[df['employee_id'] == employee_id, 'month'] = ul_pl_data[employee_id]['month']
        
        # Zone/Line Loss metrics
        if employee_id in zone_loss_data:
            df.loc[df['employee_id'] == employee_id, 'zone'] = zone_loss_data[employee_id]['zone']
            df.loc[df['employee_id'] == employee_id, 'line_loss'] = zone_loss_data[employee_id]['line_loss']
        
        # Error Count metrics
        if employee_id in error_count_data:
            df.loc[df['employee_id'] == employee_id, 'error_count'] = error_count_data[employee_id]['error_count']
        
        # Unsafe Act metrics
        if employee_id in unsafe_act_data:
            df.loc[df['employee_id'] == employee_id, 'unsafe_act_reported'] = unsafe_act_data[employee_id]['unsafe_act_reported']
            df.loc[df['employee_id'] == employee_id, 'unsafe_act_responsible'] = unsafe_act_data[employee_id]['unsafe_act_responsible']
        
        # Kaizen metrics
        if employee_id in kaizen_data:
            df.loc[df['employee_id'] == employee_id, 'kaizen_responsible'] = kaizen_data[employee_id]['kaizen_responsible']
        
        # Flexibility metrics
        if employee_id in flexibility_data:
            df.loc[df['employee_id'] == employee_id, 'flexibility_credit'] = flexibility_data[employee_id]['flexibility_credit']
        
        # Teamwork metrics
        if employee_id in teamwork_data:
            df.loc[df['employee_id'] == employee_id, 'teamwork_credit'] = teamwork_data[employee_id]['teamwork_credit']
    
    # Fill NaN values
    df = df.fillna(0)
    
    # Calculate total marks with additional metrics
    df['total_marks'] = (
        df['trainer_grade'] + 
        df['training_count'] * 0.1 +
        df['ul'] * 0.2 +
        df['pl'] * 0.2 -
        df['error_count'] * 0.1 +
        df['kaizen_responsible'] * 0.3 +
        df['flexibility_credit'] * 0.2 +
        df['teamwork_credit'] * 0.2
    )
    
    # Convert month to date
    month_map = {
        'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'june': 6, 
        'july': 7, 'aug': 8, 'sept': 9, 'oct': 10, 'nov': 11, 'dec': 12
    }
    
    df['date'] = df['month'].apply(
        lambda m: pd.Timestamp(f"2025-{month_map.get(m.lower(), 1):02d}-01") 
        if isinstance(m, str) and m.lower() in month_map 
        else pd.Timestamp('2025-01-01')
    )
    
    return df

# Load data
df = load_data()

# Create two columns for filters
col1, col2 = st.columns(2)

with col1:
    # Employee ID dropdown with enhanced search
    st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 8px;'>EMPLOYEE ID List</p>", unsafe_allow_html=True)
    
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
    # Month selector (only shown if an employee is selected)
    if employee_id:
        # Get months that have data for this employee
        employee_months = df[df['employee_id'] == employee_id]['month'].unique()
        
        # Create a mapping for month display names
        month_display_map = {
            'jan': 'January',
            'feb': 'February',
            'mar': 'March',
            'apr': 'April',
            'may': 'May',
            'june': 'June',
            'july': 'July',
            'aug': 'August',
            'sept': 'September',
            'oct': 'October',
            'nov': 'November',
            'dec': 'December'
        }
        
        # Create month options with proper capitalization
        month_options = [month_display_map.get(m.lower(), m.capitalize()) if isinstance(m, str) else "Unknown" 
                         for m in employee_months]
        
        # If no months found, show a message
        if not month_options:
            st.markdown("<p style='color: #888; font-size: 14px;'>No month data available for this employee</p>", unsafe_allow_html=True)
            selected_month = None
        else:
            # Show available months
            st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 8px;'>MONTH</p>", unsafe_allow_html=True)
            
            # Create a mapping from display name back to actual month value
            reverse_month_map = {v: k for k, v in month_display_map.items()}
            
            # Month dropdown
            selected_month_display = st.selectbox(
                "Month",
                options=month_options,
                index=0,
                key="month_selector",
                label_visibility="collapsed"
            )
            
            # Convert display name back to actual month value
            selected_month = reverse_month_map.get(selected_month_display, selected_month_display.lower())
            
            # Show available months for this employee
            if len(month_options) > 1:
                st.markdown(f"<p style='color: #888; font-size: 12px;'>Data available for: {', '.join(month_options)}</p>", unsafe_allow_html=True)
    else:
        selected_month = None
        # Show placeholder when no employee is selected
        st.markdown("<p style='color: #888; font-size: 14px; margin-bottom: 8px;'>MONTH</p>", unsafe_allow_html=True)
        st.markdown("<p style='color: #555; font-style: italic; font-size: 14px;'>Select an employee first</p>", unsafe_allow_html=True)

# Filter data
if employee_id:
    # Filter by employee ID and selected month
    if selected_month:
        filtered_df = df[
            (df['employee_id'] == employee_id) &
            (df['month'].str.lower() == selected_month.lower())
        ]
    else:
        # If no month is selected, show all data for the employee
        filtered_df = df[df['employee_id'] == employee_id]

    if not filtered_df.empty:
        # First row: OJT Score
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem; margin-top: 0;'>OJT Score</h3>", unsafe_allow_html=True)
        m1, m2, m3 = st.columns(3)
        
        with m1:
            st.metric("TOTAL MARKS", f"{filtered_df['total_marks'].iloc[0]:.1f}/4.0")

        with m2:
            st.metric("TRAINER GRADE", f"{filtered_df['trainer_grade'].iloc[0]:.1f}/4.0")

        with m3:
            st.metric("TRAINING COUNT", int(filtered_df['training_count'].iloc[0]))
        
        # Second row: Status
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        status = filtered_df['status'].iloc[0]
        
        # Center the status indicator
        _, status_col, _ = st.columns([1, 2, 1])
        with status_col:
            st.markdown(f"""
                <div style='background: var(--card-bg); border-radius: 10px; text-align: center; padding: 1.5rem;'>
                    <p style='color: #888; font-size: 14px; margin-bottom: 8px;'>STATUS</p>
                    <div class='status-{status.lower()}'>{status}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Third row: Absenteeism
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>Absenteeism</h3>", unsafe_allow_html=True)
        ul_pl_1, ul_pl_2, ul_pl_3 = st.columns(3)
        
        with ul_pl_1:
            st.metric("UL (Upper Limit)", filtered_df['ul'].iloc[0])
        
        with ul_pl_2:
            st.metric("PL (Production Limit)", filtered_df['pl'].iloc[0])
        
        with ul_pl_3:
            month_value = filtered_df['month'].iloc[0]
            month_display = month_value.capitalize() if isinstance(month_value, str) else "N/A"
            st.metric("Month", month_display)
        
        # Fourth row: Line Loss Count
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>Line Loss Count</h3>", unsafe_allow_html=True)
        
        # Use 3 columns with the middle one empty to reduce the gap
        zone_1, _, zone_2 = st.columns([1, 0.2, 1])
        
        with zone_1:
            st.metric("Zone", int(filtered_df['zone'].iloc[0]))
        
        with zone_2:
            st.metric("Line Loss/Month", filtered_df['line_loss'].iloc[0])
        
        # Fifth row: Associate Error
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>Associate Error</h3>", unsafe_allow_html=True)
        err_1, err_2, err_3 = st.columns(3)
        
        with err_1:
            st.metric("Error Count", int(filtered_df['error_count'].iloc[0]))
        
        with err_2:
            st.metric("Unsafe Acts Reported", int(filtered_df['unsafe_act_reported'].iloc[0]))
        
        with err_3:
            st.metric("Unsafe Acts Responsible", int(filtered_df['unsafe_act_responsible'].iloc[0]))
        
        # Sixth row: Performance Credits
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<h3 class='halo-font' style='font-size: 1.5rem;'>Performance Credits</h3>", unsafe_allow_html=True)
        cred_1, cred_2, cred_3 = st.columns(3)
        
        with cred_1:
            st.metric("Kaizen Responsible", int(filtered_df['kaizen_responsible'].iloc[0]))
        
        with cred_2:
            st.metric("Flexibility Credit", int(filtered_df['flexibility_credit'].iloc[0]))
        
        with cred_3:
            st.metric("Teamwork Credit", int(filtered_df['teamwork_credit'].iloc[0]))
            
        # Add a note about the scoring system at the bottom of all metrics
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("<p style='color: #888; font-size: 12px; text-align: center; margin-top: 10px;'>* Scores are rated on a scale of 0-4, with 4 being the highest.</p>", unsafe_allow_html=True)
