# general_info.py
import streamlit as st
import shared_state
from datetime import date

# Try to import synced data, otherwise use defaults (Safety Net)
try:
    import imported_data
    SOIL_TYPES = imported_data.SOIL_TYPES
    CLIMATES = imported_data.CLIMATES
    MOISTURES = imported_data.MOISTURES
except ImportError:
    # Fallback defaults if sync_excel.py hasn't been run yet
    SOIL_TYPES = ["Spodic soils", "Volcanic soils", "Clay soils", "Sandy soils", "Loam soils", "Wetland/Organic soils"]
    CLIMATES = ["Tropical montane", "Tropical wet", "Tropical dry"]
    MOISTURES = ["Moist", "Wet", "Dry"]

def render_general_info():
    # --- Header ---
    st.markdown("""
        <div style='background-color: white; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 25px; text-align: center;'>
            <h2 style='color: #2E86C1; margin:0;'>CAFI Mitigation Tool</h2>
            <p style='color: #555; font-size: 14px; margin-top: 5px;'>
                Ex-ante and post-ante estimation of mitigation potential
            </p>
        </div>
    """, unsafe_allow_html=True)

    # --- SECTION 1: PROJECT INFO (THE TOP) ---
    st.markdown("### 1. Project Information")
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.text_input("User Name", key="gi_user_name", placeholder="Enter user name...")
            st.text_input("Project Name", key="gi_project_name", placeholder="Enter project name...")
        
        with col2:
            st.date_input("Date", key="gi_date", value=date.today())
            st.text_input("Funding Agency", key="gi_funding_agency", value="CAFI")
        
        with col3:
            st.number_input("Project Cost (USD)", key="gi_project_cost", min_value=0, step=1000)
            st.text_input("Executing Agency", key="gi_executing_agency", placeholder="e.g. Ministry of Environment")

    # --- SECTION 2: PARAMETERS & SITE (THE BOTTOM) ---
    st.markdown("### 2. Site Parameters & Duration")
    with st.container(border=True):
        # Row 1: Location
        c1, c2, c3 = st.columns(3)
        
        with c1:
            # Region Selector
            region_opts = ["Central Africa", "Indonesia", "Brazil"]
            curr_reg = shared_state.get("gi_region") or "Central Africa"
            # Safety check if state has invalid value
            idx = region_opts.index(curr_reg) if curr_reg in region_opts else 0
            
            region = st.selectbox("Region", region_opts, index=idx)
            if region != shared_state.get("gi_region"):
                shared_state.set("gi_region", region)
        
        with c2:
            # Country Selector Logic
            if region == "Central Africa":
                c_options = ["Cameroon", "Central African Republic", "Republic of Congo", "Democratic Republic of the Congo", "Equatorial Guinea", "Gabon"]
            else:
                c_options = [region]
            
            curr_cnt = shared_state.get("gi_country")
            c_idx = c_options.index(curr_cnt) if curr_cnt in c_options else 0
            
            country = st.selectbox("Country", c_options, index=c_idx, key="gi_country_select")
            shared_state.set("gi_country", country)

        with c3:
            st.info(f"**Selected Site:** {country} ({region})")

        st.divider()

        # Row 2: Environmental Parameters
        p1, p2, p3 = st.columns(3)
        with p1:
            st.selectbox("Climate Zone", CLIMATES, key="gi_climate")
        with p2:
            st.selectbox("Moisture Regime", MOISTURES, key="gi_moisture")
        with p3:
            st.selectbox("Soil Type", SOIL_TYPES, key="gi_soil")

        st.divider()

        # Row 3: Duration
        d1, d2, d3 = st.columns(3)
        with d1:
            impl = st.number_input("Implementation Phase (yrs)", min_value=0, value=4, key="gi_impl_phase")
        with d2:
            cap = st.number_input("Capitalization Phase (yrs)", min_value=0, value=10, key="gi_cap_phase")
        with d3:
            st.metric("Total Project Duration", f"{impl + cap} Years")

    # --- SECTION 3: ACTIVITIES ---
    st.markdown("### 3. Activities Reported")
    with st.container(border=True):
        ac1, ac2 = st.columns(2)
        with ac1:
            st.checkbox("1. Energy (Cookstoves, Fuel substitution)", key="check_energy")
            st.checkbox("2. Afforestation & Reforestation", key="check_arr")
        with ac2:
            st.markdown("**3. Agriculture**")
            st.checkbox("   3.1 Deforestation-free outgrower schemes", value=True, key="check_agri_3_1")
            st.checkbox("   3.2 Agro-industrial plantations", value=True, key="check_agri_3_2")
            st.checkbox("   3.3 Sustainable intensification", value=True, key="check_agri_3_3")
            st.markdown("---")
            st.checkbox("4. Forestry & Conservation", key="check_forest")

    # Summary Footer
    st.info("ℹ️ Once you have filled in these parameters, use the tabs at the top to navigate to the specific calculation modules.")