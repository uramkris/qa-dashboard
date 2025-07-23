import streamlit as st
import requests
import pandas as pd

# Set the title of the web page in the browser tab
st.set_page_config(page_title="QA Dashboard", layout="wide")

# Add a main title to the page content
st.title("QA Test Results Dashboard")

# Define the URL of our FastAPI backend
API_URL = "http://127.0.0.1:8000/api/results"

# By commenting out the line below, we completely disable caching for this function.
# @st.cache_data
def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Failed to fetch data from API. Status code: {response.status_code}")
            return None
    except requests.exceptions.ConnectionError:
        st.error("Connection Error: Could not connect to the API. Is the backend server running?")
        return None

# --- Main part of the app ---
data = fetch_data()

if data:
    if len(data) > 0:
        df = pd.DataFrame(data)
        
        # Reorder columns for better visibility. Put the long test name first.
        df = df[['id', 'test_name', 'status', 'test_suite', 'duration_ms', 'error_message']]

        # --- THIS IS OUR NEW DEBUG LINE ---
        # It will print the exact column order onto the webpage for us to see.
        st.write("DEBUG: DataFrame Columns Order:", df.columns.tolist())
        
        st.write("### All Test Results")
        st.dataframe(
        df,
        column_order=('id', 'test_name', 'status', 'test_suite', 'duration_ms', 'error_message'),
        hide_index=True # <-- THIS IS THE FIX
    )
    else:
        st.warning("No test results found in the database.")