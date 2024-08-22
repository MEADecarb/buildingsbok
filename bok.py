import streamlit as st
import requests
import pandas as pd

# Access the API key from Streamlit secrets (or use DEMO_KEY for testing)
api_key = st.secrets.get("SFTOOL_API_KEY", "DEMO_KEY")

# Set the correct API base URL
base_url = "https://api.gsa.gov/sustainability/sftool/v1"

# Set up the Streamlit app
st.title("SFTool Building Systems and Workspaces Query")

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

# Function to get workspace info
def get_workspace_info(workspace_id):
  url = f"{base_url}/workspaces/{workspace_id}"
  params = {"api_key": api_key}
  response = requests.get(url, params=params)
  if response.status_code == 200:
      return response.json()
  else:
      return {"error": f"Could not retrieve workspace info. Status code: {response.status_code}"}

# Function to get workspace material groups
def get_workspace_material_groups(workspace_id):
  url = f"{base_url}/workspaces/{workspace_id}/material-groups"
  params = {"api_key": api_key}
  response = requests.get(url, params=params)
  if response.status_code == 200:
      return response.json()
  else:
      return {"error": f"Could not retrieve material groups. Status code: {response.status_code}"}

# Function to convert JSON to DataFrame
def json_to_dataframe(data):
  if isinstance(data, list):
      return pd.json_normalize(data)
  elif isinstance(data, dict):
      return pd.json_normalize([data])
  else:
      return pd.DataFrame()

# Display building system results
if selected_system:
  with st.spinner("Fetching building system data..."):
      system_info = get_building_system_info(selected_system)
      system_resources = get_building_system_resources(selected_system)
      system_bundles = get_system_bundles(selected_system)
  
  if system_info and "error" not in system_info:
      st.subheader(f"Information for {selected_system}")
      df_info = json_to_dataframe(system_info)
      st.dataframe(df_info)
  
  if system_resources and "error" not in system_resources:
      st.subheader(f"Resources for {selected_system}")
      df_resources = json_to_dataframe(system_resources)
      st.dataframe(df_resources)
  
  if system_bundles and "error" not in system_bundles:
      st.subheader(f"System Bundles for {selected_system}")
      df_bundles = json_to_dataframe(system_bundles)
      st.dataframe(df_bundles)
  
  if "error" in system_info or "error" in system_resources or "error" in system_bundles:
      st.error("An error occurred while fetching some building system data. Please check the API key and try again.")

# Workspace section
st.title("Workspace Information")

# Workspace options
workspace_options = {
  "HVAC": 83,
  "Lighting": 84,
  "Submetering": 85
}

selected_workspace = st.selectbox("Select a workspace:", list(workspace_options.keys()))

if selected_workspace:
  workspace_id = workspace_options[selected_workspace]
  
  with st.spinner("Fetching workspace data..."):
      workspace_info = get_workspace_info(workspace_id)
      material_groups = get_workspace_material_groups(workspace_id)
  
  if workspace_info and "error" not in workspace_info:
      st.subheader(f"Workspace Information for {selected_workspace}")
      df_workspace = json_to_dataframe(workspace_info)
      st.dataframe(df_workspace)
  
  if material_groups and "error" not in material_groups:
      st.subheader(f"Material Groups for {selected_workspace}")
      df_material_groups = json_to_dataframe(material_groups)
      st.dataframe(df_material_groups)
  
  if "error" in workspace_info or "error" in material_groups:
      st.error("An error occurred while fetching workspace data. Please check the API key and try again.")

# Add error handling for API key
if api_key == "DEMO_KEY":
  st.warning("You are using the DEMO_KEY. For full access, please set your SFTOOL_API_KEY in Streamlit secrets.")
