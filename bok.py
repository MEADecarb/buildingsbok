import streamlit as st
import requests

# Access the API key from Streamlit secrets
api_key = st.secrets["SFTOOL_API_KEY"]

# Set the API base URL
base_url = "https://sftool.gov/api/v1"

# Set up the Streamlit app
st.title("SFTool Building Systems Query")

# Dropdown options for building systems
building_systems = ["HVAC", "Lighting", "Plumbing", "Electrical", "Envelope", "Vertical Transportation"]

# User selects a building system from the dropdown
selected_system = st.selectbox("Select a building system:", building_systems)

# Function to query the SFTool API
def get_building_system_info(system_name):
    if system_name:
        url = f"{base_url}/buildingsystems?system={system_name}"
        headers = {"Authorization": f"Bearer {api_key}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": "Could not retrieve data. Please try again later."}
    return None

# Display results
if selected_system:
    result = get_building_system_info(selected_system)
    if "error" in result:
        st.error(result["error"])
    else:
        st.write(result)
