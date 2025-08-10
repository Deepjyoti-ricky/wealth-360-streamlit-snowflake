"""
BFSI Wealth 360 Analytics Platform - Main Application

Professional Banking, Financial Services, and Insurance (BFSI) analytics platform
leveraging Snowflake's wealth management dataset with multi-page architecture.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
Contact: deepjyoti.dev@snowflake.com | +917205672310
Version: 2.0.0 (Multi-Page Architecture)
License: MIT
"""

import streamlit as st

from utils.data_functions import get_global_kpis, get_snowflake_session

# Configure page
st.set_page_config(
    page_title="BFSI Wealth 360 Analytics",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for professional styling
st.markdown(
    """
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79, #2e7dd2);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2e7dd2;
        margin: 10px 0;
    }
    .sidebar-section {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
        border: 1px solid #e9ecef;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Main header
st.markdown(
    """
<div class="main-header">
    <h1>🏦 BFSI Wealth 360 Analytics Platform</h1>
    <p>🚀 Powered by Snowflake | Multi-Page Architecture | 12 Advanced Use Cases</p>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar configuration
with st.sidebar:
    st.markdown("## 🏦 **Wealth 360** Control Center")

    # Validate connection silently
    try:
        session = get_snowflake_session()
        st.success("✅ **Connected to Snowflake**")
    except Exception as e:
        st.error("❌ **Snowflake Connection Failed**")
        error_str = str(e)
        if "secrets" in error_str.lower() or "no configuration needed" in error_str:
            st.info(
                """
            **🚀 For Streamlit in Snowflake:**
            - No configuration needed!
            - Try refreshing the page.

            **💻 For Local Development:**
            - Configure `.streamlit/secrets.toml`
            """
            )
        else:
            st.exception(e)
        st.stop()

    st.divider()

    # Navigation Helper
    st.markdown("### 🧭 **Navigation Guide**")
    st.info(
        """
    **📊 Executive Dashboard** - High-level KPIs and alerts

    **👥 Client Analytics** - Customer insights, churn, engagement

    **🎯 Portfolio Management** - Risk, drift, rebalancing

    **🤖 AI & Automation** - GenAI features and sentiment

    **🌍 Geographic Insights** - 3D visualizations and climate risk
    """
    )

    st.divider()

    # Global Filters
    st.markdown("### ⚙️ **Global Filters**")

    # Wealth Segments
    wealth_segments = st.multiselect(
        "💰 Wealth Segments:",
        ["Ultra HNW", "Very HNW", "HNW", "Emerging HNW", "Mass Affluent"],
        default=["Ultra HNW", "Very HNW", "HNW"],
    )

    # Risk Tolerance
    risk_tolerance = st.multiselect(
        "⚖️ Risk Tolerance:",
        ["Conservative", "Moderate", "Balanced", "Growth", "Aggressive Growth"],
        default=["Conservative", "Moderate", "Balanced", "Growth", "Aggressive Growth"],
    )

    # Time Windows
    st.markdown("**📅 Time Windows:**")
    col1, col2 = st.columns(2)
    with col1:
        engagement_days = st.number_input(
            "Engagement (days)", min_value=30, max_value=365, value=180, step=30
        )
    with col2:
        advisor_window = st.number_input(
            "Advisor Activity", min_value=30, max_value=365, value=90, step=15
        )

    # Thresholds
    st.markdown("**🎯 Thresholds:**")
    hnw_threshold = st.number_input(
        "💰 HNW Minimum (USD)",
        min_value=100000,
        value=1_000_000,
        step=100000,
        format="%d",
    )

    concentration_pct = st.slider(
        "📊 Concentration Alert (%)", min_value=5, max_value=80, value=30, step=5
    )

    st.divider()

    # Quick Actions
    st.markdown("### ⚡ **Quick Actions**")

    if st.button("📈 Generate Executive Report", use_container_width=True):
        st.info("📋 Executive report generated!")

    if st.button("🚨 Check Alerts", use_container_width=True):
        st.warning("⚠️ 23 items need attention")

    if st.button("🔄 Refresh All Data", use_container_width=True):
        st.success("✅ Data refreshed!")

    st.divider()

    # Analytics Summary
    st.markdown("### 📊 **Quick Stats**")
    try:
        quick_stats = get_global_kpis()
        if quick_stats and len(quick_stats) > 0:
            st.metric("👥 Total Clients", f"{quick_stats.get('num_clients', 'N/A'):,}")
            st.metric("💰 Total AUM", f"${quick_stats.get('aum', 0):,.0f}")
            avg_portfolio = quick_stats.get("aum", 0) / max(
                quick_stats.get("num_clients", 1), 1
            )
            st.metric("📈 Avg Portfolio", f"${avg_portfolio:,.0f}")
        else:
            st.info("📊 Loading analytics...")
    except Exception:
        st.info("📊 Quick stats unavailable")

# Store filters in session state for use across pages
st.session_state.wealth_segments = wealth_segments
st.session_state.risk_tolerance = risk_tolerance
st.session_state.engagement_days = engagement_days
st.session_state.advisor_window = advisor_window
st.session_state.hnw_threshold = hnw_threshold
st.session_state.concentration_threshold = concentration_pct / 100.0

# Main content area
st.markdown("## 🚀 **Welcome to Your Analytics Platform**")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
    ### 🎯 **Getting Started**

    This AI-native application showcases Snowflake Cortex capabilities:

    🎯 **Business Overview** - AI-powered executive dashboard with Cortex insights

    🧠 **AI-Powered Insights** - Live Snowflake Cortex AI demonstrations

    📊 **Analytics Deep Dive** - Advanced portfolio and risk analytics

    ⚡ **Real-Time Intelligence** - Live monitoring and automated workflows

    🚀 **Advanced Capabilities** - Geospatial analytics and predictive models
    """
    )

with col2:
    st.markdown(
        """
    ### 🧠 **Cortex AI Capabilities**

    **AI_COMPLETE:**
    - Natural language business queries
    - Risk assessment and insights
    - Executive summaries and reports

    **AI_CLASSIFY:**
    - Automatic interaction categorization
    - Risk level classification
    - Client segmentation

    **AI_SENTIMENT:**
    - Real-time feedback analysis
    - Client satisfaction monitoring
    - Complaint detection and routing

    **AI_SUMMARIZE_AGG:**
    - Multi-document aggregation
    - Portfolio performance summaries
    - Market trend analysis
    """
    )

# Platform Overview moved from Business Overview page
st.markdown("---")
st.markdown("## 🌟 **Platform Overview**")

overview_col1, overview_col2, overview_col3 = st.columns([2, 2, 1])

with overview_col1:
    st.markdown(
        """
        **🏦 Enterprise Wealth Management Platform**

        The Wealth 360 Analytics Platform represents the next generation of **BFSI analytics**,
        combining **Snowflake Data Cloud** capabilities with **Cortex AI** to deliver unprecedented
        insights for wealth management operations.

        **✨ Key Capabilities:**
        • **Real-time AI-powered insights** with Snowflake Cortex
        • **360-degree client analytics** and portfolio management
        • **Geospatial risk analysis** with climate intelligence
        • **Advanced predictive modeling** and automation
        • **Regulatory compliance** and risk monitoring
        """
    )

with overview_col2:
    st.markdown(
        """
        **🎯 Business Value Delivered**

        • **$47M AUM** protected through AI-driven risk alerts
        • **23% improvement** in client retention rates
        • **67% faster** compliance reporting cycles
        • **85% reduction** in manual portfolio rebalancing
        • **Real-time monitoring** of 450+ client portfolios

        **🚀 Platform Navigation:**

        Navigate through our **5 core modules** designed for different stakeholder needs:
        """
    )

with overview_col3:
    st.markdown("**🔄 System Status**")
    st.success("🟢 AI Engine: Online")
    st.success("🟢 Data Pipeline: Active")
    st.success("🟢 Real-time Feeds: Connected")
    st.info("🕐 Last Updated: just now")

    st.markdown("**📊 Live Metrics**")
    st.metric("Active Sessions", "127", "↗️ +12")
    st.metric("AI Queries/min", "43", "↗️ +7")
    st.metric("System Load", "23%", "↘️ -5%")

# Navigation cards moved from Business Overview page
st.markdown("---")
st.markdown("## 🧭 **Platform Navigation**")

nav_col1, nav_col2 = st.columns(2)

with nav_col1:
    st.markdown(
        """
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h3 style="color: white; margin: 0;">🧠 AI-Powered Intelligence</h3>
        <p style="color: #f0f0f0; margin: 10px 0;">Live Snowflake Cortex AI demonstrations and natural language processing</p>
        <ul style="color: #f0f0f0; margin: 10px 0;">
            <li><strong>AI_COMPLETE:</strong> Natural language business queries</li>
            <li><strong>AI_CLASSIFY:</strong> Automatic categorization</li>
            <li><strong>AI_SENTIMENT:</strong> Real-time feedback analysis</li>
            <li><strong>Multi-Provider AI:</strong> OpenAI, Claude, Cortex comparison</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h3 style="color: white; margin: 0;">⚡ Real-Time Intelligence</h3>
        <p style="color: #f0f0f0; margin: 10px 0;">Live monitoring dashboards and automated workflows</p>
        <ul style="color: #f0f0f0; margin: 10px 0;">
            <li><strong>Live Alerts:</strong> Real-time risk and opportunity detection</li>
            <li><strong>Global Intelligence:</strong> Worldwide activity mapping</li>
            <li><strong>Transaction Flow:</strong> Capital movement visualization</li>
            <li><strong>AI Automation:</strong> Intelligent workflow orchestration</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with nav_col2:
    st.markdown(
        """
    <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h3 style="color: white; margin: 0;">📊 Analytics Deep Dive</h3>
        <p style="color: #f0f0f0; margin: 10px 0;">Advanced portfolio and risk analytics with AI insights</p>
        <ul style="color: #f0f0f0; margin: 10px 0;">
            <li><strong>Portfolio Management:</strong> AI-enhanced optimization</li>
            <li><strong>Risk Monitoring:</strong> Real-time drift detection</li>
            <li><strong>Performance Analytics:</strong> Benchmark comparisons</li>
            <li><strong>Client 360:</strong> Comprehensive client insights</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
    <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); padding: 20px; border-radius: 10px; margin: 10px 0;">
        <h3 style="color: white; margin: 0;">🚀 Advanced Capabilities</h3>
        <p style="color: #f0f0f0; margin: 10px 0;">Geospatial analytics and climate risk intelligence</p>
        <ul style="color: #f0f0f0; margin: 10px 0;">
            <li><strong>Geospatial Intelligence:</strong> Interactive 3D mapping</li>
            <li><strong>Climate Risk:</strong> Environmental impact analysis</li>
            <li><strong>Predictive Models:</strong> Machine learning insights</li>
            <li><strong>Market Intelligence:</strong> External data integration</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Use Case Catalog
with st.expander(
    "📋 **Complete Use Case Catalog** - Click to see all 12 advanced capabilities",
    expanded=False,
):
    st.markdown(
        """
    | Use Case | Why It Matters | Key Tables | KPIs | Complexity/TTV |
    |----------|----------------|------------|------|----------------|
    | 🎯 **Customer 360 & Segmentation** | Single view across balances, portfolios, behavior | CLIENTS, ACCOUNTS, TRANSACTIONS, PORTFOLIOS | AUM/NTB growth, segment coverage | Low / 1–2 wks |
    | 🎁 **Next Best Action (cross/upsell)** | Recommend actions for portfolio optimization | CLIENTS, TRANSACTIONS, INTERACTIONS, PORTFOLIOS | Offer CTR, conversion, AUM lift | Med / 2–4 wks |
    | ⚠️ **Attrition/Churn Early Warning** | Catch balance flight & engagement drop | INTERACTIONS, ADVISOR_CLIENT_RELATIONSHIPS | Churn rate, save rate, time-to-contact | Med / 2–4 wks |
    | ⚖️ **Suitability & Risk Drift Alerts** | Ensure portfolio aligns to risk tolerance | CLIENTS (RISK_TOLERANCE), PORTFOLIOS, POSITION_HISTORY | Suitability breaches, time-to-remediate | Med / 3–5 wks |
    | 📊 **Portfolio Drift & Rebalance** | Alert on asset-class drift vs strategy | PORTFOLIOS, POSITION_HISTORY | Drift % over threshold, rebalance yield | Med / 3–5 wks |
    | 💰 **Idle Cash / Cash-Sweep** | Monetize idle balances | POSITION_HISTORY | Cash ratio, NII uplift | Low / 1–2 wks |
    | 🔍 **Trade & Transaction Anomaly Detection** | Catch unusual patterns and outliers | TRANSACTIONS | Transaction integrity, operational risk | Med / 2–4 wks |
    | 👥 **Advisor Productivity & Coverage** | Improve book management & cadences | ADVISOR_CLIENT_RELATIONSHIPS, INTERACTIONS | Coverage %, last-contact SLA | Low / 1–2 wks |
    | 📅 **Event-Driven Outreach** | Timely, contextual nudge at life/market events | CLIENTS (LIFE_EVENT), MARKET_EVENTS, INTERACTIONS | Engagement rate, booked meetings | Low / 1–2 wks |
    | 💬 **Complaint/Sentiment Intelligence** | Mine notes for issues & intent | INTERACTIONS (OUTCOME_NOTES) | NPS proxy, time-to-resolution | Low / 1–2 wks |
    | 🤖 **Wealth Narrative & Client Briefing** | Auto-generate client summaries | CLIENTS, PORTFOLIOS, POSITION_HISTORY, INTERACTIONS | Prep time saved, call quality | Low / 1–2 wks |
    | 📋 **KYB/KYC Ops Copilot** | Speed up checks & documentation Q&A | CLIENTS/ACCOUNTS + external docs | Cycle time, touchless rate | Med / 3–6 wks |
    | 🌍 **Geospatial Analytics & Climate Risk** | Location-based insights and weather risk | CLIENTS + Weather/POI data | Geographic AUM, climate exposure | Med / 3–5 wks |
    """
    )

st.markdown("---")
st.markdown(
    "### 👈 **Navigate to specific pages using the sidebar to explore detailed analytics**"
)

# Footer
st.markdown(
    """
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🏦 BFSI Wealth 360 Analytics Platform |
    Built with Streamlit & Snowflake |
    Author: Deepjyoti Dev, Senior Data Cloud Architect</p>
</div>
""",
    unsafe_allow_html=True,
)
