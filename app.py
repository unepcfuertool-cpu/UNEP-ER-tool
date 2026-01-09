# app.py
import streamlit as st
import importlib
import shared_state
import parameters

# --- IMPORT MODULES THAT EXIST ---
import general_info  # This is your "Start Page"
import agri          # This is your "Agriculture" module
import results       # This is your "Results" dashboard

# --- FORCE RELOAD (To ensure updates are seen) ---
importlib.reload(general_info)
importlib.reload(agri)
importlib.reload(results)
importlib.reload(parameters)

st.set_page_config(page_title="CAFI Mitigation Tool", layout="wide")
shared_state.init_state()

# --- TABS CONFIGURATION ---
tabs = st.tabs([
    "0 Start", 
    "1 Energy", 
    "2 Afforestation & Reforestation", 
    "3 Agriculture", 
    "4 Forestry & Conservation", 
    "Results"
])

# --- TAB 0: START (General Info) ---
with tabs[0]:
    general_info.render_general_info()

# --- TAB 1: ENERGY (Placeholder) ---
with tabs[1]:
    st.header("1. Energy")
    st.info("🚧 Module under development. (File 'energy.py' not found)")

# --- TAB 2: ARR (Placeholder) ---
with tabs[2]:
    st.header("2. Afforestation & Reforestation")
    st.info("🚧 Module under development. (File 'arr.py' not found)")

# --- TAB 3: AGRICULTURE (Active) ---
with tabs[3]:
    agri.render_agri_module()

# --- TAB 4: FOREST (Placeholder) ---
with tabs[4]:
    st.header("4. Forestry & Conservation")
    st.info("🚧 Module under development. (File 'forest.py' not found)")

# --- TAB 5: RESULTS (Active) ---
with tabs[5]:
    results.render_results_module()