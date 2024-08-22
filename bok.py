import streamlit as st
import requests

# Access the API key from Streamlit secrets (or use DEMO_KEY for testing)
api_key = st.secrets.get("SFTOOL_API_KEY", "DEMO_KEY")

# Set the correct API base URL
base_url = "https://api.gsa.gov/sustainability/sftool/v1"

# Set up the Streamlit app
st.title("SFTool Building Systems Query")

# Function to get building systems
def get_building_systems():
  url = f"{base_url}/building-systems"
  params = {"api_key": api_key}
  response = requests.get(url, params=params)
  if response.status_code == 200:
      systems = response.json()
      return {system['name']: system['id'] for system in systems}
  else:
      st.error(f"Failed to fetch building systems. Status code: {response.status_code}")
      return {}

# Get building systems
building_systems = get_building_systems()

# User selects a building system from the dropdown
selected_system = st.selectbox("Select a building system:", list(building_systems.keys()))

# Function to get building system info
def get_building_system_info(system_name):
  system_id = building_systems.get(system_name)
  if system_id:
      url = f"{base_url}/building-systems/{system_id}"
      params = {"api_key": api_key}
      response = requests.get(url, params=params)
      if response.status_code == 200:
          return response.json()
      else:
          return {"error": f"Could not retrieve data. Status code: {response.status_code}"}
  return None

# Function to get building system resources
def get_building_system_resources(system_name):
  system_id = building_systems.get(system_name)
  if system_id:
      url = f"{base_url}/building-systems/{system_id}/resources"
      params = {"api_key": api_key}
      response = requests.get(url, params=params)
      if response.status_code == 200:
          return response.json()
      else:
          return {"error": f"Could not retrieve resources. Status code: {response.status_code}"}
  return None

# Function to get system bundles
def get_system_bundles(system_name):
  system_id = building_systems.get(system_name)
  if system_id:
      url = f"{base_url}/building-systems/{system_id}/system-bundles"
      params = {"api_key": api_key}
      response = requests.get(url, params=params)
      if response.status_code == 200:
          return response.json()
      else:
          return {"error": f"Could not retrieve system bundles. Status code: {response.status_code}"}
  return None

# Display results
if selected_system:
  with st.spinner("Fetching data..."):
      system_info = get_building_system_info(selected_system)
      system_resources = get_building_system_resources(selected_system)
      system_bundles = get_system_bundles(selected_system)
  
  if system_info and "error" not in system_info:
      st.subheader(f"Information for {selected_system}")
      st.json(system_info)
  
  if system_resources and "error" not in system_resources:
      st.subheader(f"Resources for {selected_system}")
      st.json(system_resources)
  
  if system_bundles and "error" not in system_bundles:
      st.subheader(f"System Bundles for {selected_system}")
      st.json(system_bundles)
  
  if "error" in system_info or "error" in system_resources or "error" in system_bundles:
      st.error("An error occurred while fetching some data. Please check the API key and try again.")

# Add error handling for API key
if api_key == "DEMO_KEY":
  st.warning("You are using the DEMO_KEY. For full access, please set your SFTOOL_API_KEY in Streamlit secrets.")
