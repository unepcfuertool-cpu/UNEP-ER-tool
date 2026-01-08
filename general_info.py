# general_info.py
import streamlit as st
import shared_state
from datetime import date
import parameters

# Try to import synced lists, ensuring we use Singular variable names locally
try:
    import imported_data
    # Map imported plural lists to Singular variables as requested
    SOIL_TYPE = imported_data.SOIL_TYPES
    CLIMATE = imported_data.CLIMATES
    MOISTURE = imported_data.MOISTURES
except ImportError:
    # Defaults
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
            
            # 1. Location
            region = st.selectbox("Region", ["Central Africa", "Indonesia", "Brazil"], key="region_selector")
            if region != shared_state.get("gi_region"): shared_state.set("gi_region", region)
            
            country = st.selectbox("Country", ["Cameroon", "Gabon", "DRC", "Congo", "Eq. Guinea", "CAR"] if region == "Central Africa" else [region], key="country_selector")
            shared_state.set("gi_country", country)
            
            st.divider()

            # 2. Environmental Context
            e1, e2, e3 = st.columns(3)
            with e1:
                st.selectbox("Climate", CLIMATE, key="gi_climate")
            with e2:
                st.selectbox("Moisture", MOISTURE, key="gi_moisture")
            with e3:
                st.selectbox("Soil Type", SOIL_TYPE, key="gi_soil")

            st.divider()
            
            # 3. Duration
            d1, d2 = st.columns(2)
            d1.number_input("Implementation (yrs)", value=4, key="gi_impl")
            d2.number_input("Capitalization (yrs)", value=10, key="gi_cap")

    # ==========================================
    # 2. ACTIVITIES REPORTED
    # ==========================================
    st.markdown("### 2. Activities Reported")
    with st.container(border=True):
        
        # We create a 2-column layout to mimic the visual balance
        col_act_1, col_act_2 = st.columns(2)
        
        with col_act_1:
            # --- Energy ---
            st.markdown("**Energy**")
            st.checkbox("Improved Cookstoves manufacturing and distribution", key="act_energy_1")
            st.checkbox("Improved transformation efficiency", key="act_energy_2")
            st.checkbox("Wood fuel substitution", key="act_energy_3")
            st.checkbox("Cogeneration", key="act_energy_4")

            st.divider()

            # --- Afforestation & Restauration ---
            st.markdown("**Afforestation & Restauration**")
            st.checkbox("Small, medium and large-scale agroforestry", key="act_arr_1")
            st.checkbox("Large-scale forest plantations", key="act_arr_2")
            st.checkbox("Natural regeneration", key="act_arr_3")

        with col_act_2:
            # --- Agriculture ---
            st.markdown("**Agriculture**")
            st.checkbox("Deforestation-free outgrower", value=True, key="act_agri_1")
            st.checkbox("Agro-industrial expansion", value=True, key="act_agri_2")
            st.checkbox("Sustainable intensification", value=True, key="act_agri_3")

            st.divider()

            # --- Forestry & Conservation ---
            st.markdown("**Forestry & Conservation**")
            st.checkbox("Forest Concessions Transitioning to Reduced Impact Logging", key="act_forest_1")
            st.checkbox("Transformation factories or equipment for sustainably sourced", key="act_forest_2")
            st.checkbox("Forest conservation", key="act_forest_3")

    # ==========================================
    # 3. PARAMETERS (TIER 1 & TIER 2)
    # ==========================================
    st.markdown("### 3. Parameters")
    with st.container(border=True):
        st.caption("Review Tier 1 defaults below. Enter Tier 2 (Local) data in the 'Override' column if available.")

        # --- GRID LAYOUT ---
        h1, h2, h3, h4 = st.columns([2.5, 1, 1, 2])
        h1.markdown("**PARAMETER**")
        h2.markdown("**UNIT**")
        h3.markdown("**DEFAULT (TIER 1)**")
        h4.markdown("**OVERRIDE (TIER 2)**")
        st.markdown("---")

        def param_row(label, unit, default_val, key_suffix):
            c1, c2, c3, c4 = st.columns([2.5, 1, 1, 2])
            c1.write(f"**{label}**")
            c2.write(unit)
            c3.code(str(default_val))
            c4.number_input(f"{label}", min_value=0.0, key=f"p_{key_suffix}", label_visibility="collapsed", help=f"Default: {default_val}")

        # --- B. GLOBAL CONSTANTS ---
        st.markdown("###### **Global Constants**")
        param_row("GWP CO2", "Index", parameters.GWP["CO2"], "gwp_co2")
        param_row("GWP CH4", "Index", parameters.GWP["CH4"], "gwp_ch4")
        param_row("GWP N2O", "Index", parameters.GWP["N2O"], "gwp_n2o")
        param_row("Carbon Fraction (Biomass)", "Frac", parameters.CARBON_FRACTION_DEFAULT, "c_fract")

        st.markdown("###### **Soil Parameters**")
        param_row("Ref. Soil Organic Carbon", "tC/ha", parameters.REF_SOC_DEFAULT, "soc_ref")
        
        # Soil Period (Special State Handling)
        c1, c2, c3, c4 = st.columns([2.5, 1, 1, 2])
        c1.write("**Soil Calculation Period**")
        c2.write("Years")
        c3.code("20")
        curr_soil = shared_state.get("soil_divisor") or 20
        new_soil = c4.number_input("Soil Period", value=int(curr_soil), step=1, key="soil_input_unique", label_visibility="collapsed")
        if new_soil != shared_state.get("soil_divisor"): shared_state.set("soil_divisor", new_soil)

        st.markdown("###### **Energy & Fuel**")
        param_row("EF Traditional Cookstoves", "tCO2e/t", parameters.ENERGY_DEFAULTS["EF_traditional_cookstove"], "ef_cook")
        param_row("Default Fuel Qty Used", "t/hh/yr", parameters.ENERGY_DEFAULTS["Default_fuel_qty"], "fuel_qty")
        param_row("EF Charcoal Production", "tCO2e/t", parameters.ENERGY_DEFAULTS["EF_charcoal_production"], "ef_char")
        param_row("EF Substitution Fuel", "tCO2/TJ", parameters.ENERGY_DEFAULTS["EF_substitution_fuel"], "ef_sub")
        param_row("C-Intensity Electricity", "tCO2/MWh", parameters.ENERGY_DEFAULTS["C_intensity_electricity"], "c_grid")
        param_row("Default Energy Generated", "MWh/yr", parameters.ENERGY_DEFAULTS["Default_energy_gen"], "energy_gen")

        st.markdown("###### **Forestry**")
        param_row("EF RIL-C", "tCO2e/m3", parameters.RIL_C_FACTOR, "ef_rilc")