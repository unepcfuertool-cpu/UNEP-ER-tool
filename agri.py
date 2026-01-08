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
        # Keys for session state
        key_main = f"main_{key_prefix}"
        key_tier3 = f"tier3_{key_prefix}"

        # Columns for LEFT table (Activity Data)
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

        # Columns for RIGHT table (Local Data)
        cols_tier3 = [
            "Reference Crop (Read-only)",
            "Emission factors (tC/ha/year) Tier 3 - Above-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Below-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Soil carbon",
            "Removal factors Tier 3 - Tillage", 
            "Removal factors Tier 3 - Input", 
            "Removal factors Tier 3 - Residue"
        ]

        # Initialize DataFrames if not present
        if key_main not in st.session_state:
            st.session_state[key_main] = pd.DataFrame(columns=cols_main)
        if key_tier3 not in st.session_state:
            st.session_state[key_tier3] = pd.DataFrame(columns=cols_tier3)

        # --- LAYOUT: TWO COLUMNS SIDE-BY-SIDE ---
        col_left, col_right = st.columns([1.3, 1])

        # --- LEFT: ACTIVITY DATA ---
        with col_left:
            st.markdown("**1. Activity Data & Defaults**")
            
            # Render Left Table
            edited_main = st.data_editor(
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
                    "Emission factors (tC/ha/year) default - Above-ground": st.column_config.NumberColumn("EF (Def) - AGB", disabled=True),
                    "Emission factors (tC/ha/year) default - Below-ground": st.column_config.NumberColumn("EF (Def) - BGB", disabled=True),
                    "Emission factors (tC/ha/year) default - Soil carbon": st.column_config.NumberColumn("EF (Def) - Soil", disabled=True),
                    "Removal factors default - Tillage": st.column_config.NumberColumn("RF (Def) - Tillage", disabled=True),
                    "Removal factors default - Input": st.column_config.NumberColumn("RF (Def) - Input", disabled=True),
                    "Removal factors default - Residue": st.column_config.NumberColumn("RF (Def) - Residue", disabled=True),
                    # Result
                    "Total GHG emission reduced (tCO2e)": st.column_config.NumberColumn("Total GHG reduced (tCO2e)", format="%.2f", disabled=True)
                },
                use_container_width=True
            )
            
            # Save Left Table Changes immediately
            st.session_state[key_main] = edited_main

        # --- SYNC LOGIC ---
        # 1. Get current Tier 3 data
        df_tier3 = st.session_state[key_tier3]
        
        # 2. Check row counts
        main_len = len(edited_main)
        tier3_len = len(df_tier3)
        
        # 3. Adjust Tier 3 Rows to match Main
        if main_len > tier3_len:
            # Add rows
            rows_to_add = main_len - tier3_len
            new_data = pd.DataFrame([[None] * len(cols_tier3)] * rows_to_add, columns=cols_tier3)
            # Use pd.concat properly
            df_tier3 = pd.concat([df_tier3, new_data], ignore_index=True)
            
        elif main_len < tier3_len:
            # Delete rows
            df_tier3 = df_tier3.iloc[:main_len]

        # 4. Sync Reference Crop Label
        if main_len > 0:
            df_tier3["Reference Crop (Read-only)"] = edited_main["Perennial cropping system deployed"].values
        else:
            df_tier3 = pd.DataFrame(columns=cols_tier3) # Reset if empty

        # 5. Save synced state BEFORE rendering the right table
        st.session_state[key_tier3] = df_tier3

        # --- RIGHT: LOCAL DATA ---
        with col_right:
            st.markdown("**2. Local Data**")
            
            # Render Right Table (Locked rows, enabled cells)
            edited_tier3 = st.data_editor(
                st.session_state[key_tier3],
                key=f"editor_{key_tier3}",
                num_rows="fixed", 
                column_config={
                    "Reference Crop (Read-only)": st.column_config.TextColumn("Ref Crop", disabled=True, width="small"),
                    
                    # User Editable Columns
                    "Emission factors (tC/ha/year) Tier 3 - Above-ground": st.column_config.NumberColumn("EF (T3) - AGB", min_value=0.0),
                    "Emission factors (tC/ha/year) Tier 3 - Below-ground": st.column_config.NumberColumn("EF (T3) - BGB", min_value=0.0),
                    "Emission factors (tC/ha/year) Tier 3 - Soil carbon": st.column_config.NumberColumn("EF (T3) - Soil", min_value=0.0),
                    
                    "Removal factors Tier 3 - Tillage": st.column_config.NumberColumn("RF (T3) - Tillage", min_value=0.0),
                    "Removal factors Tier 3 - Input": st.column_config.NumberColumn("RF (T3) - Input", min_value=0.0),
                    "Removal factors Tier 3 - Residue": st.column_config.NumberColumn("RF (T3) - Residue", min_value=0.0),
                },
                use_container_width=True
            )
            
            # Save Right Table Changes
            st.session_state[key_tier3] = edited_tier3

        return st.session_state[key_main], st.session_state[key_tier3]


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
        rf_input_map = {"Low C input": 0.95, "Medium C input": 1.0, "High C input, no manure": 1.37, "High C input, with manure": 1.37}
        rf_residue_map = {"Burned": 0.9, "Retained": 1.1, "Exported": 0.9}

        def calculate_tab(df_m, df_t):
            total_tab = 0.0
            
            # Iterate through rows
            for index, row in df_m.iterrows():
                crop = row.get("Perennial cropping system deployed")
                area = float(row.get("Area (ha)") or 0)
                
                if crop and area > 0:
                    # A. Defaults
                    defaults = params["agb_bgb_soil"].get(crop, (0.0, 0.0, 0.0))
                    
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

                    # B. Tier 3 Overrides
                    try:
                        row_t3 = df_t.iloc[index]
                        u_ef_agb = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Above-ground") or 0) or defaults[0]
                        u_ef_bgb = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Below-ground") or 0) or defaults[1]
                        u_ef_soil = float(row_t3.get("Emission factors (tC/ha/year) Tier 3 - Soil carbon") or 0) or defaults[2]
                        
                        u_rf_t = float(row_t3.get("Removal factors Tier 3 - Tillage") or 0) or def_rf_t
                        u_rf_i = float(row_t3.get("Removal factors Tier 3 - Input") or 0) or def_rf_i
                        u_rf_r = float(row_t3.get("Removal factors Tier 3 - Residue") or 0) or def_rf_r
                    except IndexError:
                        u_ef_agb, u_ef_bgb, u_ef_soil = defaults
                        u_rf_t, u_rf_i, u_rf_r = def_rf_t, def_rf_i, def_rf_r

                    # C. Calculate Total
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