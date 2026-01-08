# general_info.py
import streamlit as st
import shared_state
from datetime import date

# Try to import synced data
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
    # --- Title ---
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
        
        # Left: Project Details
        with col1:
            st.markdown("#### **Project Details**")
            st.text_input("User Name", key="gi_user_name")
            st.date_input("Date", key="gi_date", value=date.today())
            st.text_input("Project Name", key="gi_project_name")
            st.text_input("Funding Agency", key="gi_funding_agency", value="CAFI")
            st.text_input("Executing Agency", key="gi_executing_agency")
            st.number_input("Project Cost (USD)", key="gi_project_cost", step=1000)

        # Right: Site & Duration
        with col2:
            st.markdown("#### **Project Site & Duration**")
            
            # Region
            region_opts = ["Central Africa", "Indonesia", "Brazil"]
            curr_reg = shared_state.get("gi_region") or "Central Africa"
            idx = region_opts.index(curr_reg) if curr_reg in region_opts else 0
            region = st.selectbox("Region", region_opts, index=idx)
            if region != shared_state.get("gi_region"): shared_state.set("gi_region", region)

            # Country
            if region == "Central Africa":
                c_options = ["Cameroon", "Central African Republic", "Republic of Congo", "Democratic Republic of the Congo", "Equatorial Guinea", "Gabon"]
            else:
                c_options = [region]
            
            curr_cnt = shared_state.get("gi_country")
            c_idx = c_options.index(curr_cnt) if curr_cnt in c_options else 0
            country = st.selectbox("Country", c_options, index=c_idx, key="gi_country_select")
            shared_state.set("gi_country", country)
            
            st.divider()
            
            # Duration
            c_d1, c_d2 = st.columns(2)
            impl = c_d1.number_input("Implementation (yrs)", min_value=0, value=4, key="gi_impl_phase")
            cap = c_d2.number_input("Capitalization (yrs)", min_value=0, value=10, key="gi_cap_phase")
            st.info(f"Total Duration: {impl + cap} Years")

    # ==========================================
    # 2. ACTIVITIES REPORTED
    # ==========================================
    st.markdown("### 2. Activities Reported")
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

    # ==========================================
    # 3. PARAMETERS
    # ==========================================
    st.markdown("### 3. Parameters")
    with st.container(border=True):
        st.caption("Review default parameters below. Enter a value in 'Custom Override' only if specific local data is available.")

        # --- ROW 1: Environmental Selectors ---
        p1, p2, p3 = st.columns(3)
        with p1:
            st.selectbox("Climate Zone", CLIMATES, key="gi_climate")
        with p2:
            st.selectbox("Moisture Regime", MOISTURES, key="gi_moisture")
        with p3:
            soil_sel = st.selectbox("Soil Type", SOIL_TYPES, key="gi_soil")

        st.divider()

        # --- ROW 2: The "Grid" for Values ---
        # Columns: [ Parameter Name ] [ Unit ] [ Default Value ] [ Custom Override ]
        
        # Headers
        h1, h2, h3, h4 = st.columns([2, 1, 1.5, 2])
        h1.markdown("**Parameter**")
        h2.markdown("**Unit**")
        h3.markdown("**Default**")
        h4.markdown("**Custom Override**")
        
        st.markdown("---") # Thin line

        # ITEM 1: Soil Organic Carbon (SOC)
        r1_c1, r1_c2, r1_c3, r1_c4 = st.columns([2, 1, 1.5, 2])
        r1_c1.write("Soil Organic Carbon (SOC)")
        r1_c2.write("tC/ha")
        r1_c3.code("47.0") # Placeholder default
        r1_c4.number_input("SOC Override", min_value=0.0, key="gi_soc_override", label_visibility="collapsed")

        # ITEM 2: Discount Rate
        r2_c1, r2_c2, r2_c3, r2_c4 = st.columns([2, 1, 1.5, 2])
        r2_c1.write("Discount Rate")
        r2_c2.write("%")
        r2_c3.code("10%")
        r2_c4.number_input("Rate Override", min_value=0.0, key="gi_discount_override", label_visibility="collapsed")

        # ITEM 3: Soil Calculation Period
        r3_c1, r3_c2, r3_c3, r3_c4 = st.columns([2, 1, 1.5, 2])
        r3_c1.write("Soil Calculation Period")
        r3_c2.write("Years")
        r3_c3.code("20")
        soil_years = r3_c4.number_input("Period Override", min_value=1, step=1, value=20, key="soil_divisor", label_visibility="collapsed")