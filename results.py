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
    
    # Agri Sub-totals (Using exact full names for variables helps clarity, but keys must match agri.py)
    agri_1 = shared_state.get("agri_total_1", 0.0) or 0.0 # Deforestation-free outgrower
    agri_2 = shared_state.get("agri_total_2", 0.0) or 0.0 # Agro-industrial expansion
    agri_3 = shared_state.get("agri_total_3", 0.0) or 0.0 # Sustainable intensification
    agri_total = agri_1 + agri_2 + agri_3
    
    # Fallback Logic: If total exists but sub-totals don't, assign to first category
    if agri_total == 0 and shared_state.get("agri_grand_total", 0.0) > 0:
        agri_1 = shared_state.get("agri_grand_total", 0.0)
        agri_total = agri_1

    grand_total = energy + arr + agri_total + forest

    # --- 2. PROJECT INFO (Fixed Linking) ---
    # Calculating duration based on Implementation + Capitalization from Start Page
    impl_years = shared_state.get("gi_impl", 0) or 0
    cap_years = shared_state.get("gi_cap", 0) or 0
    total_duration = impl_years + cap_years

    info = {
        "Project": shared_state.get("gi_project_name", "-"),
        "Executing agency": shared_state.get("gi_executing_agency", "-"),
        "Funding agency": shared_state.get("gi_funding_agency", "-"),
        "Country": shared_state.get("gi_country", "-"),
        "Project cost": f"${shared_state.get('gi_project_cost', 0):,.0f}", # Format with commas
        "Duration": f"{total_duration} years"
    }

    # --- 3. PREPARE STACKED DATA (Full Terminology) ---
    # Main Sector Labels (X-Axis)
    sectors = [
        "Energy", 
        "Afforestation & Reforestation", 
        "Agriculture", 
        "Forestry & Conservation"
    ]
    
    # Trace Data (Y-Axis Values)
    # Each list corresponds to [Energy_Val, ARR_Val, Agri_Val, Forest_Val]
    
    # 1. Energy
    y_energy = [energy, 0, 0, 0]
    
    # 2. Afforestation & Reforestation (ARR)
    y_arr = [0, arr, 0, 0]
    
    # 3. Forestry & Conservation
    y_forest = [0, 0, 0, forest]
    
    # 4. Agriculture Sub-categories (Stacked on the 3rd column)
    y_agri_1 = [0, 0, agri_1, 0] # Deforestation-free outgrower
    y_agri_2 = [0, 0, agri_2, 0] # Agro-industrial expansion
    y_agri_3 = [0, 0, agri_3, 0] # Sustainable intensification

    # Calculate Percentages for the second chart
    def get_percents(values, total):
        if total == 0: return [0]*4
        return [(v/total)*100 for v in values]

    p_energy = get_percents(y_energy, grand_total)
    p_arr = get_percents(y_arr, grand_total)
    p_forest = get_percents(y_forest, grand_total)
    p_agri_1 = get_percents(y_agri_1, grand_total)
    p_agri_2 = get_percents(y_agri_2, grand_total)
    p_agri_3 = get_percents(y_agri_3, grand_total)

    # --- 4. LAYOUT ---
    st.markdown("### Final Results Dashboard")
    
    col_left, col_mid, col_right = st.columns([1.5, 1, 1.5])

    # --- LEFT CHART: Absolute Stacked Bar ---
    with col_left:
        st.markdown("<h6 style='text-align:center; color:#555;'>Mitigation potential by sector and activity (tCO2e)</h6>", unsafe_allow_html=True)
        
        fig1 = go.Figure()
        
        # Add Traces with FULL NAMES
        # Base Sectors
        fig1.add_trace(go.Bar(name='Energy', x=sectors, y=y_energy, marker_color='#B0B0B0'))
        fig1.add_trace(go.Bar(name='Afforestation & Reforestation', x=sectors, y=y_arr, marker_color='#B0B0B0'))
        fig1.add_trace(go.Bar(name='Forestry & Conservation', x=sectors, y=y_forest, marker_color='#B0B0B0'))
        
        # Agriculture Stacked Components
        fig1.add_trace(go.Bar(name='Deforestation-free outgrower', x=sectors, y=y_agri_1, marker_color='#E9C46A', 
                             text=[f"{v:,.0f}" if v>0 else "" for v in y_agri_1], textposition='inside'))
        fig1.add_trace(go.Bar(name='Agro-industrial expansion', x=sectors, y=y_agri_2, marker_color='#F4A261', 
                             text=[f"{v:,.0f}" if v>0 else "" for v in y_agri_2], textposition='inside'))
        fig1.add_trace(go.Bar(name='Sustainable intensification', x=sectors, y=y_agri_3, marker_color='#E76F51', 
                             text=[f"{v:,.0f}" if v>0 else "" for v in y_agri_3], textposition='inside'))

        fig1.update_layout(
            barmode='stack',
            showlegend=True,
            # Legend at bottom, horizontal
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            height=500,
            margin=dict(t=20, b=80), # Increased bottom margin for larger legend
            paper_bgcolor='white', plot_bgcolor='white'
        )
        fig1.update_yaxes(showgrid=True, gridcolor='#eee', zeroline=True, zerolinecolor='black')
        st.plotly_chart(fig1, use_container_width=True)

    # --- MIDDLE: Info & Total ---
    with col_mid:
        # Project Info Table
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
        
        # Agriculture Details Table (Full names)
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

    # --- RIGHT CHART: Percentage Stacked Bar ---
    with col_right:
        st.markdown("<h6 style='text-align:center; color:#555;'>Contribution by sector and activity (%)</h6>", unsafe_allow_html=True)
        
        fig2 = go.Figure()
        
        # Add Traces (Percentages) - Full Names
        fig2.add_trace(go.Bar(name='Energy', x=sectors, y=p_energy, marker_color='#B0B0B0'))
        fig2.add_trace(go.Bar(name='Afforestation & Reforestation', x=sectors, y=p_arr, marker_color='#B0B0B0'))
        fig2.add_trace(go.Bar(name='Forestry & Conservation', x=sectors, y=p_forest, marker_color='#B0B0B0'))
        
        fig2.add_trace(go.Bar(name='Deforestation-free outgrower', x=sectors, y=p_agri_1, marker_color='#E9C46A',
                             text=[f"{v:.1f}%" if v>0 else "" for v in p_agri_1], textposition='inside'))
        fig2.add_trace(go.Bar(name='Agro-industrial expansion', x=sectors, y=p_agri_2, marker_color='#F4A261',
                             text=[f"{v:.1f}%" if v>0 else "" for v in p_agri_2], textposition='inside'))
        fig2.add_trace(go.Bar(name='Sustainable intensification', x=sectors, y=p_agri_3, marker_color='#E76F51',
                             text=[f"{v:.1f}%" if v>0 else "" for v in p_agri_3], textposition='inside'))

        fig2.update_layout(
            barmode='stack',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
            height=500,
            margin=dict(t=20, b=80),
            paper_bgcolor='white', plot_bgcolor='white',
            yaxis=dict(range=[0, 100])
        )
        fig2.update_yaxes(showgrid=True, gridcolor='#eee', ticksuffix="%")
        st.plotly_chart(fig2, use_container_width=True)