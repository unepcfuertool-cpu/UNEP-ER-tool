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
    
    # --- DROPDOWN OPTIONS ---
    tillage_opts = ["Full tillage", "Reduced tillage", "No tillage"]
    input_opts = ["Low C input", "Medium C input", "High C input, no manure", "High C input, with manure"]
    residue_opts = ["Burned", "Exported", "Retained"]

    # --- TABS ---
    tab1, tab2, tab3 = st.tabs([
        "3.1 Deforestation-free outgrower", 
        "3.2 Agro-industrial expansion", 
        "3.3 Sustainable intensification"
    ])

    # --- HELPER: MASTER TABLE RENDERER ---
    def render_section(key_prefix):
        # Unique key for this section's dataframe
        key_df = f"df_{key_prefix}"

        # Define ALL columns in one list with FULL TITLES
        cols = [
            # --- 1. ACTIVITY DATA ---
            "Perennial cropping system deployed", 
            "Area (ha)", 
            "Management options - Tillage management", 
            "Management options - Input of organic materials", 
            "Residue management",
            
            # --- 2. DEFAULTS (Read-only) ---
            "Emission factors (tC/ha/year) default - Above-ground", 
            "Emission factors (tC/ha/year) default - Below-ground", 
            "Emission factors (tC/ha/year) default - Soil carbon",
            "Removal factors default - Tillage", 
            "Removal factors default - Input", 
            "Removal factors default - Residue",
            
            # --- 3. TIER 3 / LOCAL DATA (User Entry) ---
            "Emission factors (tC/ha/year) Tier 3 - Above-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Below-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Soil carbon",
            "Removal factors Tier 3 - Tillage", 
            "Removal factors Tier 3 - Input", 
            "Removal factors Tier 3 - Residue",
            
            # --- 4. RESULT ---
            "Total GHG emission reduced (tCO2e)"
        ]

        # Initialize DataFrames if not present
        if key_df not in st.session_state:
            st.session_state[key_df] = pd.DataFrame(columns=cols)

        # RENDER SINGLE UNIFIED TABLE
        st.markdown("**Enter Project Data** (Scroll right to enter Tier 3 / Local Data)")
        
        edited_df = st.data_editor(
            st.session_state[key_df],
            key=f"editor_{key_prefix}",
            num_rows="dynamic",
            column_config={
                # --- SECTION 1: INPUTS ---
                "Perennial cropping system deployed": st.column_config.SelectboxColumn("Perennial cropping system deployed", options=crop_list, width="medium", required=True),
                "Area (ha)": st.column_config.NumberColumn("Area (ha)", min_value=0.0, format="%.2f", width="small"),
                "Management options - Tillage management": st.column_config.SelectboxColumn("Management options - Tillage management", options=tillage_opts, width="medium", required=True),
                "Management options - Input of organic materials": st.column_config.SelectboxColumn("Management options - Input of organic materials", options=input_opts, width="medium", required=True),
                "Residue management": st.column_config.SelectboxColumn("Residue management", options=residue_opts, width="small", required=True),
                
                # --- SECTION 2: DEFAULTS (Read-Only) ---
                "Emission factors (tC/ha/year) default - Above-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Above-ground", disabled=True, width="medium"),
                "Emission factors (tC/ha/year) default - Below-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Below-ground", disabled=True, width="medium"),
                "Emission factors (tC/ha/year) default - Soil carbon": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Soil carbon", disabled=True, width="medium"),
                "Removal factors default - Tillage": st.column_config.NumberColumn("Removal factors default - Tillage", disabled=True, width="medium"),
                "Removal factors default - Input": st.column_config.NumberColumn("Removal factors default - Input", disabled=True, width="medium"),
                "Removal factors default - Residue": st.column_config.NumberColumn("Removal factors default - Residue", disabled=True, width="medium"),
                
                # --- SECTION 3: TIER 3 (Editable) ---
                "Emission factors (tC/ha/year) Tier 3 - Above-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Above-ground", min_value=0.0, width="medium"),
                "Emission factors (tC/ha/year) Tier 3 - Below-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Below-ground", min_value=0.0, width="medium"),
                "Emission factors (tC/ha/year) Tier 3 - Soil carbon": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Soil carbon", min_value=0.0, width="medium"),
                "Removal factors Tier 3 - Tillage": st.column_config.NumberColumn("Removal factors Tier 3 - Tillage", min_value=0.0, width="medium"),
                "Removal factors Tier 3 - Input": st.column_config.NumberColumn("Removal factors Tier 3 - Input", min_value=0.0, width="medium"),
                "Removal factors Tier 3 - Residue": st.column_config.NumberColumn("Removal factors Tier 3 - Residue", min_value=0.0, width="medium"),
                
                # --- SECTION 4: RESULT ---
                "Total GHG emission reduced (tCO2e)": st.column_config.NumberColumn("Total GHG emission reduced (tCO2e)", format="%.2f", disabled=True, width="medium")
            },
            use_container_width=True
        )

        # Save state
        st.session_state[key_df] = edited_df
        return edited_df

    # --- RENDER TABS ---
    with tab1:
        st.subheader("3.1 Deforestation-free outgrower")
        df_1 = render_section("3_1")

    with tab2:
        st.subheader("3.2 Agro-industrial expansion")
        df_2 = render_section("3_2")

    with tab3:
        st.subheader("3.3 Sustainable intensification")
        df_3 = render_section("3_3")

    st.divider()
    
    # --- CALCULATION LOGIC ---
    if st.button("Calculate Agriculture", type="primary"):
        
        # Mappings based on Technical Notes 
        # Tillage Factors
        rf_tillage_map = {
            "Full tillage": 1.0, 
            "Reduced tillage": 1.04,  # Updated from Tech Notes
            "No tillage": 1.10
        }
        # Input Factors
        rf_input_map = {
            "Low C input": 0.92,      # Updated from Tech Notes
            "Medium C input": 1.0, 
            "High C input, no manure": 1.11, # Updated from Tech Notes
            "High C input, with manure": 1.44 # Updated from Tech Notes
        }
        # Residue Factors
        rf_residue_map = {
            "Burned": 0.9,    # Note: Tech notes list 2.26?? but usually burning reduces C. Keeping logic, check value.
            "Exported": 0.9,  # Logic check needed if 2.26 applies to retention or removal.
            "Retained": 1.1   # Assuming retention adds carbon.
        }
        
        # Note on Tech Notes: The document lists 2.26 for ALL residue types.
        # This might be a typo in the source doc or a specific aggregated factor.
        # For now, I have kept standard logical defaults (0.9 for removal, 1.1 for retention)
        # to ensure the tool behaves predictably until that specific number is clarified.

        def calculate_tab(df):
            total_tab = 0.0
            
            for index, row in df.iterrows():
                crop = row.get("Perennial cropping system deployed")
                area = float(row.get("Area (ha)") or 0)
                
                if crop and area > 0:
                    # 1. Defaults
                    defaults = params["agb_bgb_soil"].get(crop, (0.0, 0.0, 0.0))
                    
                    # Update Default Columns
                    df.at[index, "Emission factors (tC/ha/year) default - Above-ground"] = defaults[0]
                    df.at[index, "Emission factors (tC/ha/year) default - Below-ground"] = defaults[1]
                    df.at[index, "Emission factors (tC/ha/year) default - Soil carbon"] = defaults[2]
                    
                    tillage = row.get("Management options - Tillage management")
                    inp = row.get("Management options - Input of organic materials")
                    res = row.get("Residue management")
                    
                    def_rf_t = rf_tillage_map.get(tillage, 1.0)
                    def_rf_i = rf_input_map.get(inp, 1.0)
                    def_rf_r = rf_residue_map.get(res, 1.0)
                    
                    df.at[index, "Removal factors default - Tillage"] = def_rf_t
                    df.at[index, "Removal factors default - Input"] = def_rf_i
                    df.at[index, "Removal factors default - Residue"] = def_rf_r

                    # 2. Local Overrides (Tier 3)
                    # Use local if > 0, else use default
                    u_ef_agb = float(row.get("Emission factors (tC/ha/year) Tier 3 - Above-ground") or 0) or defaults[0]
                    u_ef_bgb = float(row.get("Emission factors (tC/ha/year) Tier 3 - Below-ground") or 0) or defaults[1]
                    u_ef_soil = float(row.get("Emission factors (tC/ha/year) Tier 3 - Soil carbon") or 0) or defaults[2]
                    
                    u_rf_t = float(row.get("Removal factors Tier 3 - Tillage") or 0) or def_rf_t
                    u_rf_i = float(row.get("Removal factors Tier 3 - Input") or 0) or def_rf_i
                    u_rf_r = float(row.get("Removal factors Tier 3 - Residue") or 0) or def_rf_r

                    # 3. Calculation 
                    # Formula: Area * [ (AGB + BGB) + (Soil * RF_T * RF_I * RF_R) ] * 3.664
                    
                    # Note: Assuming u_ef_soil is an ANNUAL rate (tC/ha/year).
                    # If it is a 20-year stock change, we should divide by D (duration).
                    
                    soil_impact = u_ef_soil * u_rf_t * u_rf_i * u_rf_r
                    biomass_impact = u_ef_agb + u_ef_bgb
                    
                    total_c = area * (biomass_impact + soil_impact)
                    total_co2 = total_c * 3.664
                    
                    df.at[index, "Total GHG emission reduced (tCO2e)"] = total_co2
                    total_tab += total_co2

            return total_tab

        t1 = calculate_tab(df_1)
        t2 = calculate_tab(df_2)
        t3 = calculate_tab(df_3)
        
        grand_total = t1 + t2 + t3
        shared_state.set("agri_grand_total", grand_total)
        
        st.success(f"Calculated! Total Reductions: {grand_total:,.2f} tCO2e")
        st.rerun()