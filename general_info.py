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

    # 1. DESCRIPTION
    st.markdown("### 1. Description")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### **Project Details**")
            st.text_input("User Name", key="gi_user_name")
            st.date_input("Date", key="gi_date", value=date.today())
            st.text_input("Project Name", key="gi_project_name")
            st.text_input("Funding Agency", key="gi_funding_agency", value="CAFI")
            st.text_input("Executing Agency", key="gi_executing_agency")
            st.number_input("Project Cost (USD)", key="gi_project_cost", step=1000)

        with col2:
            st.markdown("#### **Project Site & Environment**")
            
            # --- UPDATED REGION & COUNTRY LOGIC ---
            region_list = ["Central Africa", "Southeast Asia", "South America"]
            
            # Get current region safely
            current_reg = shared_state.get("gi_region")
            reg_index = region_list.index(current_reg) if current_reg in region_list else 0
            
            region = st.selectbox("Region", region_list, index=reg_index, key="region_selector")
            if region != shared_state.get("gi_region"): 
                shared_state.set("gi_region", region)
            
            # Define Countries based on Region
            if region == "Central Africa":
                country_list = [
                    "Cameroon", 
                    "Central African Republic", 
                    "Republic of Congo", 
                    "Democratic Republic of the Congo", 
                    "Equatorial Guinea", 
                    "Gabon"
                ]
            elif region == "Southeast Asia":
                country_list = ["Indonesia"]
            elif region == "South America":
                country_list = ["Brazil"]
            else:
                country_list = []

            # Get current country safely
            current_country = shared_state.get("gi_country")
            cnt_index = country_list.index(current_country) if current_country in country_list else 0

            country = st.selectbox("Country", country_list, index=cnt_index, key="country_selector")
            shared_state.set("gi_country", country)
            
            st.divider()
            
            e1, e2, e3 = st.columns(3)
            e1.selectbox("Climate", CLIMATE, key="gi_climate")
            e2.selectbox("Moisture", MOISTURE, key="gi_moisture")
            e3.selectbox("Soil Type", SOIL_TYPE, key="gi_soil")
            st.divider()
            
            d1, d2 = st.columns(2)
            d1.number_input("Implementation (yrs)", value=4, key="gi_impl")
            d2.number_input("Capitalization (yrs)", value=10, key="gi_cap")

    # 2. ACTIVITIES REPORTED
    st.markdown("### 2. Activities Reported")
    with st.container(border=True):
        col_act_1, col_act_2 = st.columns(2)
        with col_act_1:
            st.markdown("**Energy**")
            st.checkbox("Improved Cookstoves manufacturing and distribution", value=True, key="act_energy_1")
            st.checkbox("Improved transformation efficiency", value=True, key="act_energy_2")
            st.checkbox("Wood fuel substitution", value=False, key="act_energy_3")
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

    # 3. PARAMETERS
    st.markdown("### 3. Parameters")
    
    def make_param_box(title, data_dict=None, custom_component=None):
        with st.container(border=True):
            st.markdown(f"**{title}**")
            if custom_component:
                custom_component()
            elif data_dict:
                st.dataframe(pd.DataFrame(data_dict), hide_index=True, use_container_width=True)

    r1c1, r1c2, r1c3 = st.columns(3)
    
    with r1c1:
        with st.container(border=True):
            st.markdown("**Global warming potential**")
            h1, h2, h3 = st.columns([1.5, 1, 1])
            h2.caption("Tier 1 (Def)")
            h3.caption("Tier 2 (Any)")
            for gas, val in parameters.GWP_DEFAULTS.items():
                c1, c2, c3 = st.columns([1.5, 1, 1])
                c1.write(gas)
                c2.write(val)
                c3.text_input(f"t2_{gas}", label_visibility="collapsed", key=f"gwp_{gas}")

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

    r2c1, r2c2, r2c3 = st.columns([2, 1.5, 1])
    with r2c1:
        make_param_box("Emission factor traditional cookstoves (g/kg) [default]", parameters.EF_COOKSTOVES_DATA)
    with r2c2:
        make_param_box("Quantity of fuel used", parameters.FUEL_QTY_DATA)
    with r2c3:
        make_param_box("Energy generated", parameters.ENERGY_GEN_DATA)

    make_param_box("Emission factor charcoal production (g/kg) [default]", parameters.EF_CHARCOAL_DATA)

    r4c1, r4c2 = st.columns([1.5, 1])
    with r4c1:
        make_param_box("Emission factor of substitution fuel [default]", parameters.EF_SUBSTITUTION_DATA)
    with r4c2:
        make_param_box("Carbon intensity of electricity in the Congo Basin [default]", parameters.C_INTENSITY_DATA)
        make_param_box("Emission factor RIL-C", parameters.RIL_C_DATA)