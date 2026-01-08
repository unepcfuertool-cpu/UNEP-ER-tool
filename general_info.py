# general_info.py
import streamlit as st
import pandas as pd
import shared_state
from datetime import date
import parameters

# Try to import synced lists
try:
    import imported_data
    SOIL_TYPE = imported_data.SOIL_TYPES
    CLIMATE = imported_data.CLIMATES
    MOISTURE = imported_data.MOISTURES
except ImportError:
    SOIL_TYPE = ["Spodic soils", "Volcanic soils", "Clay soils", "Sandy soils", "Loam soils", "Wetland/Organic soils"]
    CLIMATE = ["Tropical montane", "Tropical wet", "Tropical dry"]
    MOISTURE = ["Moist", "Wet", "Dry"]

def render_general_info():
    st.markdown("""
        <div style='background-color: white; padding: 15px; border-radius: 5px; border: 1px solid #ddd; margin-bottom: 20px;'>
            <h2 style='color: #2E86C1; margin:0; text-align: center;'>CAFI Mitigation Tool</h2>
        </div>
    """, unsafe_allow_html=True)

    # ==========================================
    # 1. DESCRIPTION
    # ==========================================
    st.markdown("### 1. Description")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        
        # --- LEFT: Project Details ---
        with col1:
            st.markdown("#### **Project Details**")
            st.text_input("User Name", key="gi_user_name")
            st.date_input("Date", key="gi_date", value=date.today())
            st.text_input("Project Name", key="gi_project_name")
            st.text_input("Funding Agency", key="gi_funding_agency", value="CAFI")
            st.text_input("Executing Agency", key="gi_executing_agency")
            st.number_input("Project Cost (USD)", key="gi_project_cost", step=1000)

        # --- RIGHT: Site & Environment ---
        with col2:
            st.markdown("#### **Project Site & Environment**")
            
            # Location
            region = st.selectbox("Region", ["Central Africa", "Indonesia", "Brazil"], key="region_selector")
            if region != shared_state.get("gi_region"): shared_state.set("gi_region", region)
            
            country = st.selectbox("Country", ["Cameroon", "Gabon", "DRC", "Congo", "Eq. Guinea", "CAR"] if region == "Central Africa" else [region], key="country_selector")
            shared_state.set("gi_country", country)
            
            st.divider()

            # Environmental Context
            e1, e2, e3 = st.columns(3)
            e1.selectbox("Climate", CLIMATE, key="gi_climate")
            e2.selectbox("Moisture", MOISTURE, key="gi_moisture")
            e3.selectbox("Soil Type", SOIL_TYPE, key="gi_soil")

            st.divider()
            
            # Duration
            d1, d2 = st.columns(2)
            d1.number_input("Implementation (yrs)", value=4, key="gi_impl")
            d2.number_input("Capitalization (yrs)", value=10, key="gi_cap")

    # ==========================================
    # 2. ACTIVITIES REPORTED
    # ==========================================
    st.markdown("### 2. Activities Reported")
    with st.container(border=True):
        col_act_1, col_act_2 = st.columns(2)
        
        with col_act_1:
            st.markdown("**Energy**")
            st.checkbox("Improved Cookstoves manufacturing and distribution", value=True, key="act_energy_1")
            st.checkbox("Improved transformation efficiency", value=True, key="act_energy_2")
            st.checkbox("Wood fuel substitution", value=False, key="act_energy_3") # Empty in image
            st.checkbox("Cogeneration", value=True, key="act_energy_4")

            st.divider()
            st.markdown("**Afforestation & Restauration**")
            st.checkbox("Small, medium and large-scale agroforestry", value=True, key="act_arr_1")
            st.checkbox("Large-scale forest plantations", value=True, key="act_arr_2")
            st.checkbox("Natural regeneration", value=True, key="act_arr_3")

        with col_act_2:
            st.markdown("**Agriculture**")
            st.checkbox("Deforestation-free outgrower", value=True, key="act_agri_1")
            st.checkbox("Agro-industrial expansion", value=True, key="act_agri_2")
            st.checkbox("Sustainable intensification", value=True, key="act_agri_3")

            st.divider()
            st.markdown("**Forestry & Conservation**")
            st.checkbox("Forest Concessions Transitioning to Reduced Impact Logging", value=True, key="act_forest_1")
            st.checkbox("Transformation factories or equipment for sustainably sourced", value=True, key="act_forest_2")
            st.checkbox("Forest conservation", value=True, key="act_forest_3")

    # ==========================================
    # 3. PARAMETERS (Mirroring Images)
    # ==========================================
    st.markdown("### 3. Parameters")
    
    # Helper to create those "Blue Header" tables
    def make_param_box(title, data_dict=None, custom_component=None):
        with st.container(border=True):
            st.markdown(f"**{title}**")
            if custom_component:
                custom_component()
            elif data_dict:
                st.dataframe(pd.DataFrame(data_dict), hide_index=True, use_container_width=True)

    # --- ROW 1: GWP | SOC | Carbon Fraction ---
    r1c1, r1c2, r1c3 = st.columns(3)
    
    # 1.1 Global Warming Potential
    with r1c1:
        with st.container(border=True):
            st.markdown("**Global warming potential**")
            # Custom grid layout for Tier 1 / Tier 2
            h1, h2, h3 = st.columns([1.5, 1, 1])
            h2.caption("Tier 1 (Def)")
            h3.caption("Tier 2 (Any)")
            
            for gas, val in parameters.GWP_DEFAULTS.items():
                c1, c2, c3 = st.columns([1.5, 1, 1])
                c1.write(gas)
                c2.write(val)
                c3.text_input(f"t2_{gas}", label_visibility="collapsed", key=f"gwp_{gas}")

    # 1.2 Reference Soil Organic Carbon
    with r1c2:
        with st.container(border=True):
            st.markdown("**Reference soil organic carbon**")
            h1, h2, h3 = st.columns([1.5, 1, 1])
            h2.caption("Tier 1 (Def)")
            h3.caption("Tier 2 (Any)")
            
            c1, c2, c3 = st.columns([1.5, 1, 1])
            c1.write("SOC (tC/ha)")
            c2.write(parameters.REF_SOC_DEFAULT)
            c3.text_input("t2_soc", label_visibility="collapsed", key="soc_ref")

    # 1.3 Carbon Fraction
    with r1c3:
        with st.container(border=True):
            st.markdown("**Carbon fraction**")
            h1, h2, h3 = st.columns([1.5, 1, 1])
            h2.caption("Tier 1 (Def)")
            h3.caption("Tier 2 (Any)")
            
            c1, c2, c3 = st.columns([1.5, 1, 1])
            c1.write("Carbon fraction")
            c2.write(parameters.CARBON_FRACTION_DEFAULT)
            c3.text_input("t2_cf", label_visibility="collapsed", key="c_fract")

    # --- ROW 2: Cookstoves | Fuel Qty | Energy Gen ---
    r2c1, r2c2, r2c3 = st.columns([2, 1.5, 1])
    with r2c1:
        make_param_box("Emission factor traditional cookstoves (g/kg) [default]", parameters.EF_COOKSTOVES_DATA)
    with r2c2:
        make_param_box("Quantity of fuel used", parameters.FUEL_QTY_DATA)
    with r2c3:
        make_param_box("Energy generated", parameters.ENERGY_GEN_DATA)

    # --- ROW 3: Charcoal Production ---
    # (Matches image_69cc85.png)
    make_param_box("Emission factor charcoal production (g/kg) [default]", parameters.EF_CHARCOAL_DATA)

    # --- ROW 4: Substitution Fuel | C-Intensity | RIL-C ---
    r4c1, r4c2 = st.columns([1.5, 1])
    
    with r4c1:
        make_param_box("Emission factor of substitution fuel [default]", parameters.EF_SUBSTITUTION_DATA)

    with r4c2:
        # C-Intensity and RIL-C stacked vertically on the right
        make_param_box("Carbon intensity of electricity in the Congo Basin [default]", parameters.C_INTENSITY_DATA)
        make_param_box("Emission factor RIL-C", parameters.RIL_C_DATA)