# shared_state.py
import streamlit as st
from datetime import date

def init_state():
    defaults = {
        "gi_region": "Central Africa",
        "gi_country": "Cameroon",
        "soil_divisor": 20,
        "agri_grand_total": 0.0,
        "agri_results_table": [],
        # Initialize agri sub-totals to avoid errors if they aren't calculated yet
        "agri_total_1": 0.0,
        "agri_total_2": 0.0,
        "agri_total_3": 0.0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

# UPDATED: Now accepts a 'default' argument
def get(key, default=None):
    return st.session_state.get(key, default)

def set(key, value):
    st.session_state[key] = value