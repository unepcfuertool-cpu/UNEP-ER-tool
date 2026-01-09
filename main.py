# main.py
import streamlit as st
import shared_state

# Import all modules
import start_page
import energy
import arr
import agri
import forest
import results  # <--- Make sure this is imported

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Carbon Mitigation Tool",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- NAVIGATION ---
# Initialize session state for navigation if not present
if "current_page" not in st.session_state:
    st.session_state["current_page"] = "0 Start"

# Define the list of pages
pages = [
    "0 Start", 
    "1 Energy", 
    "2 Afforestation & Reforestation", 
    "3 Agriculture", 
    "4 Forestry & Conservation", 
    "Results"
]

# Create a horizontal navigation menu
selected_page = st.radio(
    "Navigation", 
    pages, 
    index=pages.index(st.session_state["current_page"]), 
    horizontal=True, 
    label_visibility="collapsed"
)

# Update session state if changed via radio button
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
    # This MUST call the function from results.py
    results.render_results_module()