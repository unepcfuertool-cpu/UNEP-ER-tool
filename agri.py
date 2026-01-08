# agri.py
import streamlit as st
import pandas as pd
import shared_state
import parameters

def render_agri_module():
    st.header("3. Agriculture")
    
    # 1. Get Parameters
    params = parameters.get_agri_params(shared_state.get("gi_country"))
    crop_list = list(params["agb_bgb_soil"].keys()) if "agb_bgb_soil" in params else []
    
    # Management Options
    tillage_opts = ["Full tillage", "Reduced tillage", "No tillage"]
    input_opts = ["Low", "Medium", "High", "Without manure"]
    residue_opts = ["Burned", "Retained", "Exported"]

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs([
        "3.1 Deforestation-free outgrower", 
        "3.2 Agro-industrial expansion", 
        "3.3 Sustainable intensification"
    ])

    # --- HELPER: MASTER TABLE RENDERER ---
    def render_section(key_prefix):
        # Initialize Session State for the Main Input Table
        key_main = f"main_{key_prefix}"
        key_tier3 = f"tier3_{key_prefix}"

        # Define full column names for Table 1
        cols_main = [
            "Perennial cropping system deployed", 
            "Area (ha)", 
            "Management options - Tillage management", 
            "Management options - Input of organic materials", 
            "Residue management",
            "Emission factors (tC/ha/year) default - Above-ground", 
            "Emission factors (tC/ha/year) default - Below-ground", 
            "Emission factors (tC/ha/year) default - Soil carbon",
            "Removal factors default - Tillage", 
            "Removal factors default - Input", 
            "Removal factors default - Residue",
            "Total GHG emission reduced (tCO2e)"
        ]

        # Define full column names for Table 2
        cols_tier3 = [
            "Reference Crop (Read-only)",
            "Emission factors (tC/ha/year) Tier 3 - Above-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Below-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Soil carbon",
            "Removal factors Tier 3 - Tillage", 
            "Removal factors Tier 3 - Input", 
            "Removal factors Tier 3 - Residue"
        ]

        if key_main not in st.session_state:
            st.session_state[key_main] = pd.DataFrame(columns=cols_main)
        
        if key_tier3 not in st.session_state:
            st.session_state[key_tier3] = pd.DataFrame(columns=cols_tier3)

        # --- TABLE 1: ACTIVITY DATA ---
        st.markdown("**1. Activity Data & Defaults**")
        df_main = st.data_editor(
            st.session_state[key_main],
            key=f"editor_{key_main}",
            num_rows="dynamic",
            column_config={
                "Perennial cropping system deployed": st.column_config.SelectboxColumn("Perennial cropping system deployed", options=crop_list, width="medium", required=True),
                "Area (ha)": st.column_config.NumberColumn("Area (ha)", min_value=0.0, format="%.2f"),
                "Management options - Tillage management": st.column_config.SelectboxColumn("Management options - Tillage management", options=tillage_opts, required=True),
                "Management options - Input of organic materials": st.column_config.SelectboxColumn("Management options - Input of organic materials", options=input_opts, required=True),
                "Residue management": st.column_config.SelectboxColumn("Residue management", options=residue_opts, required=True),
                
                # Defaults (Read-Only)
                "Emission factors (tC/ha/year) default - Above-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Above-ground", disabled=True),
                "Emission factors (tC/ha/year) default - Below-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Below-ground", disabled=True),
                "Emission factors (tC/ha/year) default - Soil carbon": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Soil carbon", disabled=True),
                "Removal factors default - Tillage": st.column_config.NumberColumn("Removal factors default - Tillage", disabled=True),
                "Removal factors default - Input": st.column_config.NumberColumn("Removal factors default - Input", disabled=True),
                "Removal factors default - Residue": st.column_config.NumberColumn("Removal factors default - Residue", disabled=True),
                
                # Result
                "Total GHG emission reduced (tCO2e)": st.column_config.NumberColumn("Total GHG emission reduced (tCO2e)", format="%.2f", disabled=True)
            },
            use_container_width=True
        )

        # --- SYNC LOGIC: Update Tier 3 Table rows to match Main Table ---
        current_rows = len(df_main)
        old_tier3 = st.session_state[key_tier3]
        
        # If rows were added
        if current_rows > len(old_tier3):
            rows_to_add = current_rows - len(old_tier3)
            new_data = pd.DataFrame(
                [[None] * len(old_tier3.columns)] * rows_to_add, 
                columns=old_tier3.columns
            )
            old_tier3 = pd.concat([old_tier3, new_data], ignore_index=True)
        
        # If rows were deleted
        elif current_rows < len(old_tier3):
            old_tier3 = old_tier3.iloc[:current_rows]

        # Update the "Reference Crop" column so user knows which row is which
        old_tier3["Reference Crop (Read-only)"] = df_main["Perennial cropping system deployed"].values

        # --- TABLE 2: TIER 3 DATA ---
        st.markdown("**2. Tier 3 (Local) Data**")
        st.caption("Rows correspond to the **Activity Data** table above.")
        
        df_tier3 = st.data_editor(
            old_tier3,
            key=f"editor_{key_tier3}",
            num_rows="fixed", # Locked to match top table
            column_config={
                "Reference Crop (Read-only)": st.column_config.TextColumn("Reference Crop", disabled=True),
                "Emission factors (tC/ha/year) Tier 3 - Above-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Above-ground", min_value=0.0),
                "Emission factors (tC/ha/year) Tier 3 - Below-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Below-ground", min_value=0.0),
                "Emission factors (tC/ha/year) Tier 3 - Soil carbon": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Soil carbon", min_value=0.0),
                "Removal factors Tier 3 - Tillage": st.column_config.NumberColumn("Removal factors Tier 3 - Tillage", min_value=0.0),
                "Removal factors Tier 3 - Input": st.column_config.NumberColumn("Removal factors Tier 3 - Input", min_value=0.0),
                "Removal factors Tier 3 - Residue": st.column_config.NumberColumn("Removal factors Tier 3 - Residue", min_value=0.0),
            },
            use_container_width=True
        )

        # Save manually to state to persist updates
        st.session_state[key_main] = df_main
        st.session_state[key_tier3] = df_tier3
        
        return df_main, df_tier3


    # --- RENDER TABS ---
    with tab1:
        st.subheader("3.1 Deforestation-free outgrower")
        df_main_1, df_tier3_1 = render_section("3_1")

    with tab2:
        st.subheader("3.2 Agro-industrial expansion")
        df_main_2, df_tier3_2 = render_section("3_2")

    with tab3:
        st.subheader("3.3 Sustainable intensification")
        df_main_3, df_tier3_3 = render_section("3_3")

    st.divider()
    
    # --- CALCULATION LOGIC ---
    if st.button("Calculate Agriculture", type="primary"):
        
        # Removal Factor Defaults
        rf_tillage_map = {"Full tillage": 1.0, "Reduced tillage": 1.02, "No tillage": 1.10}
        rf_input_map = {"Low": 0.95, "Medium": 1.0, "High": 1.37, "Without manure": 1.0}
        rf_residue_map = {"Burned": 0.9, "Retained": 1.1, "Exported": 0.9}

        def calculate_tab(df_m, df_t):
            total_tab = 0.0
            
            # Iterate through Main table rows
            for index, row in df_m.iterrows():
                crop = row.get("Perennial cropping system deployed")
                area = float(row.get("Area (ha)") or 0)
                
                if crop and area > 0:
                    # 1. Get Defaults
                    defaults = params["agb_bgb_soil"].get(crop, (0.0, 0.0, 0.0))
                    
                    # Update Main Table Default Columns
                    df_m.at[index, "Emission factors (tC/ha/year) default - Above-ground"] = defaults[0]
                    df_m.at[index, "Emission factors (tC/ha/year) default - Below-ground"] = defaults[1]
                    df_m.at[index, "Emission factors (tC/ha/year) default - Soil carbon"] = defaults[2]
                    
                    tillage = row.get("Management options - Tillage management")
                    inp = row.get("Management options - Input of organic materials")
                    res = row.get("Residue management")
                    
                    def_rf_t = rf_tillage_map.get(tillage, 1.0)
                    def_rf_i = rf_input_map.get(inp, 1.0)
                    def_rf_r = rf_residue_map.get(res, 1.0)
                    
                    df_m.at[index, "Removal factors default - Tillage"] = def_rf_t
                    df_m.at[index, "Removal factors default - Input"] = def_rf_i
                    df_m.at[index, "Removal factors default - Residue"] = def_rf_r

                    # 2. Get Tier 3 Overrides (from df_t row with same index)
                    try:
                        row_t3 = df_t.iloc[index]
                        u_ef_agb = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Above-ground") or 0) or defaults[0]
                        u_ef_bgb = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Below-ground") or 0) or defaults[1]
                        u_ef_soil = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Soil carbon") or 0) or defaults[2]
                        
                        u_rf_t = float(row_t3.get("Removal factors Tier 3 - Tillage") or 0) or def_rf_t
                        u_rf_i = float(row_t3.get("Removal factors Tier 3 - Input") or 0) or def_rf_i
                        u_rf_r = float(row_t3.get("Removal factors Tier 3 - Residue") or 0) or def_rf_r
                    except IndexError:
                        # Fallback
                        u_ef_agb, u_ef_bgb, u_ef_soil = defaults
                        u_rf_t, u_rf_i, u_rf_r = def_rf_t, def_rf_i, def_rf_r

                    # 3. Calculate
                    soil_impact = u_ef_soil * u_rf_t * u_rf_i * u_rf_r
                    biomass_impact = u_ef_agb + u_ef_bgb
                    
                    total_c = area * (biomass_impact + soil_impact)
                    total_co2 = total_c * 3.664
                    
                    df_m.at[index, "Total GHG emission reduced (tCO2e)"] = total_co2
                    total_tab += total_co2

            return total_tab

        t1 = calculate_tab(df_main_1, df_tier3_1)
        t2 = calculate_tab(df_main_2, df_tier3_2)
        t3 = calculate_tab(df_main_3, df_tier3_3)
        
        grand_total = t1 + t2 + t3
        shared_state.set("agri_grand_total", grand_total)
        
        st.success(f"Calculated! Total Reductions: {grand_total:,.2f} tCO2e")
        st.rerun()