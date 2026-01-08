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
        # Keys
        key_main = f"main_{key_prefix}"
        key_tier3 = f"tier3_{key_prefix}"

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

        # Columns - Right Table
        cols_tier3 = [
            "Reference Crop (Read-only)",
            "Emission factors (tC/ha/year) Tier 3 - Above-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Below-ground", 
            "Emission factors (tC/ha/year) Tier 3 - Soil carbon",
            "Removal factors Tier 3 - Tillage", 
            "Removal factors Tier 3 - Input", 
            "Removal factors Tier 3 - Residue"
        ]

        # Initialize State
        if key_main not in st.session_state:
            st.session_state[key_main] = pd.DataFrame(columns=cols_main)
        if key_tier3 not in st.session_state:
            st.session_state[key_tier3] = pd.DataFrame(columns=cols_tier3)

        # Layout
        col_left, col_right = st.columns([1.5, 1.2]) # Adjusted ratio for better visibility

        # --- LEFT: ACTIVITY DATA ---
        with col_left:
            st.markdown("**1. Activity Data & Defaults**")
            edited_main = st.data_editor(
                st.session_state[key_main],
                key=f"editor_{key_main}",
                num_rows="dynamic",
                column_config={
                    "Perennial cropping system deployed": st.column_config.SelectboxColumn("Perennial cropping system deployed", options=crop_list, width="medium", required=True),
                    "Area (ha)": st.column_config.NumberColumn("Area (ha)", min_value=0.0, format="%.2f", width="small"),
                    "Management options - Tillage management": st.column_config.SelectboxColumn("Management options - Tillage management", options=tillage_opts, width="medium", required=True),
                    "Management options - Input of organic materials": st.column_config.SelectboxColumn("Management options - Input of organic materials", options=input_opts, width="medium", required=True),
                    "Residue management": st.column_config.SelectboxColumn("Residue management", options=residue_opts, width="small", required=True),
                    
                    # Read-only Defaults (Width adjusted to show text)
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
            st.session_state[key_main] = edited_main

        # --- SYNC LOGIC ---
        current_tier3 = st.session_state[key_tier3]
        rows_main = len(edited_main)
        rows_tier3 = len(current_tier3)

        # 1. Resize Tier 3 DataFrame to match Main
        if rows_main > rows_tier3:
            rows_to_add = rows_main - rows_tier3
            empty_data = {col: [None] * rows_to_add for col in cols_tier3}
            df_new_rows = pd.DataFrame(empty_data)
            current_tier3 = pd.concat([current_tier3, df_new_rows], ignore_index=True)
        elif rows_main < rows_tier3:
            current_tier3 = current_tier3.iloc[:rows_main]

        # 2. Update Reference Labels
        if rows_main > 0:
            current_tier3["Reference Crop (Read-only)"] = edited_main["Perennial cropping system deployed"].values
            numeric_cols = cols_tier3[1:]
            current_tier3[numeric_cols] = current_tier3[numeric_cols].fillna(0.0)

        st.session_state[key_tier3] = current_tier3

        # --- RIGHT: LOCAL DATA ---
        with col_right:
            st.markdown("**2. Local Data**")
            
            edited_tier3 = st.data_editor(
                st.session_state[key_tier3],
                key=f"editor_{key_tier3}",
                num_rows="fixed",
                column_config={
                    "Reference Crop (Read-only)": st.column_config.TextColumn("Reference Crop", disabled=True, width="medium"),
                    
                    # Adjusted widths to show full titles
                    "Emission factors (tC/ha/year) Tier 3 - Above-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Above-ground", min_value=0.0, width="medium"),
                    "Emission factors (tC/ha/year) Tier 3 - Below-ground": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Below-ground", min_value=0.0, width="medium"),
                    "Emission factors (tC/ha/year) Tier 3 - Soil carbon": st.column_config.NumberColumn("Emission factors (tC/ha/year) Tier 3 - Soil carbon", min_value=0.0, width="medium"),
                    
                    "Removal factors Tier 3 - Tillage": st.column_config.NumberColumn("Removal factors Tier 3 - Tillage", min_value=0.0, width="medium"),
                    "Removal factors Tier 3 - Input": st.column_config.NumberColumn("Removal factors Tier 3 - Input", min_value=0.0, width="medium"),
                    "Removal factors Tier 3 - Residue": st.column_config.NumberColumn("Removal factors Tier 3 - Residue", min_value=0.0, width="medium"),
                },
                use_container_width=True
            )
            st.session_state[key_tier3] = edited_tier3

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
            
            for index, row in df_m.iterrows():
                crop = row.get("Perennial cropping system deployed")
                area = float(row.get("Area (ha)") or 0)
                
                if crop and area > 0:
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