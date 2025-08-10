"""
Analytics Deep Dive - Professional Portfolio Analytics

This page provides comprehensive portfolio analytics with enhanced visual design,
featuring risk monitoring, drift analysis, and performance optimization.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_functions import (
    get_advisor_productivity,
    get_idle_cash_analysis,
    get_portfolio_drift_analysis,
    get_suitability_risk_alerts,
    get_trade_fee_anomalies,
)

st.set_page_config(page_title="Analytics Deep Dive", page_icon="📊", layout="wide")

# Sidebar - Analytics Configuration & Filters
st.sidebar.markdown("## 📊 **Analytics Configuration**")

# Portfolio Filters
st.sidebar.markdown("### 🎯 **Portfolio Filters**")
selected_portfolios = st.sidebar.multiselect(
    "Select Portfolios",
    ["All Portfolios", "Growth", "Conservative", "Balanced", "Aggressive", "Income"],
    default=["All Portfolios"],
)

advisor_filter = st.sidebar.selectbox(
    "Filter by Advisor",
    ["All Advisors", "Top Performers", "New Advisors", "High Risk", "Custom"],
    index=0,
)

# Risk Analysis Settings
st.sidebar.markdown("### ⚠️ **Risk Analysis Settings**")
risk_tolerance = st.sidebar.slider("Risk Tolerance Threshold", 0.0, 10.0, 7.5, 0.5)
drift_threshold = st.sidebar.slider("Portfolio Drift Alert (%)", 1.0, 20.0, 5.0, 1.0)
volatility_window = st.sidebar.selectbox(
    "Volatility Analysis Window", ["1 Month", "3 Months", "6 Months", "1 Year"], index=2
)

# Performance Benchmarks
st.sidebar.markdown("### 📈 **Performance Benchmarks**")
primary_benchmark = st.sidebar.selectbox(
    "Primary Benchmark",
    ["S&P 500", "NASDAQ", "Russell 2000", "MSCI World", "Custom Blend"],
    index=0,
)

comparison_period = st.sidebar.selectbox(
    "Comparison Period",
    ["1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "3 Years"],
    index=4,
)

# Alert Configuration
st.sidebar.markdown("### 🚨 **Alert Configuration**")
enable_drift_alerts = st.sidebar.checkbox("🎯 Portfolio Drift Alerts", value=True)
enable_performance_alerts = st.sidebar.checkbox("📈 Performance Alerts", value=True)
enable_risk_alerts = st.sidebar.checkbox("⚠️ Risk Level Alerts", value=True)
enable_compliance_alerts = st.sidebar.checkbox("📋 Compliance Alerts", value=True)

# Real-time Analytics Monitoring
st.sidebar.markdown("### 📊 **Analytics Monitoring**")
portfolios_analyzed = st.sidebar.metric("Portfolios Analyzed", "892", "↗️ +47")
avg_analysis_time = st.sidebar.metric("Avg Analysis Time", "0.8s", "↘️ -0.1s")
active_alerts = st.sidebar.metric("Active Alerts", "23", "↗️ +5")

# Advanced Analytics Options
st.sidebar.markdown("### 🔬 **Advanced Analytics**")
enable_ml_predictions = st.sidebar.checkbox("🤖 ML Predictions", value=True)
enable_stress_testing = st.sidebar.checkbox("⚡ Stress Testing", value=False)
enable_scenario_analysis = st.sidebar.checkbox("🎭 Scenario Analysis", value=False)

# Export & Reporting
st.sidebar.markdown("### 📤 **Export & Reporting**")
if st.sidebar.button("📊 Export Analytics Report", use_container_width=True):
    st.sidebar.success("Analytics report exported!")

if st.sidebar.button("📈 Export Performance Data", use_container_width=True):
    st.sidebar.success("Performance data exported!")

if st.sidebar.button("🚨 Export Alert Summary", use_container_width=True):
    st.sidebar.success("Alert summary exported!")

# Navigation
st.sidebar.markdown("### 🧭 **Navigation**")
if st.sidebar.button("🧠 AI-Powered Insights ←", use_container_width=True):
    st.switch_page("pages/02_🧠_AI_Powered_Insights.py")

if st.sidebar.button("⚡ Real-Time Intelligence →", use_container_width=True):
    st.switch_page("pages/04_⚡_Real_Time_Intelligence.py")

# Custom CSS for professional styling
st.markdown(
    """
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 10px 0;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }
    .risk-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .opportunity-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Page header with enhanced design
