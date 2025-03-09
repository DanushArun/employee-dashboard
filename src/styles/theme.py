import streamlit as st

def apply_custom_theme():
    st.set_page_config(
        page_title="Employee Performance Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    # Custom CSS for dark theme and animations
    st.markdown("""
        <style>
        /* Main theme colors */
        :root {
            --background-color: #000000;
            --accent-color: #00FF9D;
            --text-color: #FFFFFF;
            --card-bg: #1C1C1C;
            --hover-bg: #2D2D2D;
            --border-color: rgba(255, 255, 255, 0.1);
        }
        
        /* Global styles */
        .stApp {
            background-color: var(--background-color);
            font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* Streamlit default element overrides */
        .stApp > header {
            background-color: transparent !important;
        }

        .stApp [data-testid="stToolbar"] {
            background-color: transparent !important;
        }

        .stApp .stMarkdown {
            font-family: "SF Pro Display", -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Custom card styling */
        div.element-container div.row-widget.stRadio > div {
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 1rem;
            transition: transform 0.3s ease;
        }
        
        div.element-container div.row-widget.stRadio > div:hover {
            transform: translateY(-5px);
        }
        
        /* Dropdown customization */
        .stSelectbox > div > div {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px;
            min-height: 48px;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:hover {
            border-color: var(--accent-color) !important;
            background-color: var(--hover-bg) !important;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background-color: transparent !important;
        }
        
        .stSelectbox [data-baseweb="popover"] {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px;
            margin-top: 4px;
        }
        
        .stSelectbox [data-baseweb="select-option"] {
            padding: 12px 16px !important;
            transition: all 0.2s ease;
        }
        
        .stSelectbox [data-baseweb="select-option"]:hover {
            background-color: var(--hover-bg) !important;
            color: var(--accent-color) !important;
        }
        
        /* Date picker styling */
        .stDateInput > div {
            background-color: var(--card-bg) !important;
            border: 1px solid var(--border-color) !important;
            border-radius: 8px;
            min-height: 48px;
            transition: all 0.3s ease;
        }
        
        .stDateInput > div:hover {
            border-color: var(--accent-color) !important;
            background-color: var(--hover-bg) !important;
        }
        
        .stDateInput input {
            color: var(--text-color) !important;
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
        
        /* Dropdown search styling */
        .stSelectbox input {
            color: var(--text-color) !important;
            background-color: var(--card-bg) !important;
        }
        
        .stSelectbox [data-baseweb="select"] {
            background-color: var(--card-bg) !important;
        }
        
        .stSelectbox [data-baseweb="popover"] {
            background-color: var(--card-bg) !important;
        }
        
        .stSelectbox [data-baseweb="select-option"]:hover {
            background-color: var(--accent-color) !important;
            color: var(--background-color) !important;
        }
        
        /* Metric cards */
        div[data-testid="metric-container"] {
            background-color: var(--card-bg);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid var(--border-color);
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
        }
        
        div[data-testid="metric-container"]:hover {
            border-color: var(--accent-color);
            transform: translateY(-2px);
            box-shadow: 0 8px 16px rgba(0, 255, 157, 0.1);
        }
        
        div[data-testid="metric-container"] label {
            color: #888 !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            letter-spacing: 0.5px !important;
            text-transform: uppercase !important;
        }
        
        div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            font-size: 32px !important;
            font-weight: 700 !important;
            color: var(--text-color) !important;
            letter-spacing: -0.5px !important;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .element-container {
            animation: fadeIn 0.6s ease-out forwards;
        }
        
        /* Status indicator */
        .status-indicator {
            padding: 8px 16px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 16px;
            display: inline-block;
            letter-spacing: 0.5px;
            text-transform: uppercase;
            transition: all 0.3s ease;
        }
        
        .status-pass {
            background-color: rgba(0, 255, 157, 0.2);
            color: #00FF9D;
        }
        
        .status-fail {
            background-color: rgba(255, 71, 87, 0.2);
            color: #FF4757;
        }
        
        /* Search box styling */
        .stTextInput > div > div > input {
            background-color: var(--card-bg) !important;
            border: 1px solid rgba(255, 255, 255, 0.1);
            color: var(--text-color) !important;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 1px var(--accent-color) !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5);
        }
        
        /* Hide default Streamlit labels when needed */
        .stTextInput label, .stSelectbox label {
            display: none;
        }
        
        /* Improve spacing between search and dropdown */
        .stTextInput {
            margin-bottom: 0.5rem;
        }
        </style>
    """, unsafe_allow_html=True)
