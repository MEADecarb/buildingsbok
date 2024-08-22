import streamlit as st
import requests
import pandas as pd
import re

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
      allowed_systems = ["Lighting", "HVAC", "IEQ", "Submetering"]
      return {system['name']: system['id'] for system in systems if system['name'] in allowed_systems}
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

# Function to get all workspaces
def get_workspaces():
  url = f"{base_url}/workspaces"
  params = {"api_key": api_key}
  response = requests.get(url, params=params)
  if response.status_code == 200:
      workspaces = response.json()
      return {workspace['name']: workspace['id'] for workspace in workspaces if workspace['name'] != 'Enclosed Conference'}
  else:
      st.error(f"Failed to fetch workspaces. Status code: {response.status_code}")
      return {}

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

# Function to remove HTML tags
def remove_html_tags(text):
  clean = re.compile('<.*?>')
  return re.sub(clean, '', text)

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
      with st.expander("Resources", expanded=False):
          df_resources = json_to_dataframe(system_resources)
          st.dataframe(df_resources)
  
  if system_bundles and "error" not in system_bundles:
      st.subheader(f"System Bundles for {selected_system}")
      df_bundles = json_to_dataframe(system_bundles)
      if 'id' in df_bundles.columns:
          df_bundles = df_bundles.drop(columns=['id'])
      if 'description' in df_bundles.columns:
          df_bundles['description'] = df_bundles['description'].apply(remove_html_tags)
      if 'system_components' in df_bundles.columns:
          df_bundles = df_bundles.drop(columns=['system_components'])
      st.dataframe(df_bundles)
  
  if "error" in system_info or "error" in system_resources or "error" in system_bundles:
      st.error("An error occurred while fetching some building system data. Please check the API key and try again.")

# Workspace section
st.title("Workspace Information")

# Get all workspaces
workspaces = get_workspaces()

# User selects a workspace from the dropdown
selected_workspace = st.selectbox("Select a workspace:", list(workspaces.keys()))

if selected_workspace:
  workspace_id = workspaces[selected_workspace]
  
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
      df_material_groups = df_material_groups.iloc[2:]  # Remove the first 2 rows
      st.dataframe(df_material_groups)
  
  if "error" in workspace_info or "error" in material_groups:
      st.error("An error occurred while fetching workspace data. Please check the API key and try again.")

# Add error handling for API key
if api_key == "DEMO_KEY":
  st.warning("You are using the DEMO_KEY. For full access, please set your SFTOOL_API_KEY in Streamlit secrets.")
