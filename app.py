"""
Resource Planning Engine - Complete Application
Author: Ye(Alexia) Quan
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sys
sys.path.append('src')
from optimization import optimize_budget_allocation, compare_allocation_strategies

st.set_page_config(page_title="Resource Planning Engine", page_icon="📊", layout="wide")

st.markdown("""<style>
.big-metric {font-size: 36px; font-weight: bold; color: #1f77b4;}
.metric-label {font-size: 14px; color: #666; text-transform: uppercase;}
.optimization-card {background-color: #f0f8ff; padding: 20px; border-left: 4px solid #1f77b4; margin: 15px 0; border-radius: 5px;}
.six-sigma-card {background-color: #f0fff0; padding: 20px; border-left: 4px solid #2e8b57; margin: 15px 0; border-radius: 5px;}
.warning-card {background-color: #fff8dc; padding: 20px; border-left: 4px solid #ffa500; margin: 15px 0; border-radius: 5px;}
.success-card {background-color: #f0fff0; padding: 20px; border-left: 4px solid #28a745; margin: 15px 0; border-radius: 5px;}
</style>""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        return (
            pd.read_csv('data/resource_requests.csv'),
            pd.read_csv('data/historical_roi.csv'),
            pd.read_csv('data/service_metrics.csv'),
            pd.read_csv('data/process_quality.csv'),
            pd.read_csv('data/constraints.csv')
        )
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None, None, None, None

def fmt_curr(val):
    return f"${val/1e6:.1f}M" if val >= 1e6 else f"${val/1e3:.0f}K"

def page_optimization():
    st.title("📊 Strategic Resource Allocation (PuLP Optimization)")
    
    rr, _, _, _, cons = load_data()
    if rr is None: 
        st.error("Run: python src/generate_sample_data.py")
        return
    
    budget = cons[cons['constraint_type']=='total_budget']['value'].values[0]
    requested = rr['budget_requested'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Available Budget", fmt_curr(budget))
    col2.metric("Total Requested", fmt_curr(requested))
    col3.metric("Over-Requested", fmt_curr(requested-budget))
    col4.metric("Service Lines", len(rr))
    
    st.markdown("### 🎯 PuLP Optimization Results")
    
    try:
        result = optimize_budget_allocation(rr, budget)
        
        if result['status'] == 'Optimal':
            col1, col2, col3 = st.columns(3)
            
            col1.markdown(f"""<div class='success-card'>
                <strong>✅ Status: {result['status']}</strong><br>
                Allocated: {fmt_curr(result['total_allocated'])}<br>
                Utilization: {result['budget_utilization']:.1f}%<br>
                Funded: {len(result['funded_projects'])} of {len(rr)}
            </div>""", unsafe_allow_html=True)
            
            col2.markdown(f"""<div class='success-card'>
                <strong>📈 Performance</strong><br>
                Blended ROI: {result['blended_roi']:.2f}x<br>
                Expected Return: {fmt_curr(result['total_expected_return'])}<br>
                Net Value: {fmt_curr(result['total_expected_return']-result['total_allocated'])}
            </div>""", unsafe_allow_html=True)
            
            strategies = compare_allocation_strategies(rr, budget)
            improvement = ((result['blended_roi']-strategies['Equal']['blended_roi'])/strategies['Equal']['blended_roi'])*100
            
            col3.markdown(f"""<div class='success-card'>
                <strong>💡 vs Equal Allocation</strong><br>
                Equal ROI: {strategies['Equal']['blended_roi']:.2f}x<br>
                Optimized: {result['blended_roi']:.2f}x<br>
                Improvement: +{improvement:.1f}%
            </div>""", unsafe_allow_html=True)
            
            # Table
            alloc_data = []
            for sl, info in result['allocations'].items():
                alloc_data.append({
                    'Service Line': sl,
                    'Requested': fmt_curr(info['requested']),
                    'Allocated': fmt_curr(info['allocated']),
                    'Funded': '✅' if info['funded'] else '❌',
                    'ROI': f"{info['expected_roi']:.2f}x"
                })
            st.dataframe(pd.DataFrame(alloc_data), use_container_width=True, hide_index=True)
            
            # Charts
            col1, col2 = st.columns(2)
            
            with col1:
                comp_df = pd.DataFrame({
                    'Service': list(result['allocations'].keys()),
                    'Requested': [result['allocations'][s]['requested'] for s in result['allocations'].keys()],
                    'Allocated': [result['allocations'][s]['allocated'] for s in result['allocations'].keys()]
                })
                fig = go.Figure()
                fig.add_trace(go.Bar(name='Requested', x=comp_df['Service'], y=comp_df['Requested'], marker_color='lightblue'))
                fig.add_trace(go.Bar(name='Allocated', x=comp_df['Service'], y=comp_df['Allocated'], marker_color='darkblue'))
                fig.update_layout(title='Requested vs Allocated', barmode='group', height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                funded = [s for s, i in result['allocations'].items() if i['funded']]
                amounts = [result['allocations'][s]['allocated'] for s in funded]
                fig = px.pie(values=amounts, names=funded, title='Budget Distribution', hole=0.4)
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.error(f"Optimization failed: {result['status']}")
    except Exception as e:
        st.error(f"Error: {e}")

def page_drivers():
    st.title("🎯 Driver-Based Planning Models")
    
    st.markdown("### 📈 Sales Capacity Model")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        rev_target = st.number_input("Revenue Target ($M)", 1.0, 100.0, 10.0, 0.5) * 1e6
        deal_size = st.number_input("Avg Deal Size ($K)", 10.0, 500.0, 50.0, 5.0) * 1e3
        win_rate = st.slider("Win Rate (%)", 10, 50, 25, 5) / 100
        ramp = st.slider("Ramp Time (months)", 3, 12, 6)
        quota = st.slider("Quota Attainment (%)", 60, 120, 85, 5) / 100
    
    with col2:
        deals = rev_target / deal_size
        opps = deals / win_rate
        opps_per_rep = 4 * 12 * quota
        reps = opps / opps_per_rep * (1 + ramp/12)
        cost = reps * 150000
        
        df = pd.DataFrame({
            'Metric': ['Revenue Target', 'Deals Needed', 'Opps Needed', 'Reps Required', 'Sales Investment', 'Efficiency'],
            'Value': [fmt_curr(rev_target), f"{deals:.0f}", f"{opps:.0f}", f"{reps:.0f}", fmt_curr(cost), f"{rev_target/cost:.2f}x"]
        })
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        st.markdown(f"""<div class='optimization-card'>
            💡 Hire <strong>{int(reps)} reps</strong> for {fmt_curr(rev_target)} target<br>
            Investment: {fmt_curr(cost)} | Efficiency: {rev_target/cost:.1f}x
        </div>""", unsafe_allow_html=True)

def page_scenarios():
    st.title("🔮 Scenario Modeling")
    
    col1, col2, col3 = st.columns(3)
    cons_g = col1.slider("Conservative Growth %", 10, 50, 20, key='c') / 100
    base_g = col2.slider("Base Growth %", 10, 100, 40, key='b') / 100
    agg_g = col3.slider("Aggressive Growth %", 10, 150, 60, key='a') / 100
    
    current_rev = 10e6
    scenarios = {}
    for name, growth in [('Conservative', cons_g), ('Base', base_g), ('Aggressive', agg_g)]:
        rev = current_rev * (1 + growth)
        margin = 0.20 if name == 'Conservative' else 0.25 if name == 'Base' else 0.30
        scenarios[name] = {'revenue': rev, 'income': rev * margin, 'growth': growth * 100}
    
    data = []
    for name, s in scenarios.items():
        data.append({'Scenario': name, 'Revenue': fmt_curr(s['revenue']), 'Growth': f"{s['growth']:.0f}%", 'Income': fmt_curr(s['income'])})
    
    st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    
    fig = go.Figure()
    for name in scenarios.keys():
        fig.add_trace(go.Bar(name=name, x=['Revenue', 'Income'], y=[scenarios[name]['revenue'], scenarios[name]['income']]))
    fig.update_layout(title='Scenario Comparison', barmode='group', height=400)
    st.plotly_chart(fig, use_container_width=True)

def page_sixsigma():
    st.title("⭐ Six Sigma Dashboard")
    
    _, _, sm, _, _ = load_data()
    if sm is None: return
    
    dmaic = {'Define': '✅ Complete', 'Measure': '✅ Complete', 'Analyze': '🔄 In Progress', 'Improve': '📋 Planned', 'Control': '📋 Planned'}
    cols = st.columns(5)
    for idx, (phase, status) in enumerate(dmaic.items()):
        cols[idx].markdown(f"**{phase}**<br>{status}", unsafe_allow_html=True)
    
    st.markdown("### 📊 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    onboard = sm['onboarding_time_days'].mean()
    defect = sm['defect_rate'].mean() * 100
    satis = sm['client_satisfaction'].mean()
    util = sm['team_utilization_pct'].mean()
    
    col1.metric("Onboarding", f"{onboard:.1f} days", f"{onboard-14:.1f} vs target")
    col2.metric("Defect Rate", f"{defect:.1f}%", f"{defect-3:.1f}pts vs target")
    col3.metric("Satisfaction", f"{satis:.2f}/5", f"{satis-4.5:.2f} vs target")
    col4.metric("Utilization", f"{util:.1f}%", f"{util-75:.1f}pts vs target")
    
    st.markdown("### 🔍 Root Cause Analysis (Pareto)")
    
    causes = pd.DataFrame({'Cause': ['Unclear requirements', 'Resource unavailable', 'Scope creep', 'Technical', 'Communication'], 'Freq': [35, 28, 18, 12, 8]})
    causes['Cum%'] = causes['Freq'].cumsum() / causes['Freq'].sum() * 100
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=causes['Cause'], y=causes['Freq'], marker_color='steelblue'), secondary_y=False)
    fig.add_trace(go.Scatter(x=causes['Cause'], y=causes['Cum%'], mode='lines+markers', line=dict(color='red', width=2)), secondary_y=True)
    fig.update_layout(title='Defect Causes', height=400)
    fig.update_yaxes(title_text="Frequency", secondary_y=False)
    fig.update_yaxes(title_text="Cumulative %", range=[0, 100], secondary_y=True)
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""<div class='six-sigma-card'>
        📊 Top 3 causes = 76% of defects<br>
        Priority: Requirements checklist, Resource planning, Scope control<br>
        Expected: Reduce defects 8% → 3% | Save $280K annually
    </div>""", unsafe_allow_html=True)

def page_roi():
    st.title("🎯 ROI Prioritization")
    
    rr, _, _, _, _ = load_data()
    if rr is None: return
    
    rr['fin_score'] = rr['expected_roi'] * (rr['budget_requested'] / 1e6)
    rr['fin_score'] = (rr['fin_score'] - rr['fin_score'].min()) / (rr['fin_score'].max() - rr['fin_score'].min()) * 100
    rr['strat_score'] = (rr['strategic_priority'] / 5) * 100
    rr['risk_score'] = rr['success_probability'] * 100
    rr['composite'] = rr['fin_score'] * 0.4 + rr['strat_score'] * 0.35 + rr['risk_score'] * 0.25
    
    sorted_rr = rr.sort_values('composite', ascending=False)
    
    df = sorted_rr[['service_line', 'budget_requested', 'expected_roi', 'strategic_priority', 'composite']].copy()
    df['budget_requested'] = df['budget_requested'].apply(fmt_curr)
    df['expected_roi'] = df['expected_roi'].apply(lambda x: f"{x:.2f}x")
    df['composite'] = df['composite'].apply(lambda x: f"{x:.1f}")
    df.columns = ['Service Line', 'Budget', 'ROI', 'Priority', 'Score']
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    fig = px.bar(sorted_rr, y='service_line', x='composite', title='Composite Scores', orientation='h', color='composite', color_continuous_scale='Viridis')
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def main():
    st.sidebar.title("Resource Planning Engine")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio("Navigate:", [
        "📊 Strategic Allocation",
        "🎯 Driver-Based Planning",
        "🔮 Scenario Modeling",
        "⭐ Six Sigma Dashboard",
        "🎯 ROI Prioritization"
    ])
    
    st.sidebar.markdown("---")
    st.sidebar.info("""
        **CFO Portfolio Project**
        
        Demonstrates:
        - PuLP optimization
        - Driver-based planning
        - Scenario analysis
        - Six Sigma DMAIC
        - ROI prioritization
        
        **Author:** Ye(Alexia) Quan
    """)
    
    if "Strategic" in page: page_optimization()
    elif "Driver" in page: page_drivers()
    elif "Scenario" in page: page_scenarios()
    elif "Six Sigma" in page: page_sixsigma()
    elif "ROI" in page: page_roi()

if __name__ == "__main__":
    main()
