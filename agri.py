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

    # Helper to create the expanded table structure
    def make_table(key):
        if key not in st.session_state:
            st.session_state[key] = pd.DataFrame(columns=[
                # --- INPUTS ---
                "Perennial cropping system deployed", "Area (ha)", 
                "Mgmt: Tillage", "Mgmt: Inputs", "Residue management",
                
                # --- DEFAULTS (Read-Only) ---
                "EF: Above-ground", "EF: Below-ground", "EF: Soil Carbon",
                "RF: Tillage", "RF: Input", "RF: Residue",
                
                # --- LOCAL DATA (User Entry - Tier 3) ---
                "Local EF: AGB (Tier 3)", "Local EF: BGB (Tier 3)", "Local EF: Soil (Tier 3)",
                "Local RF: Tillage (Tier 3)", "Local RF: Input (Tier 3)", "Local RF: Residue (Tier 3)",
                
                # --- RESULT ---
                "Total GHG Reduced (tCO2e)"
            ])
            
        return st.data_editor(
            st.session_state[key],
            key=f"editor_{key}",
            num_rows="dynamic",
            column_config={
                # --- 1. Project Inputs ---
                "Perennial cropping system deployed": st.column_config.SelectboxColumn("1. Cropping System", options=crop_list, width="medium", required=True),
                "Area (ha)": st.column_config.NumberColumn("2. Area (ha)", min_value=0.0, format="%.2f"),
                "Mgmt: Tillage": st.column_config.SelectboxColumn("3a. Tillage", options=tillage_opts, required=True),
                "Mgmt: Inputs": st.column_config.SelectboxColumn("3b. Org. Inputs", options=input_opts, required=True),
                "Residue management": st.column_config.SelectboxColumn("4. Residue Mgmt", options=residue_opts, required=True),
                
                # --- 2. Defaults (Greyed out) ---
                "EF: Above-ground": st.column_config.NumberColumn("Def. EF AGB", disabled=True, help="Tier 1 Default"),
                "EF: Below-ground": st.column_config.NumberColumn("Def. EF BGB", disabled=True, help="Tier 1 Default"),
                "EF: Soil Carbon": st.column_config.NumberColumn("Def. EF Soil", disabled=True, help="Tier 1 Default"),
                "RF: Tillage": st.column_config.NumberColumn("Def. RF Tillage", disabled=True, help="Tier 1 Default"),
                "RF: Input": st.column_config.NumberColumn("Def. RF Input", disabled=True, help="Tier 1 Default"),
                "RF: Residue": st.column_config.NumberColumn("Def. RF Residue", disabled=True, help="Tier 1 Default"),
                
                # --- 3. Local Data (Tier 3) ---
                "Local EF: AGB (Tier 3)": st.column_config.NumberColumn("Local EF: AGB (Tier 3)", min_value=0.0, help="Enter Tier 3 Above-Ground Biomass factor"),
                "Local EF: BGB (Tier 3)": st.column_config.NumberColumn("Local EF: BGB (Tier 3)", min_value=0.0, help="Enter Tier 3 Below-Ground Biomass factor"),
                "Local EF: Soil (Tier 3)": st.column_config.NumberColumn("Local EF: Soil (Tier 3)", min_value=0.0, help="Enter Tier 3 Soil Carbon factor"),
                "Local RF: Tillage (Tier 3)": st.column_config.NumberColumn("Local RF: Tillage (Tier 3)", min_value=0.0, help="Enter Tier 3 Removal Factor for Tillage"),
                "Local RF: Input (Tier 3)": st.column_config.NumberColumn("Local RF: Input (Tier 3)", min_value=0.0, help="Enter Tier 3 Removal Factor for Inputs"),
                "Local RF: Residue (Tier 3)": st.column_config.NumberColumn("Local RF: Residue (Tier 3)", min_value=0.0, help="Enter Tier 3 Removal Factor for Residue"),
                
                # --- 4. Result ---
                "Total GHG Reduced (tCO2e)": st.column_config.NumberColumn("Total Reductions", format="%.2f", disabled=True)
            },
            use_container_width=True
        )

    # --- Render Tables ---
    with tab1:
        st.subheader("3.1 Deforestation-free outgrower")
        st.caption("Scroll right to enter **Tier 3** data if available.")
        df_3_1 = make_table("df_3_1")

    with tab2:
        st.subheader("3.2 Agro-industrial expansion")
        st.caption("Scroll right to enter **Tier 3** data if available.")
        df_3_2 = make_table("df_3_2")

    with tab3:
        st.subheader("3.3 Sustainable intensification")
        st.caption("Scroll right to enter **Tier 3** data if available.")
        df_3_3 = make_table("df_3_3")

    st.divider()
    
    # --- Calculation Logic ---
    if st.button("Calculate Agriculture", type="primary"):
        
        # 1. Defaults for Removal Factors (RF)
        rf_tillage_map = {"Full tillage": 1.0, "Reduced tillage": 1.02, "No tillage": 1.10}
        rf_input_map = {"Low": 0.95, "Medium": 1.0, "High": 1.37, "Without manure": 1.0}
        rf_residue_map = {"Burned": 0.9, "Retained": 1.1, "Exported": 0.9}

        def calculate_and_update(df_key):
            df = st.session_state[df_key]
            
            for index, row in df.iterrows():
                crop = row.get("Perennial cropping system deployed")
                area = float(row.get("Area (ha)") or 0)
                
                if crop and area > 0:
                    # --- A. Retrieve Standard Defaults ---
                    defaults = params["agb_bgb_soil"].get(crop, (0.0, 0.0, 0.0))
                    
                    # Fill "Default" columns for visibility
                    df.at[index, "EF: Above-ground"] = defaults[0]
                    df.at[index, "EF: Below-ground"] = defaults[1]
                    df.at[index, "EF: Soil Carbon"] = defaults[2]
                    
                    tillage = row.get("Mgmt: Tillage")
                    inp = row.get("Mgmt: Inputs")
                    res = row.get("Residue management")
                    
                    def_rf_t = rf_tillage_map.get(tillage, 1.0)
                    def_rf_i = rf_input_map.get(inp, 1.0)
                    def_rf_r = rf_residue_map.get(res, 1.0)
                    
                    df.at[index, "RF: Tillage"] = def_rf_t
                    df.at[index, "RF: Input"] = def_rf_i
                    df.at[index, "RF: Residue"] = def_rf_r

                    # --- B. Select Used Values (Tier 3 overrides Default) ---
                    # Logic: If Tier 3 cell > 0, use Tier 3. Else use Default.
                    
                    # Emission Factors
                    u_ef_agb = float(row.get("Local EF: AGB (Tier 3)") or 0) or defaults[0]
                    u_ef_bgb = float(row.get("Local EF: BGB (Tier 3)") or 0) or defaults[1]
                    u_ef_soil = float(row.get("Local EF: Soil (Tier 3)") or 0) or defaults[2]
                    
                    # Removal Factors
                    u_rf_t = float(row.get("Local RF: Tillage (Tier 3)") or 0) or def_rf_t
                    u_rf_i = float(row.get("Local RF: Input (Tier 3)") or 0) or def_rf_i
                    u_rf_r = float(row.get("Local RF: Residue (Tier 3)") or 0) or def_rf_r
                    
                    # --- C. Calculate Total ---
                    # Formula: Area * [ (AGB + BGB) + (Soil * RF_T * RF_I * RF_R) ] * 3.664
                    
                    soil_impact = u_ef_soil * u_rf_t * u_rf_i * u_rf_r
                    biomass_impact = u_ef_agb + u_ef_bgb
                    
                    total_c = area * (biomass_impact + soil_impact)
                    total_co2 = total_c * 3.664
                    
                    df.at[index, "Total GHG Reduced (tCO2e)"] = total_co2

            st.session_state[df_key] = df
            return df["Total GHG Reduced (tCO2e)"].sum()

        t1 = calculate_and_update("df_3_1")
        t2 = calculate_and_update("df_3_2")
        t3 = calculate_and_update("df_3_3")
        
        grand_total = t1 + t2 + t3
        shared_state.set("agri_grand_total", grand_total)
        
        st.success(f"Calculated! Total Reductions: {grand_total:,.2f} tCO2e")
        st.rerun()