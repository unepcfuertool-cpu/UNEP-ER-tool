# agri.py
import streamlit as st
import pandas as pd
import shared_state
import parameters

def render_agri_module():
    st.header("3. Agriculture")
    params = parameters.get_agri_params(shared_state.get("gi_country"))
    crop_list = list(params["agb_bgb_soil"].keys())
    
    # Dropdowns
    tillage_opts = ["Full tillage", "Reduced tillage", "No tillage"]
    input_opts = ["Low C input", "Medium C input", "High C input, no manure", "High C input, with manure"]
    residue_opts = ["Burned", "Exported", "Retained"]

    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "3.1 Deforestation-free outgrower", 
        "3.2 Agro-industrial expansion", 
        "3.3 Sustainable intensification"
    ])

    # --- RENDERER ---
    def render_section(key_prefix):
        key_df = f"df_{key_prefix}"
        
        # CHANGED: "Tier 3" replaced with "Local" in column names
        cols = [
            "Perennial cropping system deployed", "Area (ha)", 
            "Management options - Tillage management", "Management options - Input of organic materials", "Residue management",
            "Emission factors (tC/ha/year) default - Above-ground", "Emission factors (tC/ha/year) default - Below-ground", "Emission factors (tC/ha/year) default - Soil carbon",
            "Removal factors default - Tillage", "Removal factors default - Input", "Removal factors default - Residue",
            "Emission factors (tC/ha/year) Local - Above-ground", "Emission factors (tC/ha/year) Local - Below-ground", "Emission factors (tC/ha/year) Local - Soil carbon",
            "Removal factors Local - Tillage", "Removal factors Local - Input", "Removal factors Local - Residue",
            "Total GHG emission reduced (tCO2e)"
        ]
        
        if key_df not in st.session_state:
            st.session_state[key_df] = pd.DataFrame(columns=cols)

        # CHANGED: Updated Instruction Text
        st.markdown("**Enter Project Data** (Scroll right for Local Data)")
        
        edited_df = st.data_editor(
            st.session_state[key_df],
            key=f"editor_{key_prefix}",
            num_rows="dynamic",
            column_config={
                "Perennial cropping system deployed": st.column_config.SelectboxColumn("1. Cropping System", options=crop_list, width="medium", required=True),
                "Area (ha)": st.column_config.NumberColumn("2. Area (ha)", min_value=0.0, format="%.2f", width="small"),
                "Management options - Tillage management": st.column_config.SelectboxColumn("3. Tillage", options=tillage_opts, width="medium", required=True),
                "Management options - Input of organic materials": st.column_config.SelectboxColumn("4. Inputs", options=input_opts, width="medium", required=True),
                "Residue management": st.column_config.SelectboxColumn("5. Residue", options=residue_opts, width="small", required=True),
                
                # Defaults (Gray)
                "Emission factors (tC/ha/year) default - Above-ground": st.column_config.NumberColumn("Def. EF AGB", disabled=True),
                "Emission factors (tC/ha/year) default - Below-ground": st.column_config.NumberColumn("Def. EF BGB", disabled=True),
                "Emission factors (tC/ha/year) default - Soil carbon": st.column_config.NumberColumn("Def. EF Soil", disabled=True),
                "Removal factors default - Tillage": st.column_config.NumberColumn("Def. RF Tillage", disabled=True),
                "Removal factors default - Input": st.column_config.NumberColumn("Def. RF Input", disabled=True),
                "Removal factors default - Residue": st.column_config.NumberColumn("Def. RF Residue", disabled=True),
                
                # Local Data (Editable) - CHANGED Labels
                "Emission factors (tC/ha/year) Local - Above-ground": st.column_config.NumberColumn("Local EF AGB", min_value=0.0),
                "Emission factors (tC/ha/year) Local - Below-ground": st.column_config.NumberColumn("Local EF BGB", min_value=0.0),
                "Emission factors (tC/ha/year) Local - Soil carbon": st.column_config.NumberColumn("Local EF Soil", min_value=0.0),
                "Removal factors Local - Tillage": st.column_config.NumberColumn("Local RF Tillage", min_value=0.0),
                "Removal factors Local - Input": st.column_config.NumberColumn("Local RF Input", min_value=0.0),
                "Removal factors Local - Residue": st.column_config.NumberColumn("Local RF Residue", min_value=0.0),
                
                # Result
                "Total GHG emission reduced (tCO2e)": st.column_config.NumberColumn("Total Reduced", format="%.2f", disabled=True)
            },
            use_container_width=True
        )
        st.session_state[key_df] = edited_df
        return edited_df

    # Render Sections
    with tab1: df_1 = render_section("3_1")
    with tab2: df_2 = render_section("3_2")
    with tab3: df_3 = render_section("3_3")

    st.divider()
    
    # --- CALCULATION ---
    if st.button("Calculate Agriculture", type="primary"):
        # Maps
        rf_tillage = {"Full tillage": 1.0, "Reduced tillage": 1.04, "No tillage": 1.10}
        rf_input = {"Low C input": 0.92, "Medium C input": 1.0, "High C input, no manure": 1.11, "High C input, with manure": 1.44}
        rf_residue = {"Burned": 0.9, "Exported": 0.9, "Retained": 1.1} 

        def calc(df):
            total = 0.0
            for idx, row in df.iterrows():
                crop = row.get("Perennial cropping system deployed")
                area = float(row.get("Area (ha)") or 0)
                if crop and area > 0:
                    defaults = params["agb_bgb_soil"].get(crop, (0.0, 0.0, 0.0))
                    
                    # Update Default Display
                    df.at[idx, "Emission factors (tC/ha/year) default - Above-ground"] = defaults[0]
                    df.at[idx, "Emission factors (tC/ha/year) default - Below-ground"] = defaults[1]
                    df.at[idx, "Emission factors (tC/ha/year) default - Soil carbon"] = defaults[2]
                    
                    t_val = rf_tillage.get(row.get("Management options - Tillage management"), 1.0)
                    i_val = rf_input.get(row.get("Management options - Input of organic materials"), 1.0)
                    r_val = rf_residue.get(row.get("Residue management"), 1.0)
                    
                    df.at[idx, "Removal factors default - Tillage"] = t_val
                    df.at[idx, "Removal factors default - Input"] = i_val
                    df.at[idx, "Removal factors default - Residue"] = r_val

                    # Use Local if entered, else Default (CHANGED KEYS)
                    ef_agb = float(row.get("Emission factors (tC/ha/year) Local - Above-ground") or 0) or defaults[0]
                    ef_bgb = float(row.get("Emission factors (tC/ha/year) Local - Below-ground") or 0) or defaults[1]
                    ef_soil = float(row.get("Emission factors (tC/ha/year) Local - Soil carbon") or 0) or defaults[2]
                    
                    rf_t = float(row.get("Removal factors Local - Tillage") or 0) or t_val
                    rf_i = float(row.get("Removal factors Local - Input") or 0) or i_val
                    rf_r = float(row.get("Removal factors Local - Residue") or 0) or r_val

                    # Math
                    soil_imp = ef_soil * rf_t * rf_i * rf_r
                    total_c = area * (ef_agb + ef_bgb + soil_imp)
                    res = total_c * 3.664
                    df.at[idx, "Total GHG emission reduced (tCO2e)"] = res
                    total += res
            return total

        # Calculate & Save
        total_1 = calc(df_1)
        total_2 = calc(df_2)
        total_3 = calc(df_3)
        grand_total = total_1 + total_2 + total_3
        
        shared_state.set("agri_grand_total", grand_total)
        shared_state.set("agri_total_1", total_1)
        shared_state.set("agri_total_2", total_2)
        shared_state.set("agri_total_3", total_3)
        
        st.success(f"Calculated! Total: {grand_total:,.2f} tCO2e")
        st.rerun()