st.markdown(
    """
<div style="background: linear-gradient(90deg, #1e3c72 0%, #2a5298 100%); padding: 30px; border-radius: 15px; color: white; text-align: center; margin-bottom: 30px;">
    <h1>📊 Analytics Deep Dive</h1>
    <p style="font-size: 18px; margin-bottom: 0;">Advanced portfolio analytics enhanced by Cortex AI intelligence</p>
</div>
""",
    unsafe_allow_html=True,
)

# Analytics Overview Dashboard
st.markdown("### 🎯 **Portfolio Analytics Overview**")

# Key metrics in cards
metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)

with metrics_col1:
    st.markdown(
        """
    <div class="metric-card">
        <h3>💰 Total AUM</h3>
        <h2>$895M</h2>
        <p>+5.7% YTD</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with metrics_col2:
    st.markdown(
        """
    <div class="metric-card">
        <h3>📊 Portfolios</h3>
        <h2>1,247</h2>
        <p>Active management</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with metrics_col3:
    st.markdown(
        """
    <div class="metric-card">
        <h3>⚖️ Risk Score</h3>
        <h2>7.2/10</h2>
        <p>Moderate risk</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with metrics_col4:
    st.markdown(
        """
    <div class="metric-card">
        <h3>🎯 Compliance</h3>
        <h2>98.3%</h2>
        <p>Above benchmark</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.divider()

# Professional Analytics Sections
analytics_tabs = st.tabs(
    [
        "⚖️ Risk & Suitability",
        "📈 Portfolio Drift",
        "💰 Cash Management",
        "🔍 Anomaly Detection",
        "👥 Advisor Analytics",
    ]
)

# Risk & Suitability Analysis
with analytics_tabs[0]:
    st.markdown("### ⚖️ **Risk & Suitability Analysis**")

    suitability_alerts = get_suitability_risk_alerts()

    # Risk Overview Cards
    risk_col1, risk_col2, risk_col3 = st.columns(3)

    with risk_col1:
        st.markdown(
            """
        <div class="risk-card">
            <h4>🔴 High Risk Items</h4>
            <h2>7</h2>
            <p>Immediate attention required</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with risk_col2:
        st.markdown(
            """
        <div class="opportunity-card">
            <h4>🟡 Medium Risk Items</h4>
            <h2>16</h2>
            <p>Review within 30 days</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with risk_col3:
        st.markdown(
            """
        <div class="success-card">
            <h4>🟢 Low Risk Items</h4>
            <h2>342</h2>
            <p>Within acceptable range</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    if not suitability_alerts.empty:
        # Risk Analysis Visualization
        col1, col2 = st.columns([2, 1])

        with col1:
            # Enhanced risk distribution chart
            alert_counts = suitability_alerts["ALERT_LEVEL"].value_counts()
            fig = go.Figure(
                data=[
                    go.Bar(
                        x=alert_counts.index,
                        y=alert_counts.values,
                        marker=dict(
                            color=["#ff4444", "#ffa500", "#90ee90"],
                            line=dict(color="rgba(255,255,255,0.8)", width=2),
                        ),
                        text=alert_counts.values,
                        textposition="auto",
                    )
                ]
            )
            fig.update_layout(
                title="Risk Alert Distribution", template="plotly_white", height=400
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown("**🎯 Risk Mitigation Actions**")
            st.markdown(
                """
            **High Priority (Immediate):**
            • Portfolio concentration review
            • Suitability realignment
            • Client communication

            **Medium Priority (30 days):**
            • Quarterly risk assessment
            • Strategy optimization
            • Performance review

            **Monitoring:**
            • Automated alerts
            • Compliance tracking
            • Regular reporting
            """
            )

        # Detailed Risk Table
        st.markdown("**📋 Detailed Risk Analysis**")
        st.dataframe(
            suitability_alerts.style.format({"TOTAL_PORTFOLIO_VALUE": "${:,.0f}"}),
            use_container_width=True,
        )

# Portfolio Drift Analysis
with analytics_tabs[1]:
    st.markdown("### 📈 **Portfolio Drift & Rebalancing**")

    drift_analysis = get_portfolio_drift_analysis()

    if not drift_analysis.empty:
        # Drift Overview
        drift_col1, drift_col2, drift_col3 = st.columns(3)

        high_drift = len(drift_analysis[drift_analysis["DRIFT_LEVEL"] == "High"])
        medium_drift = len(drift_analysis[drift_analysis["DRIFT_LEVEL"] == "Medium"])
        low_drift = len(drift_analysis[drift_analysis["DRIFT_LEVEL"] == "Low"])

        with drift_col1:
            st.markdown(
                f"""
            <div class="risk-card">
                <h4>⚠️ High Drift</h4>
                <h2>{high_drift}</h2>
                <p>Rebalancing required</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with drift_col2:
            st.markdown(
                f"""
            <div class="opportunity-card">
                <h4>📊 Medium Drift</h4>
                <h2>{medium_drift}</h2>
                <p>Monitor closely</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with drift_col3:
            st.markdown(
                f"""
            <div class="success-card">
                <h4>✅ Low Drift</h4>
                <h2>{low_drift}</h2>
                <p>Within target range</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Enhanced Drift Visualization
        col1, col2 = st.columns(2)

        with col1:
            # 3D scatter plot for drift analysis
            fig = px.scatter_3d(
                drift_analysis,
                x="CURRENT_PCT",
                y="TARGET_PCT",
                z="DRIFT_PCT",
                color="DRIFT_LEVEL",
                size="CURRENT_VALUE",
                hover_data=["PORTFOLIO_ID", "ASSET_CLASS"],
                title="Portfolio Drift Analysis (3D View)",
                color_discrete_map={
                    "High": "#ff4444",
                    "Medium": "#ffa500",
                    "Low": "#90ee90",
                },
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Asset class drift summary
            asset_drift = (
                drift_analysis.groupby("ASSET_CLASS")
                .agg({"DRIFT_PCT": ["mean", "max", "count"], "CURRENT_VALUE": "sum"})
                .round(2)
            )

            asset_drift.columns = ["Avg Drift %", "Max Drift %", "Count", "Total Value"]

            st.markdown("**📊 Asset Class Analysis**")
            st.dataframe(
                asset_drift.style.format(
                    {
                        "Total Value": "${:,.0f}",
                        "Avg Drift %": "{:.1f}%",
                        "Max Drift %": "{:.1f}%",
                    }
                ),
                use_container_width=True,
            )

# Cash Management
with analytics_tabs[2]:
    st.markdown("### 💰 **Cash Management & Optimization**")

    idle_cash = get_idle_cash_analysis()

    if not idle_cash.empty:
        # Cash overview metrics
        total_idle_cash = idle_cash["CASH_BALANCE"].sum()
        potential_income = idle_cash["POTENTIAL_ANNUAL_INCOME"].sum()
        high_priority_count = len(
            idle_cash[idle_cash["SWEEP_PRIORITY"] == "High Priority"]
        )

        cash_col1, cash_col2, cash_col3 = st.columns(3)

        with cash_col1:
            st.markdown(
                f"""
            <div class="opportunity-card">
                <h4>💰 Total Idle Cash</h4>
                <h2>${total_idle_cash:,.0f}</h2>
                <p>Optimization opportunity</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with cash_col2:
            st.markdown(
                f"""
            <div class="success-card">
                <h4>📈 Revenue Potential</h4>
                <h2>${potential_income:,.0f}</h2>
                <p>Annual income opportunity</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with cash_col3:
            st.markdown(
                f"""
            <div class="risk-card">
                <h4>🚨 High Priority</h4>
                <h2>{high_priority_count}</h2>
                <p>Immediate action items</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Cash Analysis Visualizations
        col1, col2 = st.columns(2)

        with col1:
            # Cash distribution by priority
            priority_counts = idle_cash["SWEEP_PRIORITY"].value_counts()
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="Cash Sweep Priority Distribution",
                color_discrete_map={
                    "High Priority": "#ff4444",
                    "Medium Priority": "#ffa500",
                    "Low Priority": "#90ee90",
                    "Acceptable": "#87ceeb",
                },
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Cash vs portfolio size bubble chart
            fig = px.scatter(
                idle_cash,
                x="TOTAL_PORTFOLIO_VALUE",
                y="CASH_BALANCE",
                size="CASH_PERCENTAGE",
                color="SWEEP_PRIORITY",
                title="Cash vs Portfolio Size Analysis",
                labels={
                    "TOTAL_PORTFOLIO_VALUE": "Portfolio Value ($)",
                    "CASH_BALANCE": "Cash Balance ($)",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

# Anomaly Detection
with analytics_tabs[3]:
    st.markdown("### 🔍 **Transaction Anomaly Detection**")

    anomalies_df = get_trade_fee_anomalies()

    if not anomalies_df.empty:
        # Anomaly overview
        total_anomalies = len(anomalies_df)
        critical_count = len(
            anomalies_df[
                anomalies_df["ANOMALY_TYPE"].isin(
                    ["Unusually Large Transaction", "Statistical Outlier - High Value"]
                )
            ]
        )

        anomaly_col1, anomaly_col2 = st.columns(2)

        with anomaly_col1:
            st.markdown(
                f"""
            <div class="risk-card">
                <h4>🔍 Total Anomalies</h4>
                <h2>{total_anomalies}</h2>
                <p>Last 90 days</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with anomaly_col2:
            st.markdown(
                f"""
            <div class="opportunity-card">
                <h4>🚨 Critical Anomalies</h4>
                <h2>{critical_count}</h2>
                <p>Require investigation</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Anomaly timeline and analysis
        col1, col2 = st.columns(2)

        with col1:
            # Anomaly timeline
            fig = px.scatter(
                anomalies_df,
                x="TIMESTAMP",
                y="TOTAL_AMOUNT",
                color="ANOMALY_TYPE",
                size="QUANTITY",
                title="Anomaly Timeline - Last 90 Days",
                labels={"TIMESTAMP": "Date", "TOTAL_AMOUNT": "Amount ($)"},
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Anomaly type distribution
            anomaly_counts = anomalies_df["ANOMALY_TYPE"].value_counts()
            fig = px.bar(
                x=anomaly_counts.values,
                y=anomaly_counts.index,
                orientation="h",
                title="Anomaly Types Distribution",
                labels={"x": "Count", "y": "Anomaly Type"},
            )
            st.plotly_chart(fig, use_container_width=True)

# Advisor Analytics
with analytics_tabs[4]:
    st.markdown("### 👥 **Advisor Performance Analytics**")

    advisor_data = get_advisor_productivity()

    if not advisor_data.empty:
        # Advisor metrics overview
        total_advisors = len(advisor_data)
        avg_aum = advisor_data["TOTAL_AUM"].mean()
        avg_clients = advisor_data["TOTAL_CLIENTS"].mean()

        advisor_col1, advisor_col2, advisor_col3 = st.columns(3)

        with advisor_col1:
            st.markdown(
                f"""
            <div class="metric-card">
                <h4>👥 Total Advisors</h4>
                <h2>{total_advisors}</h2>
                <p>Active advisors</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with advisor_col2:
            st.markdown(
                f"""
            <div class="success-card">
                <h4>💰 Avg AUM</h4>
                <h2>${avg_aum:,.0f}</h2>
                <p>Per advisor</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with advisor_col3:
            st.markdown(
                f"""
            <div class="opportunity-card">
                <h4>👤 Avg Clients</h4>
                <h2>{avg_clients:.0f}</h2>
                <p>Per advisor</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Advisor performance analysis
        col1, col2 = st.columns(2)

        with col1:
            # Advisor efficiency scatter plot
            fig = px.scatter(
                advisor_data,
                x="TOTAL_CLIENTS",
                y="TOTAL_AUM",
                size="INTERACTIONS_PER_CLIENT",
                color="SPECIALIZATION",
                hover_data=["ADVISOR_NAME"],
                title="Advisor Efficiency: Clients vs AUM",
                labels={
                    "TOTAL_CLIENTS": "Number of Clients",
                    "TOTAL_AUM": "Total AUM ($)",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Top performers
            top_performers = advisor_data.nlargest(10, "TOTAL_AUM")
            fig = px.bar(
                top_performers,
                x="ADVISOR_NAME",
                y="TOTAL_AUM",
                title="Top 10 Advisors by AUM",
                labels={"TOTAL_AUM": "Total AUM ($)"},
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

# Analytics Summary Dashboard
st.divider()
st.markdown("### 📋 **Analytics Summary Dashboard**")

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    st.markdown(
        """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4444;">
        <h4>⚖️ Risk Alerts</h4>
        <p><strong>7</strong> High Priority</p>
        <p><strong>16</strong> Medium Priority</p>
        <p><strong>342</strong> Low Risk</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with summary_col2:
    st.markdown(
        """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #ffa500;">
        <h4>📊 Portfolio Drift</h4>
        <p><strong>23</strong> Portfolios with drift</p>
        <p><strong>7</strong> High drift</p>
        <p><strong>16</strong> Medium drift</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with summary_col3:
    st.markdown(
        """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #90ee90;">
        <h4>💰 Cash Optimization</h4>
        <p><strong>$47M</strong> Idle cash</p>
        <p><strong>$1.8M</strong> Potential income</p>
        <p><strong>12</strong> High priority</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with summary_col4:
    st.markdown(
        """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #4fc3f7;">
        <h4>🔍 Anomalies</h4>
        <p><strong>89</strong> Total anomalies</p>
        <p><strong>12</strong> Critical</p>
        <p><strong>77</strong> Minor</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Navigation footer
st.divider()
st.markdown(
    """
### 🚀 **Next Steps**
- **⚡ Real-Time Intelligence**: Live monitoring and automated workflows
- **🚀 Advanced Capabilities**: Geospatial analytics and predictive modeling
- **🧠 AI-Powered Insights**: Return to Cortex AI demonstrations
"""
)
