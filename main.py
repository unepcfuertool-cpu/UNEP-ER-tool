# main.py
import streamlit as st
import importlib
import shared_state
import start_page, energy, arr, agri, forest, results, parameters

# --- CRITICAL: FORCE RELOAD MODULES ---
importlib.reload(agri)
importlib.reload(results)
importlib.reload(parameters)

st.set_page_config(page_title="Carbon Mitigation Tool", layout="wide")

if "current_page" not in st.session_state: st.session_state["current_page"] = "0 Start"

pages = ["0 Start", "1 Energy", "2 Afforestation & Reforestation", "3 Agriculture", "4 Forestry & Conservation", "Results"]
sel = st.radio("Navigation", pages, index=pages.index(st.session_state["current_page"]), horizontal=True, label_visibility="collapsed")

if sel != st.session_state["current_page"]:
    st.session_state["current_page"] = sel
    st.rerun()

st.divider()

if sel == "0 Start": start_page.render_start_page()
elif sel == "1 Energy": energy.render_energy_module()
elif sel == "2 Afforestation & Reforestation": arr.render_arr_module()
elif sel == "3 Agriculture": agri.render_agri_module()
elif sel == "4 Forestry & Conservation": forest.render_forest_module()
elif sel == "Results": results.render_results_module()