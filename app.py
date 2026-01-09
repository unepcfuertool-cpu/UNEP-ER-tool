# app.py
import streamlit as st
import importlib
import shared_state
import general_info

# Import modules
import agri 
import results  # <--- NEW: Import the results module
import start_page
import energy
import arr
import forest
import parameters

# --- FORCE RELOAD to ensure you see changes ---
importlib.reload(agri)
importlib.reload(results)
importlib.reload(parameters)

st.set_page_config(page_title="CAFI Mitigation Tool", layout="wide")
shared_state.init_state()

# Tabs
tabs = st.tabs([
    "0 Start", 
    "1 Energy", 
    "2 Afforestation & Reforestation", 
    "3 Agriculture", 
    "4 Forestry & Conservation", 
    "Results"
])

# --- TAB 0: Start ---
with tabs[0]:
    # Use the render function from general_info or start_page depending on your preference.
    # Based on your file uploads, general_info seems to contain the start logic.
    general_info.render_general_info()

# --- TAB 1 & 2: Placeholders ---
with tabs[1]:
    # energy.render_energy_module() # Uncomment when ready
    st.header("1. Energy")
    st.info("🚧 Module under development (Placeholder)")

with tabs[2]:
    # arr.render_arr_module() # Uncomment when ready
    st.header("2. Afforestation & Reforestation")
    st.info("🚧 Module under development (Placeholder)")

# --- TAB 3: AGRICULTURE (Active) ---
with tabs[3]:
    agri.render_agri_module()

# --- TAB 4: Placeholder ---
with tabs[4]:
    # forest.render_forest_module() # Uncomment when ready
    st.header("4. Forestry & Conservation")
    st.info("🚧 Module under development (Placeholder)")

# --- TAB 5: Results ---
with tabs[5]:
    # THIS LINE WAS MISSING. It now calls the dashboard.
    results.render_results_module()