# main.py
import streamlit as st
import importlib # Required to force reload of modules
import shared_state

# Import all modules
import start_page
import energy
import arr
import agri
import forest
import results 

# --- FORCE RELOAD MODULES ---
# This ensures that if you change code in results.py, Streamlit sees it immediately.
importlib.reload(results)
importlib.reload(start_page)
importlib.reload(energy)
importlib.reload(arr)
importlib.reload(agri)
importlib.reload(forest)

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Carbon Mitigation Tool",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- NAVIGATION ---
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "0 Start"

pages = [
    "0 Start", 
    "1 Energy", 
    "2 Afforestation & Reforestation", 
    "3 Agriculture", 
    "4 Forestry & Conservation", 
    "Results"
]

selected_page = st.radio(
    "Navigation", 
    pages, 
    index=pages.index(st.session_state["current_page"]), 
    horizontal=True, 
    label_visibility="collapsed"
)

if selected_page != st.session_state["current_page"]:
    st.session_state["current_page"] = selected_page
    st.rerun()

st.divider()

# --- RENDER SELECTED MODULE ---
if selected_page == "0 Start":
    start_page.render_start_page()

elif selected_page == "1 Energy":
    energy.render_energy_module()

elif selected_page == "2 Afforestation & Reforestation":
    arr.render_arr_module()

elif selected_page == "3 Agriculture":
    agri.render_agri_module()

elif selected_page == "4 Forestry & Conservation":
    forest.render_forest_module()

elif selected_page == "Results":
    results.render_results_module()