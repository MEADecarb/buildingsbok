import streamlit as st
import requests

# Access the API key from Streamlit secrets (or use DEMO_KEY for testing)
api_key = st.secrets.get("SFTOOL_API_KEY", "DEMO_KEY")

# Set the correct API base URL
base_url = "https://api.gsa.gov/sustainability/sftool/v1"

# Set up the Streamlit app
st.title("SFTool Building Systems Query")

# Function to get all building systems
def get_building_systems():
  url = f"{base_url}/building-systems"
  params = {"api_key": api_key}
  response = requests.get(url, params=params)
  if response.status_code == 200:
      systems = response.json()
      return {system['name']: system['slug'] for system in systems}
  else:
      st.error(f"Failed to fetch building systems. Status code: {response.status_code}")
      return {}

# Get building systems
building_systems = get_building_systems()

# User selects a building system from the dropdown
selected_system = st.selectbox("Select a building system:", list(building_systems.keys()))

# Function to query the SFTool API for system details
def get_building_system_info(system_slug):
  url = f"{base_url}/building-systems/{system_slug}"
  params = {"api_key": api_key}
  response = requests.get(url, params=params)
  if response.status_code == 200:
      return response.json()
  else:
      return {"error": f"Could not retrieve data. Status code: {response.status_code}. Message: {response.text}"}

# Function to query the SFTool API for system resources
def get_building_system_resources(system_slug):
  url = f"{base_url}/building-systems/{system_slug}/resources"
  params = {"api_key": api_key}
  response = requests.get(url, params=params)
  if response.status_code == 200:
      return response.json()
  else:
      return {"error": f"Could not retrieve resources. Status code: {response.status_code}. Message: {response.text}"}

# Display results
if selected_system:
  system_slug = building_systems[selected_system]
  
  with st.spinner("Fetching system information..."):
      system_info = get_building_system_info(system_slug)
  
  if "error" in system_info:
      st.error(system_info["error"])
  else:
      st.subheader(f"Information for {selected_system}")
      st.json(system_info)
  
  with st.spinner("Fetching system resources..."):
      system_resources = get_building_system_resources(system_slug)
  
  if "error" in system_resources:
      st.error(system_resources["error"])
  else:
      st.subheader(f"Resources for {selected_system}")
      st.json(system_resources)

# Add error handling for API key
if api_key == "DEMO_KEY":
  st.warning("Using DEMO_KEY. For full access, please set your SFTOOL_API_KEY in Streamlit secrets.")
