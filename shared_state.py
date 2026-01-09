# shared_state.py
import streamlit as st
from datetime import date

def init_state():
    defaults = {
        # Defaults set to None so the dropdowns start empty
        "gi_region": None,
        "gi_country": None,
        "soil_divisor": 20,
        "agri_grand_total": 0.0,
        "agri_results_table": [],
        "agri_total_1": 0.0,
        "agri_total_2": 0.0,
        "agri_total_3": 0.0,
        
        # Form fields defaults (Empty)
        "gi_user_name": "",
        "gi_project_name": "",
        "gi_funding_agency": "",
        "gi_executing_agency": "",
        "gi_project_cost": 0.0,
        "gi_impl": 0,
        "gi_cap": 0
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get(key, default=None):
    return st.session_state.get(key, default)

def set(key, value):
    st.session_state[key] = value