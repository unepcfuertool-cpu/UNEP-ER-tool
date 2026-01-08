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
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

def get(key):
    return st.session_state.get(key)

def set(key, value):
    st.session_state[key] = value