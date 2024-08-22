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
      url = f"{base_url}/buildingsystems"
      headers = {"Authorization": f"Bearer {api_key}"}
      params = {"system": system_name}
      response = requests.get(url, headers=headers, params=params)
      if response.status_code == 200:
          return response.json()
      else:
          return {"error": f"Could not retrieve data. Status code: {response.status_code}"}
  return None

# Display results
if selected_system:
  with st.spinner("Fetching data..."):
      result = get_building_system_info(selected_system)
  
  if result is None:
      st.warning("No data retrieved. Please select a building system.")
  elif "error" in result:
      st.error(result["error"])
  else:
      st.subheader(f"Information for {selected_system}")
      st.json(result)

# Add error handling for API key
if not api_key:
  st.error("API key is missing. Please set the SFTOOL_API_KEY in your Streamlit secrets.")
