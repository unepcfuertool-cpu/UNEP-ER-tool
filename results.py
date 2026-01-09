# results.py
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import datetime
import shared_state

def render_results_module():
    # --- 1. GATHER DATA ---
    # Retrieve totals from shared state
    energy_total = shared_state.get("energy_grand_total", 0.0) or 0.0
    arr_total = shared_state.get("arr_grand_total", 0.0) or 0.0
    agri_total = shared_state.get("agri_grand_total", 0.0) or 0.0
    forest_total = shared_state.get("forest_grand_total", 0.0) or 0.0
    
    # Calculate Grand Total
    grand_total = energy_total + arr_total + agri_total + forest_total

    # Project Information (from Start Page)
    project_info = {
        "Project": shared_state.get("project_name", "-"),
        "Executing agency": shared_state.get("executing_agency", "-"),
        "Funding agency": shared_state.get("funding_agency", "-"),
        "Country": shared_state.get("gi_country", "-"),
        "Project cost (in USD)": shared_state.get("project_cost", "0"),
        "Project duration": f"{shared_state.get('project_duration', '0')} years"
    }

    # Prepare Data for Charts
    sectors = ["Energy", "Afforestation & Restoration", "Agriculture", "Forestry & Conservation"]
    values = [energy_total, arr_total, agri_total, forest_total]
    
    # Calculate Percentages (avoid division by zero)
    if grand_total > 0:
        percentages = [(v / grand_total) * 100 for v in values]
    else:
        percentages = [0.0] * 4

    # --- 2. LAYOUT ---
    
    # Create 3 columns: Left Chart | Middle Info | Right Chart
    col_left, col_mid, col_right = st.columns([1.5, 1, 1.5])

    # --- LEFT COLUMN: CHART 1 (Absolute) ---
    with col_left:
        # Title
        st.markdown("<h6 style='text-align: center; color: #555;'>Mitigation potential by sector and activity</h6>", unsafe_allow_html=True)
        
        # Build Figure (Bar Chart)
        fig1 = go.Figure(data=[
            go.Bar(
                x=sectors,
                y=values,
                marker_color='#F4A261', # Orange/Peach color from screenshot
                text=values,
                textposition='auto',
            )
        ])
        
        # Update Layout to look "Empty"/Clean like screenshot if 0
        fig1.update_layout(
            showlegend=False, 
            height=500,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor='white',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=False,
                linecolor='black',
                ticks='outside'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#eee',
                linecolor='black',
                ticks='outside',
                zeroline=True,
                zerolinecolor='black'
            )
        )
        st.plotly_chart(fig1, use_container_width=True)


    # --- MIDDLE COLUMN: SUMMARY TABLE & CARD ---
    with col_mid:
        # A. Project Info Table (Styled HTML)
        table_html = """
        <style>
            .info-table { 
                width: 100%; 
                border-collapse: collapse; 
                font-family: sans-serif; 
                font-size: 0.85em; 
                margin-bottom: 20px; 
                border: 2px solid black; 
            }
            .info-table td { 
                border: 1px solid black; 
                padding: 8px; 
                text-align: center; /* Center align like screenshot */
            }
            .info-label { 
                background-color: #f2f2f2; 
                font-weight: bold; 
                width: 50%;
            }
            .info-val { 
                color: #007bff; /* Blue text */
                font-style: italic; 
            }
        </style>
        <table class="info-table">
        """
        for key, value in project_info.items():
            val_display = value if value else "-"
            table_html += f"<tr><td class='info-label'>{key}</td><td class='info-val'>{val_display}</td></tr>"
        table_html += "</table>"
        
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Spacer
        st.write("")

        # B. Total Mitigation Card (Green Box)
        # Matches the screenshot: Bordered box, green center
        st.markdown(f"""
        <div style="border: 2px solid black; padding: 0; text-align: center; margin-bottom: 20px;">
            <div style="padding: 15px; font-weight: bold; background-color: white; border-bottom: 1px solid #ddd;">Total mitigation potential</div>
            <div style="
                background-color: #ccf7d6; 
                padding: 40px 10px; 
                color: black;">
                <div style="font-size: 3em; font-weight: bold;">{grand_total:,.0f}</div>
                <div style="font-size: 1.2em;">tCO₂ eq.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # C. Footer Timestamp
        today = datetime.date.today().strftime("%d/%m/%Y")
        st.markdown(f"""
        <div style="text-align: center; font-size: 0.8em; color: black; font-style: italic; background-color: #f9f9f9; padding: 10px;">
            Report generated by<br>
            <strong>{today}</strong>
        </div>
        """, unsafe_allow_html=True)


    # --- RIGHT COLUMN: CHART 2 (Percentage) ---
    with col_right:
        # Title
        st.markdown("<h6 style='text-align: center; color: #555;'>Mitigation potential by sector and activity</h6>", unsafe_allow_html=True)
        
        # Build Figure (Bar Chart with Secondary Axis Look)
        fig2 = go.Figure(data=[
            go.Bar(
                x=sectors,
                y=percentages,
                marker_color='#F4A261', # Orange/Peach
                text=[f"{p:.1f}%" for p in percentages],
                textposition='auto',
            )
        ])
        
        # Update layout to mimic the 0-1.0 and 0-100% look
        fig2.update_layout(
            showlegend=False, 
            height=500,
            margin=dict(l=20, r=20, t=30, b=20),
            paper_bgcolor='white',
            plot_bgcolor='white',
            xaxis=dict(
                showgrid=False,
                linecolor='black',
                ticks='outside'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#eee',
                linecolor='black',
                ticks='outside',
                range=[0, 100], # Force 0-100% scale
                title=None
            )
        )
        
        # Add "1.0" / "100%" secondary axis simulation if desired, 
        # but standard plotly percent formatting is cleaner:
        fig2.update_yaxes(ticksuffix="%")
        
        st.plotly_chart(fig2, use_container_width=True)