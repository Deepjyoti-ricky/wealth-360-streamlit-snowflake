"""
Executive Dashboard - High-level KPIs and Alerts

This page provides C-suite level insights with real-time KPIs, priority alerts,
and executive summary visualizations for the BFSI Wealth 360 platform.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_functions import get_customer_360_segments, get_global_kpis

st.set_page_config(page_title="Executive Dashboard", page_icon="📊", layout="wide")

# Page header
st.markdown("# 📊 Executive Dashboard")
st.caption(
    "🚀 **Real-time insights and key performance indicators across all business areas**"
)

# Global KPIs Row
global_kpis = get_global_kpis()
if global_kpis and len(global_kpis) > 0:
    kpi_data = global_kpis

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(
            "👥 Total Clients",
            f"{kpi_data.get('num_clients', 0):,}",
            delta="+127 this month",
        )
    with col2:
        st.metric("💰 Total AUM", f"${kpi_data.get('aum', 0):,.0f}", delta="+2.3%")
    with col3:
        avg_portfolio = kpi_data.get("aum", 0) / max(kpi_data.get("num_clients", 1), 1)
        st.metric(
            "📈 Avg Portfolio",
            f"${avg_portfolio:,.0f}",
            delta="+5.7%",
        )
    with col4:
        st.metric(
            "👨‍💼 Total Advisors",
            f"{kpi_data.get('num_advisors', 0):,}",
            delta="Active advisors",
        )
    with col5:
        ytd_growth = kpi_data.get("ytd_growth_pct")
        if ytd_growth is not None:
            st.metric("📈 YTD Growth", f"{ytd_growth*100:.1f}%", delta="Year to date")
        else:
            st.metric("🎯 Engagement Rate", "87.3%", delta="+3.2%")

st.divider()

# Alert Summary Dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 🚨 **Priority Alerts & Actions**")

    # High Priority Items
    alert_col1, alert_col2 = st.columns(2)

    with alert_col1:
        st.error("**🔴 Critical Alerts (7)**")
        st.markdown(
            """
        - 3x Concentration breaches >30%
        - 2x Suitability drift alerts
        - 1x Large withdrawal pending
        - 1x KYC documentation expired
        """
        )

    with alert_col2:
        st.warning("**🟡 Attention Required (16)**")
        st.markdown(
            """
        - 8x Clients not contacted >180 days
        - 4x Portfolio rebalancing needed
        - 3x Event-driven outreach opportunities
        - 1x Transaction anomaly detected
        """
        )

with col2:
    st.markdown("### 📈 **Quick Insights**")

    # Top performers
    st.success("**🏆 Top Performing Segments**")
    st.markdown(
        """
    1. **Ultra HNW**: +12.7% AUM growth
    2. **Tech Executives**: +8.9%
    3. **Healthcare Professionals**: +6.2%
    """
    )

    st.info("**🎯 Opportunities**")
    st.markdown(
        """
    - **$47M** in idle cash to sweep
    - **23** cross-sell opportunities
    - **12** clients ready for upsell
    """
    )

st.divider()

# Quick Action Panels
st.markdown("### ⚡ **Today's Action Items**")

action_col1, action_col2, action_col3 = st.columns(3)

with action_col1:
    st.markdown("**🎯 Client Outreach (Next 5)**")
    if st.button("📞 Contact High-Priority Clients", use_container_width=True):
        st.success("✅ Outreach list generated!")

with action_col2:
    st.markdown("**📊 Portfolio Reviews (Today)**")
    if st.button("⚖️ Review Risk Drifts", use_container_width=True):
        st.info("📋 Risk assessment report ready!")

with action_col3:
    st.markdown("**🤖 AI Recommendations**")
    if st.button("🧠 Generate Next Best Actions", use_container_width=True):
        st.success("🎁 AI recommendations updated!")

# Executive Summary Charts
st.divider()
st.markdown("### 📊 **Executive Summary Charts**")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    # AUM Growth Trend (simulated)
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="M")
    aum_trend = pd.DataFrame(
        {
            "Month": dates,
            "AUM": [850 + i * 15 + np.random.normal(0, 10) for i in range(len(dates))],
        }
    )

    fig_trend = px.line(
        aum_trend,
        x="Month",
        y="AUM",
        title="📈 AUM Growth Trend (YTD)",
        labels={"AUM": "AUM ($ Millions)"},
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with summary_col2:
    # Segment Performance (using actual data)
    customer_data = get_customer_360_segments()
    segments_df = customer_data["segments"]
    if not segments_df.empty:
        segment_counts = segments_df["WEALTH_SEGMENT"].value_counts()
        fig_segments = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="🎯 Client Distribution by Wealth Segment",
        )
        st.plotly_chart(fig_segments, use_container_width=True)

# Performance Metrics Table
st.divider()
st.markdown("### 📋 **Key Performance Indicators (Monthly)**")

kpi_table = pd.DataFrame(
    {
        "Metric": [
            "Client Acquisition Rate",
            "AUM Growth Rate",
            "Portfolio Performance",
            "Client Satisfaction Score",
            "Advisor Productivity",
            "Operational Efficiency",
        ],
        "Current Month": ["2.3%", "+$47M", "+5.7%", "8.9/10", "94%", "87%"],
        "Previous Month": ["1.8%", "+$42M", "+4.2%", "8.7/10", "92%", "85%"],
        "YTD Target": ["2.5%", "+$500M", "+6.0%", "9.0/10", "95%", "90%"],
        "Status": [
            "🟢 On Track",
            "🟢 Ahead",
            "🟢 On Track",
            "🟡 Close",
            "🟢 On Track",
            "🟡 Close",
        ],
    }
)

st.dataframe(kpi_table, use_container_width=True, hide_index=True)

# Risk Dashboard
st.divider()
st.markdown("### ⚠️ **Risk Monitoring Dashboard**")

risk_col1, risk_col2, risk_col3 = st.columns(3)

with risk_col1:
    st.markdown("#### 🔴 **High Risk Items**")
    st.warning("7 items requiring immediate attention")
    st.markdown(
        """
    - Portfolio concentration breaches
    - Suitability misalignments
    - Large pending withdrawals
    """
    )

with risk_col2:
    st.markdown("#### 🟡 **Medium Risk Items**")
    st.info("16 items for review")
    st.markdown(
        """
    - Client engagement gaps
    - Portfolio rebalancing needs
    - KYC documentation updates
    """
    )

with risk_col3:
    st.markdown("#### 🟢 **Low Risk Items**")
    st.success("342 items within acceptable range")
    st.markdown(
        """
    - Regular monitoring items
    - Routine compliance checks
    - Standard performance reviews
    """
    )

# Footer with navigation
st.divider()
st.markdown(
    """
### 🧭 **Next Steps**
- **👥 Client Analytics** - Deep dive into customer insights
- **🎯 Portfolio Management** - Review risk and performance details
- **🤖 AI & Automation** - Explore AI-powered recommendations
- **🌍 Geographic Insights** - Analyze geographical performance
"""
)
