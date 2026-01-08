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
        # Unique keys for this section
        # "storage_" keys hold the actual dataframe data
        # "editor_" keys are for the streamlit widgets
        storage_key_main = f"storage_main_{key_prefix}"
        storage_key_tier3 = f"storage_tier3_{key_prefix}"
        widget_key_main = f"editor_main_{key_prefix}"
        widget_key_tier3 = f"editor_tier3_{key_prefix}"

        # Columns - Left Table
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

        # Columns - Right Table (Full Titles)
        cols_tier3 = [
            "Reference Crop (Read-only)",
            "Emission factors (tC/ha/year) Tier 3 - Above-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Below-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Soil carbon",
            "Removal factors Tier 3 - Tillage", 
            "Removal factors Tier 3 - Input", 
            "Removal factors Tier 3 - Residue"
        ]

        # --- 1. INITIALIZE STORAGE IF MISSING ---
        if storage_key_main not in st.session_state:
            st.session_state[storage_key_main] = pd.DataFrame(columns=cols_main)
        if storage_key_tier3 not in st.session_state:
            st.session_state[storage_key_tier3] = pd.DataFrame(columns=cols_tier3)

        # Layout
        col_left, col_right = st.columns([1.5, 1.2])

        # --- 2. RENDER LEFT TABLE (ACTIVITY DATA) ---
        with col_left:
            st.markdown("**1. Activity Data & Defaults**")
            
            # Load current data from storage
            current_main_df = st.session_state[storage_key_main]
            
            edited_main = st.data_editor(
                current_main_df,
                key=widget_key_main,
                num_rows="dynamic",
                column_config={
                    "Perennial cropping system deployed": st.column_config.SelectboxColumn("Perennial cropping system deployed", options=crop_list, width="medium", required=True),
                    "Area (ha)": st.column_config.NumberColumn("Area (ha)", min_value=0.0, format="%.2f", width="small"),
                    "Management options - Tillage management": st.column_config.SelectboxColumn("Management options - Tillage management", options=tillage_opts, width="medium", required=True),
                    "Management options - Input of organic materials": st.column_config.SelectboxColumn("Management options - Input of organic materials", options=input_opts, width="medium", required=True),
                    "Residue management": st.column_config.SelectboxColumn("Residue management", options=residue_opts, width="small", required=True),
                    # Read-only Defaults
                    "Emission factors (tC/ha/year) default - Above-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Above-ground", width="medium", disabled=True),
                    "Emission factors (tC/ha/year) default - Below-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Below-ground", width="medium", disabled=True),
                    "Emission factors (tC/ha/year) default - Soil carbon": st.column_config.NumberColumn("Emission factors (tC/ha/year) default - Soil carbon", width="medium", disabled=True),
                    "Removal factors default - Tillage": st.column_config.NumberColumn("Removal factors default - Tillage", width="small", disabled=True),
                    "Removal factors default - Input": st.column_config.NumberColumn("Removal factors default - Input", width="small", disabled=True),
                    "Removal factors default - Residue": st.column_config.NumberColumn("Removal factors default - Residue", width="small", disabled=True),
                    "Total GHG emission reduced (tCO2e)": st.column_config.NumberColumn("Total GHG emission reduced (tCO2e)", format="%.2f", width="medium", disabled=True)
                },
                use_container_width=True
            )
            # Update storage immediately with Left Table edits
            st.session_state[storage_key_main] = edited_main

        # --- 3. SYNC LOGIC (CRITICAL STEP) ---
        # We must align the Right Table (Tier 3) storage to match the Left Table's row count *before* rendering the Right Table.
        
        current_tier3_df = st.session_state[storage_key_tier3]
        rows_main = len(edited_main)
        rows_tier3 = len(current_tier3_df)

        if rows_main > rows_tier3:
            # Add missing rows
            rows_to_add = rows_main - rows_tier3
            # Create empty rows with 0.0 defaults for numeric cols
            new_data = {col: [0.0 if i > 0 else None for i in range(len(cols_tier3))] for col in cols_tier3}
            # Adjust first col (Reference Crop) to be None initially
            new_data["Reference Crop (Read-only)"] = [None] * (len(cols_tier3) - len(new_data)) # Fix key issue
            
            df_new = pd.DataFrame(new_data)
            # Ensure correct structure
            df_new = pd.DataFrame(
                [[None] + [0.0]*(len(cols_tier3)-1)] * rows_to_add, 
                columns=cols_tier3
            )
            current_tier3_df = pd.concat([current_tier3_df, df_new], ignore_index=True)
            
        elif rows_main < rows_tier3:
            # Remove extra rows
            current_tier3_df = current_tier3_df.iloc[:rows_main]

        # Sync Reference Crop Names
        if rows_main > 0:
            current_tier3_df["Reference Crop (Read-only)"] = edited_main["Perennial cropping system deployed"].values

        # --- 4. RENDER RIGHT TABLE (LOCAL DATA) ---
        with col_right:
            st.markdown("**2. Local Data**")
            
            edited_tier3 = st.data_editor(
                current_tier3_df,
                key=widget_key_tier3,
                num_rows="fixed", # Locked to follow Left Table
                column_config={
                    "Reference Crop (Read-only)": st.column_config.TextColumn("Reference Crop", disabled=True, width="medium"),
                    
                    # Full Titles
                    "Emission factors (tC/ha/year) Tier 3 - Above-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Above-ground", min_value=0.0, width="medium"),
                    "Emission factors (tC/ha/year) Tier 3 - Below-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Below-ground", min_value=0.0, width="medium"),
                    "Emission factors (tC/ha/year) Tier 3 - Soil carbon": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Soil carbon", min_value=0.0, width="medium"),
                    
                    "Removal factors Tier 3 - Tillage": st.column_config.NumberColumn("Removal factors Tier 3 - Tillage", min_value=0.0, width="medium"),
                    "Removal factors Tier 3 - Input": st.column_config.NumberColumn("Removal factors Tier 3 - Input", min_value=0.0, width="medium"),
                    "Removal factors Tier 3 - Residue": st.column_config.NumberColumn("Removal factors Tier 3 - Residue", min_value=0.0, width="medium"),
                },
                use_container_width=True
            )
            
            # Update storage with Right Table edits
            st.session_state[storage_key_tier3] = edited_tier3

        return edited_main, edited_tier3

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
        
        # Mappings
        rf_tillage_map = {"Full tillage": 1.0, "Reduced tillage": 1.02, "No tillage": 1.10}
        rf_input_map = {"Low C input": 0.95, "Medium C input": 1.0, "High C input, no manure": 1.37, "High C input, with manure": 1.37}
        rf_residue_map = {"Burned": 0.9, "Retained": 1.1, "Exported": 0.9}

        def calculate_tab(df_m, df_t):
            total_tab = 0.0
            
            # Iterate through synced dataframes
            for index, row in df_m.iterrows():
                crop = row.get("Perennial cropping system deployed")
                area = float(row.get("Area (ha)") or 0)
                
                if crop and area > 0:
                    # Defaults
                    defaults = params["agb_bgb_soil"].get(crop, (0.0, 0.0, 0.0))
                    
                    # Update Defaults in Main Table (Visual only, for next render)
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

                    # Local Overrides (Tier 3)
                    try:
                        row_t3 = df_t.iloc[index]
                        
                        u_ef_agb = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Above-ground") or 0) or defaults[0]
                        u_ef_bgb = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Below-ground") or 0) or defaults[1]
                        u_ef_soil = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Soil carbon") or 0) or defaults[2]
                        
                        u_rf_t = float(row_t3.get("Removal factors Tier 3 - Tillage") or 0) or def_rf_t
                        u_rf_i = float(row_t3.get("Removal factors Tier 3 - Input") or 0) or def_rf_i
                        u_rf_r = float(row_t3.get("Removal factors Tier 3 - Residue") or 0) or def_rf_r
                    except (IndexError, KeyError):
                        # Fallback if synchronization failed
                        u_ef_agb, u_ef_bgb, u_ef_soil = defaults
                        u_rf_t, u_rf_i, u_rf_r = def_rf_t, def_rf_i, def_rf_r

                    # Calculation
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