# general_info.py
import streamlit as st
import shared_state
from datetime import date
import parameters

# Try to import synced lists
try:
    import imported_data
    SOIL_TYPES = imported_data.SOIL_TYPES
    CLIMATES = imported_data.CLIMATES
    MOISTURES = imported_data.MOISTURES
except ImportError:
    SOIL_TYPES = ["Spodic soils", "Volcanic soils", "Clay soils", "Sandy soils", "Loam soils", "Wetland/Organic soils"]
    CLIMATES = ["Tropical montane", "Tropical wet", "Tropical dry"]
    MOISTURES = ["Moist", "Wet", "Dry"]

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
        with col1:
            st.markdown("#### **Project Details**")
            st.text_input("User Name", key="gi_user_name")
            st.date_input("Date", key="gi_date", value=date.today())
            st.text_input("Project Name", key="gi_project_name")
            st.text_input("Funding Agency", key="gi_funding_agency", value="CAFI")
        with col2:
            st.markdown("#### **Project Site & Duration**")
            region = st.selectbox("Region", ["Central Africa", "Indonesia", "Brazil"], key="region_selector")
            if region != shared_state.get("gi_region"): shared_state.set("gi_region", region)
            
            country = st.selectbox("Country", ["Cameroon", "Gabon", "DRC", "Congo", "Eq. Guinea", "CAR"] if region == "Central Africa" else [region], key="country_selector")
            shared_state.set("gi_country", country)
            
            st.divider()
            c1, c2 = st.columns(2)
            c1.number_input("Implementation (yrs)", value=4, key="gi_impl")
            c2.number_input("Capitalization (yrs)", value=10, key="gi_cap")

    # ==========================================
    # 2. ACTIVITIES
    # ==========================================
    st.markdown("### 2. Activities Reported")
    with st.container(border=True):
        c1, c2 = st.columns(2)
        with c1:
            st.checkbox("1. Energy", disabled=True, help="Placeholder")
            st.checkbox("2. ARR", disabled=True, help="Placeholder")
        with c2:
            st.markdown("**3. Agriculture**")
            st.checkbox("3.1 Outgrower", value=True)
            st.checkbox("3.2 Agro-industrial", value=True)
            st.checkbox("3.3 Intensification", value=True)
            st.markdown("---")
            st.checkbox("4. Forestry", disabled=True, help="Placeholder")

    # ==========================================
    # 3. PARAMETERS (TIER 1 & TIER 2)
    # ==========================================
    st.markdown("### 3. Parameters")
    with st.container(border=True):
        st.caption("Review Tier 1 defaults below. Enter Tier 2 (Local) data in the 'Override' column if available.")

        # --- A. Environmental Context ---
        st.markdown("#### **A. Environmental Context**")
        p1, p2, p3 = st.columns(3)
        p1.selectbox("Climate Zone", CLIMATES, key="gi_climate")
        p2.selectbox("Moisture Regime", MOISTURES, key="gi_moisture")
        p3.selectbox("Soil Type", SOIL_TYPES, key="gi_soil")

        st.divider()

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
        st.markdown("###### **B. Global Constants**")
        param_row("GWP CO2", "Index", parameters.GWP["CO2"], "gwp_co2")
        param_row("GWP CH4", "Index", parameters.GWP["CH4"], "gwp_ch4")
        param_row("GWP N2O", "Index", parameters.GWP["N2O"], "gwp_n2o")
        param_row("Carbon Fraction (Biomass)", "Frac", parameters.CARBON_FRACTION_DEFAULT, "c_fract")

        st.markdown("###### **C. Soil Parameters**")
        # Standard default, decoupled from the dropdown above
        param_row("Ref. Soil Organic Carbon", "tC/ha", parameters.REF_SOC_DEFAULT, "soc_ref")
        
        # Soil Period (Special State Handling)
        c1, c2, c3, c4 = st.columns([2.5, 1, 1, 2])
        c1.write("**Soil Calculation Period**")
        c2.write("Years")
        c3.code("20")
        curr_soil = shared_state.get("soil_divisor") or 20
        new_soil = c4.number_input("Soil Period", value=int(curr_soil), step=1, key="soil_input_unique", label_visibility="collapsed")
        if new_soil != shared_state.get("soil_divisor"): shared_state.set("soil_divisor", new_soil)

        st.markdown("###### **D. Energy & Fuel**")
        param_row("EF Traditional Cookstoves", "tCO2e/t", parameters.ENERGY_DEFAULTS["EF_traditional_cookstove"], "ef_cook")
        param_row("Default Fuel Qty Used", "t/hh/yr", parameters.ENERGY_DEFAULTS["Default_fuel_qty"], "fuel_qty")
        param_row("EF Charcoal Production", "tCO2e/t", parameters.ENERGY_DEFAULTS["EF_charcoal_production"], "ef_char")
        param_row("EF Substitution Fuel", "tCO2/TJ", parameters.ENERGY_DEFAULTS["EF_substitution_fuel"], "ef_sub")
        param_row("C-Intensity Electricity", "tCO2/MWh", parameters.ENERGY_DEFAULTS["C_intensity_electricity"], "c_grid")
        param_row("Default Energy Generated", "MWh/yr", parameters.ENERGY_DEFAULTS["Default_energy_gen"], "energy_gen")

        st.markdown("###### **E. Forestry**")
        param_row("EF RIL-C", "tCO2e/m3", parameters.RIL_C_FACTOR, "ef_rilc")