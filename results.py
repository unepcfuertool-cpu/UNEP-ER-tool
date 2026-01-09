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
    
    # Agri Sub-totals (From agri.py)
    agri_1 = shared_state.get("agri_total_1", 0.0) or 0.0 # Deforestation-free outgrower
    agri_2 = shared_state.get("agri_total_2", 0.0) or 0.0 # Agro-industrial expansion
    agri_3 = shared_state.get("agri_total_3", 0.0) or 0.0 # Sustainable intensification
    agri_total = agri_1 + agri_2 + agri_3
    
    # Fallback: if totals exist but sub-totals are 0 (legacy data issue)
    if agri_total == 0 and shared_state.get("agri_grand_total", 0.0) > 0:
        agri_1 = shared_state.get("agri_grand_total", 0.0)
        agri_total = agri_1

    grand_total = energy + arr + agri_total + forest

    # Project Info (Corrected keys to match general_info.py)
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

    # --- 2. LAYOUT ---
    st.markdown("### Final Results Dashboard")
    
    col_left, col_mid, col_right = st.columns([1.5, 1, 1.5])

    # --- LEFT CHART: SECTOR OVERVIEW ---
    with col_left:
        st.markdown("<h6 style='text-align:center; color:#555;'>Global Mitigation by Sector (tCO2e)</h6>", unsafe_allow_html=True)
        
        # Data
        sec_labels = ["Energy", "Afforestation & Reforestation", "Agriculture", "Forestry & Conservation"]
        sec_values = [energy, arr, agri_total, forest]
        
        fig1 = go.Figure(go.Bar(
            x=sec_labels,
            y=sec_values,
            marker_color=['#B0B0B0', '#B0B0B0', '#2A9D8F', '#B0B0B0'], # Highlight Agri in Green
            text=[f"{v:,.0f}" if v > 0 else "" for v in sec_values],
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


    # --- RIGHT CHART: AGRICULTURE DEEP-DIVE ---
    with col_right:
        # Specific Header for Agriculture
        st.markdown("<h6 style='text-align:center; color:#2A9D8F;'>Agriculture Sector Breakdown (tCO2e)</h6>", unsafe_allow_html=True)
        
        # Data - ONLY Agriculture Categories
        agri_labels = [
            "Deforestation-free outgrower",
            "Agro-industrial expansion",
            "Sustainable intensification"
        ]
        agri_values = [agri_1, agri_2, agri_3]
        agri_colors = ['#E9C46A', '#F4A261', '#E76F51'] # Distinct colors
        
        fig2 = go.Figure(go.Bar(
            x=agri_labels,
            y=agri_values,
            marker_color=agri_colors,
            text=[f"{v:,.0f}" if v > 0 else "" for v in agri_values],
            textposition='auto'
        ))
        
        fig2.update_layout(
            showlegend=False,
            height=500,
            margin=dict(t=20, b=50),
            paper_bgcolor='white', plot_bgcolor='white'
        )
        fig2.update_yaxes(showgrid=True, gridcolor='#eee', zeroline=True, zerolinecolor='black')
        st.plotly_chart(fig2, use_container_width=True)