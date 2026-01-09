# results.py
import streamlit as st
import plotly.graph_objects as go
import shared_state
import datetime

def render_results_module():
    # --- 1. GATHER DATA ---
    # Global Totals
    energy = shared_state.get("energy_grand_total", 0.0) or 0.0
    arr = shared_state.get("arr_grand_total", 0.0) or 0.0
    forest = shared_state.get("forest_grand_total", 0.0) or 0.0
    
    # Agri Sub-totals
    agri_1 = shared_state.get("agri_total_1", 0.0) or 0.0 # Deforestation-free outgrower
    agri_2 = shared_state.get("agri_total_2", 0.0) or 0.0 # Agro-industrial expansion
    agri_3 = shared_state.get("agri_total_3", 0.0) or 0.0 # Sustainable intensification
    agri_total = agri_1 + agri_2 + agri_3
    
    # Fallback if totals exist but sub-totals don't
    if agri_total == 0 and shared_state.get("agri_grand_total", 0.0) > 0:
        agri_1 = shared_state.get("agri_grand_total", 0.0)
        agri_total = agri_1

    grand_total = energy + arr + agri_total + forest

    # Project Info
    impl_years = shared_state.get("gi_impl", 0) or 0
    cap_years = shared_state.get("gi_cap", 0) or 0
    total_duration = impl_years + cap_years

    info = {
        "Project": shared_state.get("gi_project_name", "-"),
        "Executing agency": shared_state.get("gi_executing_agency", "-"),
        "Funding agency": shared_state.get("gi_funding_agency", "-"),
        "Country": shared_state.get("gi_country", "-"),
        "Project cost": f"${shared_state.get('gi_project_cost', 0):,.0f}",
        "Duration": f"{total_duration} years"
    }

    # --- 2. PREPARE DATA ---
    # Sectors (X-Axis for both charts)
    sectors = ["Energy", "Afforestation & Reforestation", "Agriculture", "Forestry & Conservation"]
    
    # DATA FOR LEFT CHART (Totals Only)
    sector_values = [energy, arr, agri_total, forest]

    # DATA FOR RIGHT CHART (Stacked Activities)
    # We create a separate trace for each Activity. 
    # The list [v1, v2, v3, v4] corresponds to [Energy, ARR, Agri, Forest]
    
    # 1. Energy Activity (Only appears in Energy column)
    y_energy_act = [energy, 0, 0, 0]
    
    # 2. ARR Activity (Only appears in ARR column)
    y_arr_act = [0, arr, 0, 0]
    
    # 3. Forestry Activity (Only appears in Forest column)
    y_forest_act = [0, 0, 0, forest]
    
    # 4. Agri Activities (These 3 will STACK inside the Agriculture column)
    y_agri_outgrower = [0, 0, agri_1, 0]
    y_agri_industrial = [0, 0, agri_2, 0]
    y_agri_intensification = [0, 0, agri_3, 0]

    # --- 3. LAYOUT ---
    st.markdown("### Final Results Dashboard")
    
    col_left, col_mid, col_right = st.columns([1.5, 1, 1.5])

    # --- LEFT CHART: SECTOR OVERVIEW (Simple) ---
    with col_left:
        st.markdown("<h6 style='text-align:center; color:#555;'>Total Mitigation by Sector (tCO2e)</h6>", unsafe_allow_html=True)
        
        fig1 = go.Figure(go.Bar(
            x=sectors,
            y=sector_values,
            marker_color='#6c757d', # Uniform Grey
            text=[f"{v:,.0f}" if v > 0 else "" for v in sector_values],
            textposition='auto'
        ))
        
        fig1.update_layout(
            showlegend=False,
            height=500,
            margin=dict(t=20, b=50),
            paper_bgcolor='white', plot_bgcolor='white'
        )
        fig1.update_yaxes(showgrid=True, gridcolor='#eee', zeroline=True, zerolinecolor='black')
        st.plotly_chart(fig1, use_container_width=True)


    # --- MIDDLE: INFO & TOTAL ---
    with col_mid:
        # Info Table
        html = """<style>
            .it{width:100%; border-collapse:collapse; border:2px solid black; font-size:0.85em; font-family:sans-serif;} 
            .it td{border:1px solid black; padding:6px; text-align:center;} 
            .il{background:#f2f2f2; font-weight:bold; width:40%; text-align:left; padding-left:10px;} 
            .iv{color:#0056b3; font-style:italic;}
        </style><table class='it'>"""
        for k, v in info.items():
            html += f"<tr><td class='il'>{k}</td><td class='iv'>{v}</td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
        
        st.write("")
        
        # Green Total Box
        st.markdown(f"""
        <div style="border:2px solid black; text-align:center; margin-bottom:20px;">
            <div style="padding:10px; font-weight:bold; border-bottom:1px solid #ddd; background:white;">Total Emission Reduction</div>
            <div style="background:#ccf7d6; padding:30px 10px;">
                <div style="font-size:2.5em; font-weight:bold; color:#155724;">{grand_total:,.0f}</div>
                <div style="font-size:1.1em; color:#155724;">tCO₂ eq.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Agri Details Table
        if agri_total > 0:
            st.markdown("""<div style="font-size:0.85em; font-weight:bold; text-align:center; margin-bottom:5px;">Agriculture Details</div>""", unsafe_allow_html=True)
            agri_html = f"""
            <table class='it' style="border:1px solid #ccc;">
                <tr style="background:#E9C46A;"><td style="text-align:left;">Deforestation-free outgrower</td><td>{agri_1:,.0f}</td></tr>
                <tr style="background:#F4A261;"><td style="text-align:left;">Agro-industrial expansion</td><td>{agri_2:,.0f}</td></tr>
                <tr style="background:#E76F51;"><td style="text-align:left;">Sustainable intensification</td><td>{agri_3:,.0f}</td></tr>
            </table>
            """
            st.markdown(agri_html, unsafe_allow_html=True)


    # --- RIGHT CHART: DETAILED BREAKDOWN (Stacked) ---
    with col_right:
        st.markdown("<h6 style='text-align:center; color:#555;'>Mitigation by Activity (Stacked by Sector)</h6>", unsafe_allow_html=True)
        
        fig2 = go.Figure()
        
        # 1. Base Activities (Grey)
        fig2.add_trace(go.Bar(name='Energy', x=sectors, y=y_energy_act, marker_color='#B0B0B0'))
        fig2.add_trace(go.Bar(name='Afforestation & Reforestation', x=sectors, y=y_arr_act, marker_color='#B0B0B0'))
        fig2.add_trace(go.Bar(name='Forestry & Conservation', x=sectors, y=y_forest_act, marker_color='#B0B0B0'))
        
        # 2. Agriculture Activities (Colored & Stacked)
        # These 3 will stack on top of each other in the "Agriculture" column
        fig2.add_trace(go.Bar(name='Deforestation-free outgrower', x=sectors, y=y_agri_outgrower, marker_color='#E9C46A',
                             text=[f"{v:,.0f}" if v>0 else "" for v in y_agri_outgrower], textposition='inside'))
        
        fig2.add_trace(go.Bar(name='Agro-industrial expansion', x=sectors, y=y_agri_industrial, marker_color='#F4A261',
                             text=[f"{v:,.0f}" if v>0 else "" for v in y_agri_industrial], textposition='inside'))
        
        fig2.add_trace(go.Bar(name='Sustainable intensification', x=sectors, y=y_agri_intensification, marker_color='#E76F51',
                             text=[f"{v:,.0f}" if v>0 else "" for v in y_agri_intensification], textposition='inside'))

        fig2.update_layout(
            barmode='stack', # This forces the hierarchy
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            height=500,
            margin=dict(t=20, b=80),
            paper_bgcolor='white', plot_bgcolor='white'
        )
        fig2.update_yaxes(showgrid=True, gridcolor='#eee', zeroline=True, zerolinecolor='black')
        st.plotly_chart(fig2, use_container_width=True)