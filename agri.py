# agri.py
import streamlit as st
import pandas as pd
import shared_state
import parameters

def render_agri_module():
    st.header("3. Agriculture Emissions")
    
    # Load parameters
    params = parameters.get_agri_params(shared_state.get("gi_country"))
    crop_list = list(params["agb_bgb_soil"].keys())
    
    st.info("ℹ️ Enter data below. Defaults (AGB, BGB) are pulled from parameters.")

    tab1, tab2, tab3 = st.tabs(["3.1 Outgrower", "3.2 Agro-industrial", "3.3 Intensification"])

    # Helper to create tables
    def make_table(key):
        if key not in st.session_state:
            st.session_state[key] = pd.DataFrame(columns=[
                "Crop System", "Area (ha)", "Tillage", "Inputs", "Residue", 
                "Local AGB", "Local Soil"
            ])
        return st.data_editor(
            st.session_state[key],
            key=f"editor_{key}",
            num_rows="dynamic",
            column_config={
                "Crop System": st.column_config.SelectboxColumn("Crop", options=crop_list, required=True),
                "Area (ha)": st.column_config.NumberColumn(min_value=0.0),
                "Tillage": st.column_config.SelectboxColumn("Tillage", options=["Full tillage", "Reduced tillage", "No tillage"], required=True),
                "Inputs": st.column_config.SelectboxColumn("Inputs", options=["Low C input", "Medium C input", "High C input"], required=True),
                "Residue": st.column_config.SelectboxColumn("Residue", options=["Burned", "Retained", "Exported"], required=True),
                "Local AGB": st.column_config.NumberColumn("Local AGB (Override)", help="Leave 0 for Default"),
                "Local Soil": st.column_config.NumberColumn("Local Soil (Override)", help="Leave 0 for Default"),
            },
            use_container_width=True
        )

    with tab1: df_3_1 = make_table("df_3_1")
    with tab2: df_3_2 = make_table("df_3_2")
    with tab3: df_3_3 = make_table("df_3_3")

    st.divider()
    
    if st.button("Calculate Agriculture", type="primary"):
        total = 0.0
        results = []
        soil_years = shared_state.get("soil_divisor") or 20

        def calc_df(df, section):
            sub_total = 0
            for _, row in df.iterrows():
                crop = row.get("Crop System")
                area = float(row.get("Area (ha)") or 0)
                if crop and area > 0:
                    # Get Defaults
                    defs = params["agb_bgb_soil"].get(crop, (0,0,0)) # (AGB, BGB, Soil)
                    
                    # Logic: Use Local if > 0, else Default
                    agb = float(row.get("Local AGB") or 0)
                    if agb == 0: agb = defs[0]
                    
                    bgb = defs[1] # Using default BGB for simplicity here
                    
                    soil = float(row.get("Local Soil") or 0)
                    if soil == 0: soil = defs[2]

                    # Simplified Math
                    biomass_co2 = (agb + bgb) * 3.664
                    soil_co2 = (soil / soil_years) * 1.0 # (Simplified factors)
                    
                    reduction = (biomass_co2 + soil_co2) * area
                    sub_total += reduction
                    results.append({
                        "Section": section, "Crop": crop, 
                        "Area": area, "Ref AGB": agb, "Ref Soil": soil,
                        "Emission Reduction": reduction
                    })
            return sub_total

        t1 = calc_df(df_3_1, "3.1 Outgrower")
        t2 = calc_df(df_3_2, "3.2 Agro-ind")
        t3 = calc_df(df_3_3, "3.3 Intensif")
        
        grand = t1 + t2 + t3
        shared_state.set("agri_grand_total", grand)
        shared_state.set("agri_results_table", results)
        st.success(f"Calculated! Total: {grand:,.2f} tCO2e")