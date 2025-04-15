import streamlit as st
import plotly.graph_objects as go
from utils.lucide_icons import get_risk_icon

def display_dashboard():
    """
    Display the risk dashboard with metrics and visualizations
    """
    # Create columns for metrics
    col1, col2, col3 = st.columns(3)
    
    # Get risk metrics from session state
    risk_metrics = st.session_state.get('risk_metrics', {
        'total_risks': 0,
        'high_risk_clauses': [],
        'medium_risk_clauses': [],
        'low_risk_clauses': []
    })
    
    # Calculate risk counts
    high_risk = len(risk_metrics['high_risk_clauses'])
    medium_risk = len(risk_metrics['medium_risk_clauses'])
    low_risk = len(risk_metrics['low_risk_clauses'])
    
    # Calculate risk score if there are any clauses
    total_clauses = high_risk + medium_risk + low_risk
    risk_score = 0
    if total_clauses > 0:
        risk_score = (high_risk * 100 + medium_risk * 50) / total_clauses
    
    # Display overall risk score
    with col1:
        # Determine risk level and color
        risk_color = "red" if risk_score > 70 else \
                    "orange" if risk_score > 30 else \
                    "green"
        
        risk_level = "High Risk" if risk_score > 70 else \
                    "Medium Risk" if risk_score > 30 else \
                    "Low Risk"
                    
        # Create a gauge chart for risk score
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=risk_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Overall Risk Score"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': risk_color},
                'steps': [
                    {'range': [0, 30], 'color': "lightgreen"},
                    {'range': [30, 70], 'color': "lightyellow"},
                    {'range': [70, 100], 'color': "lightcoral"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': risk_score
                }
            }
        ))
        
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown(f"<div style='text-align: center; color: {risk_color}; font-weight: bold; font-size: 20px;'>{risk_level}</div>", unsafe_allow_html=True)
    
    # Display risk distribution
    with col2:
        st.subheader("Risk Distribution")
        
        # Create a horizontal bar chart for risk distribution
        fig = go.Figure()
        
        # Add bars for each risk level
        fig.add_trace(go.Bar(
            y=['High Risk', 'Medium Risk', 'Low Risk'],
            x=[high_risk, medium_risk, low_risk],
            orientation='h',
            marker=dict(
                color=['red', 'orange', 'green'],
                line=dict(color='rgba(0, 0, 0, 0.5)', width=1)
            )
        ))
        
        # Update layout
        fig.update_layout(
            height=200,
            margin=dict(l=20, r=20, t=20, b=20),
            xaxis=dict(
                title="Number of Clauses",
                title_font=dict(size=12),
                tickfont=dict(size=10)
            ),
            yaxis=dict(
                title_font=dict(size=12),
                tickfont=dict(size=10),
                autorange="reversed"
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Display highest risk areas
    with col3:
        st.subheader("Highest Risk Clauses")
        
        # Get clauses from session state
        clauses = st.session_state.get('clauses', {})
        
        # Get high risk clauses
        high_risk_clauses = risk_metrics['high_risk_clauses']
        
        # Display top 3 high risk clauses
        if high_risk_clauses:
            for clause_id in high_risk_clauses[:3]:
                # Get risk icon
                risk_icon = get_risk_icon('high')
                
                # Display risk clause with icon
                st.markdown(f"""
                <div style='margin-bottom: 10px;'>
                    <span style='vertical-align: middle;'>{risk_icon}</span>
                    <span style='vertical-align: middle; margin-left: 5px;'>{clause_id}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No high-risk clauses identified.")
    
    # Divider
    st.markdown("---")