import streamlit as st
import subprocess
import os
import sys
import webbrowser
from threading import Timer

def open_browser():
    """Open the browser to the Streamlit app."""
    webbrowser.open_new("http://localhost:8501")

def deploy_dashboard():
    """Deploy the employee dashboard."""
    st.title("Employee Dashboard Deployment")
    
    st.write("### Deployment Options")
    
    deployment_type = st.radio(
        "Select deployment method:",
        ["Local Deployment", "Streamlit Cloud Deployment"]
    )
    
    if deployment_type == "Local Deployment":
        st.write("### Local Deployment")
        st.write("This will run the dashboard on your local machine.")
        
        if st.button("Start Local Dashboard"):
            st.success("Starting dashboard... The dashboard will open in a new browser tab.")
            
            # Open browser after a short delay
            Timer(2, open_browser).start()
            
            # Run the Streamlit app
            try:
                subprocess.run([sys.executable, "app.py"], check=True)
            except subprocess.CalledProcessError:
                st.error("Failed to start the dashboard. Please check the console for errors.")
    
    else:
        st.write("### Streamlit Cloud Deployment")
        st.write("""
        To deploy to Streamlit Cloud:
        
        1. Create a GitHub repository with your dashboard code
        2. Sign up for [Streamlit Cloud](https://streamlit.io/cloud)
        3. Connect your GitHub repository
        4. Configure the deployment settings:
           - Main file path: `app.py`
           - Python version: 3.9+
        """)
        
        st.info("This method allows you to access your dashboard from anywhere with an internet connection.")

if __name__ == "__main__":
    deploy_dashboard()
