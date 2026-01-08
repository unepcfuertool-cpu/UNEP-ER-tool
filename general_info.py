# general_info.py
import streamlit as st
import shared_state
from datetime import date

# Import data safely
try:
    import imported_data
    SOIL_TYPES = imported_data.SOIL_TYPES
    CLIMATES = imported_data.CLIMATES
    MOISTURES = imported_data.MOISTURES
except ImportError:
    # Defaults if sync failed
    SOIL_TYPES = ["Spodic soils", "Volcanic soils", "Clay soils", "Sandy soils", "Loam soils", "Wetland/Organic soils"]
    CLIMATES = ["Tropical montane", "Tropical wet", "Tropical dry"]
    MOISTURES = ["Moist", "Wet", "Dry"]

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
        with col2:
            st.markdown("#### **Project Site & Duration**")
            region = st.selectbox("Region", ["Central Africa", "Indonesia", "Brazil"], key="region_selector")
            if region != shared_state.get("gi_region"): shared_state.set("gi_region", region)
            
            country = st.selectbox("Country", ["Cameroon", "Gabon", "DRC", "Congo", "Eq. Guinea", "CAR"] if region == "Central Africa" else [region], key="country_selector")
            shared_state.set("gi_country", country)
            
            st.divider()
            c1, c2 = st.columns(2)
            impl = c1.number_input("Implementation (yrs)", value=4, key="gi_impl")
            cap = c2.number_input("Capitalization (yrs)", value=10, key="gi_cap")
            st.caption(f"Total Duration: {impl + cap} Years")

    # 2. ACTIVITIES
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

    # 3. PARAMETERS (Grid Layout)
    st.markdown("### 3. Parameters")
    with st.container(border=True):
        st.caption("Review defaults. Enter 'Override' only if necessary.")
        
        # Environmental Selectors
        p1, p2, p3 = st.columns(3)
        p1.selectbox("Climate", CLIMATES, key="gi_climate")
        p2.selectbox("Moisture", MOISTURES, key="gi_moisture")
        p3.selectbox("Soil Type", SOIL_TYPES, key="gi_soil")
        
        st.divider()
        
        # Parameter Grid
        h1, h2, h3, h4 = st.columns([2, 1, 1.5, 2])
        h1.markdown("**Parameter**"); h2.markdown("**Unit**"); h3.markdown("**Default**"); h4.markdown("**Custom Override**")
        st.markdown("---")

        # SOC
        r1_c1, r1_c2, r1_c3, r1_c4 = st.columns([2, 1, 1.5, 2])
        r1_c1.write("Soil Organic Carbon")
        r1_c2.write("tC/ha")
        r1_c3.code("47.0")
        r1_c4.number_input("SOC Override", min_value=0.0, key="gi_soc_override", label_visibility="collapsed")

        # Soil Period
        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns([2, 1, 1.5, 2])
        r2_c1.write("Soil Calc Period")
        r2_c2.write("Years")
        r2_c3.code("20")
        
        # Handle State for Soil Divisor
        curr_soil = shared_state.get("soil_divisor") or 20
        new_soil = r2_c4.number_input("Soil Period", value=int(curr_soil), step=1, key="soil_input_unique", label_visibility="collapsed")
        if new_soil != shared_state.get("soil_divisor"):
            shared_state.set("soil_divisor", new_soil)