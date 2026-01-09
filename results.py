# results.py
import streamlit as st
import plotly.graph_objects as go
import datetime
import shared_state

def render_results_module():
    # --- 1. GATHER DATA ---
    # Global Totals
    energy = shared_state.get("energy_grand_total", 0.0) or 0.0
    arr = shared_state.get("arr_grand_total", 0.0) or 0.0
    forest = shared_state.get("forest_grand_total", 0.0) or 0.0
    
    # Agri Sub-totals (Must match keys saved in agri.py)
    agri_1 = shared_state.get("agri_total_1", 0.0) or 0.0 # Outgrower
    agri_2 = shared_state.get("agri_total_2", 0.0) or 0.0 # Industrial
    agri_3 = shared_state.get("agri_total_3", 0.0) or 0.0 # Intensification
    agri_total = agri_1 + agri_2 + agri_3
    
    grand_total = energy + arr + agri_total + forest

    # Project Info
    info = {
        "Project": shared_state.get("project_name", "-"),
        "Executing agency": shared_state.get("executing_agency", "-"),
        "Funding agency": shared_state.get("funding_agency", "-"),
        "Country": shared_state.get("gi_country", "-"),
        "Project cost": f"${shared_state.get('project_cost', '0')}",
        "Duration": f"{shared_state.get('project_duration', '0')} years"
    }

    # Prepare Data for Charts (Breakdown including Agri Sub-categories)
    labels = [
        "Energy",
        "ARR",
        "Forestry",
        "Agri: Outgrower",
        "Agri: Industrial",
        "Agri: Intensification"
    ]
    
    values = [
        energy,
        arr,
        forest,
        agri_1,
        agri_2,
        agri_3
    ]
    
    # Percentages
    if grand_total > 0:
        percents = [(v / grand_total) * 100 for v in values]
    else:
        percents = [0.0] * len(values)

    # --- 2. LAYOUT ---
    col_left, col_mid, col_right = st.columns([1.5, 1, 1.5])

    # --- LEFT CHART: Absolute Breakdown ---
    with col_left:
        st.markdown("<h6 style='text-align:center; color:#555;'>Reduction by Category (tCO2e)</h6>", unsafe_allow_html=True)
        
        fig1 = go.Figure(go.Bar(
            x=labels, 
            y=values, 
            # Distinct colors for Agriculture to highlight them
            marker_color=['#999', '#999', '#999', '#F4A261', '#E76F51', '#2A9D8F'], 
            text=[f"{v:,.0f}" if v > 0 else "" for v in values],
            textposition='auto'
        ))
        
        fig1.update_layout(
            showlegend=False, height=500, margin=dict(t=20, b=100), 
            paper_bgcolor='white', plot_bgcolor='white'
        )
        fig1.update_yaxes(showgrid=True, gridcolor='#eee', zeroline=True, zerolinecolor='black')
        st.plotly_chart(fig1, use_container_width=True)


    # --- MIDDLE: Info & Total ---
    with col_mid:
        # 1. Info Table
        html = """<style>
            .it{width:100%; border-collapse:collapse; border:2px solid black; font-size:0.85em; font-family:sans-serif;} 
            .it td{border:1px solid black; padding:6px; text-align:center;} 
            .il{background:#f2f2f2; font-weight:bold; width:40%;} 
            .iv{color:#0056b3; font-style:italic;}
        </style><table class='it'>"""
        for k, v in info.items():
            html += f"<tr><td class='il'>{k}</td><td class='iv'>{v}</td></tr>"
        html += "</table>"
        st.markdown(html, unsafe_allow_html=True)
        
        st.write("")
        
        # 2. Green Total Box
        st.markdown(f"""
        <div style="border:2px solid black; text-align:center; margin-bottom:20px;">
            <div style="padding:10px; font-weight:bold; border-bottom:1px solid #ddd; background:white;">Total Emission Reduction</div>
            <div style="background:#ccf7d6; padding:30px 10px;">
                <div style="font-size:2.5em; font-weight:bold; color:#155724;">{grand_total:,.0f}</div>
                <div style="font-size:1.1em; color:#155724;">tCO₂ eq.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- RIGHT CHART: Percentage Breakdown ---
    with col_right:
        st.markdown("<h6 style='text-align:center; color:#555;'>Contribution by Category (%)</h6>", unsafe_allow_html=True)
        
        fig2 = go.Figure(go.Bar(
            x=labels, 
            y=percents, 
            marker_color=['#999', '#999', '#999', '#F4A261', '#E76F51', '#2A9D8F'],
            text=[f"{p:.1f}%" if p > 0 else "" for p in percents],
            textposition='auto'
        ))
        
        fig2.update_layout(
            showlegend=False, height=500, margin=dict(t=20, b=100), 
            paper_bgcolor='white', plot_bgcolor='white', 
            yaxis=dict(range=[0, 100])
        )
        fig2.update_yaxes(showgrid=True, gridcolor='#eee', ticksuffix="%")
        st.plotly_chart(fig2, use_container_width=True)