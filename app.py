# app.py
import streamlit as st
import pandas as pd
import shared_state
import general_info
import agri
import forest

# 1. Page Config
st.set_page_config(page_title="CAFI Mitigation Tool", layout="wide")

# 2. Initialize Shared State
shared_state.init_state()

# 3. Create Top Navigation Tabs
tabs = st.tabs([
    "0 Start", 
    "1 Energy", 
    "2 Afforestation & Reforestation", 
    "3 Agriculture", 
    "4 Forestry & Conservation", 
    "Results"
])

# --- TAB 0: Start / Landing Page ---
with tabs[0]:
    general_info.render_general_info()

# --- TAB 1: Energy ---
with tabs[1]:
    st.header("1. Energy")
    st.info("Energy module coming soon...")

# --- TAB 2: ARR ---
with tabs[2]:
    st.header("2. Afforestation & Reforestation")
    st.info("ARR module coming soon...")

# --- TAB 3: Agriculture ---
with tabs[3]:
    agri.render_agri_module()

# --- TAB 4: Forestry ---
with tabs[4]:
    forest.render_forest_module()

# --- TAB 5: Results ---
with tabs[5]:
    st.header("Results Summary")
    
    # Retrieve data safely
    grand_total_agri = shared_state.get("agri_grand_total") or 0.0
    grand_total_forest = shared_state.get("forest_grand_total") or 0.0
    total_combined = grand_total_agri + grand_total_forest
    
    # Display Metric
    st.metric("Total Project Emissions Reduction", f"{total_combined:,.2f} tCO2e")

    # Detailed Breakdown for Agriculture
    results_data = shared_state.get("agri_results_table") or []
    if results_data:
        st.subheader("Agriculture Breakdown")
        df_res = pd.DataFrame(results_data)
        st.dataframe(
            df_res, 
            column_config={
                "Emission Reduction": st.column_config.NumberColumn(format="%.2f"),
            },
            use_container_width=True
        )
        
        # Stacked Chart
        import plotly.express as px
        if "Section" in df_res.columns and "Emission Reduction" in df_res.columns:
            fig = px.bar(
                df_res, 
                x="Section", 
                y="Emission Reduction", 
                color="Crop", 
                title="Agri Reductions by Crop System"
            )
            st.plotly_chart(fig, use_container_width=True)