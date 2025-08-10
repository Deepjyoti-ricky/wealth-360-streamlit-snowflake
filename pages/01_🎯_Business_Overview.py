"""
Business Overview - Executive Dashboard with Cortex AI

This page provides C-suite level insights powered by Snowflake Cortex AI,
demonstrating real-time KPIs, AI-driven alerts, and intelligent summaries.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_functions import get_customer_360_segments, get_global_kpis

st.set_page_config(page_title="Business Overview", page_icon="🎯", layout="wide")

# Sidebar - Executive Controls & Navigation
st.sidebar.markdown("## 🎯 **Executive Controls**")

# Global Settings Section
st.sidebar.markdown("### ⚙️ **Dashboard Settings**")
refresh_interval = st.sidebar.selectbox(
    "Auto-refresh Interval",
    ["Manual", "30 seconds", "1 minute", "5 minutes", "15 minutes"],
    index=2,
)

show_ai_insights = st.sidebar.checkbox("🧠 Enable AI Insights", value=True)
show_alerts = st.sidebar.checkbox("🚨 Show Priority Alerts", value=True)
executive_mode = st.sidebar.checkbox(
    "👔 Executive Mode", value=True, help="Simplified view for C-suite"
)

# Time Range Filter
st.sidebar.markdown("### 📅 **Time Range**")
time_period = st.sidebar.selectbox(
    "Analysis Period",
    ["Last 24 Hours", "Last Week", "Last Month", "Last Quarter", "YTD", "Custom"],
    index=4,
)

# Key Metrics Filter
st.sidebar.markdown("### 📊 **Key Metrics Focus**")
focus_metrics = st.sidebar.multiselect(
    "Primary KPIs",
    [
        "AUM Growth",
        "Client Acquisition",
        "Revenue",
        "Risk Metrics",
        "Performance",
        "Alerts",
    ],
    default=["AUM Growth", "Client Acquisition", "Risk Metrics"],
)

# Alert Threshold Settings
st.sidebar.markdown("### 🚨 **Alert Thresholds**")
risk_threshold = st.sidebar.slider("Risk Alert Threshold", 0.0, 100.0, 85.0, 5.0)
performance_threshold = st.sidebar.slider(
    "Performance Alert (%)", -10.0, 10.0, -3.0, 0.5
)

# Quick Navigation
st.sidebar.markdown("### 🧭 **Quick Navigation**")
if st.sidebar.button("🧠 AI-Powered Insights →", use_container_width=True):
    st.switch_page("pages/02_🧠_AI_Powered_Insights.py")

if st.sidebar.button("📊 Analytics Deep Dive →", use_container_width=True):
    st.switch_page("pages/03_📊_Analytics_Deep_Dive.py")

if st.sidebar.button("⚡ Real-Time Intelligence →", use_container_width=True):
    st.switch_page("pages/04_⚡_Real_Time_Intelligence.py")

if st.sidebar.button("🚀 Advanced Capabilities →", use_container_width=True):
    st.switch_page("pages/05_🚀_Advanced_Capabilities.py")

# Export Options
st.sidebar.markdown("### 📤 **Export Options**")
if st.sidebar.button("📋 Export Executive Summary", use_container_width=True):
    st.sidebar.success("Executive summary exported!")

if st.sidebar.button("📈 Export KPI Dashboard", use_container_width=True):
    st.sidebar.success("KPI dashboard exported!")

# Page header for Business Overview only
st.markdown("# 🎯 Business Overview")
st.caption(
    "🧠 **AI-Powered Executive Dashboard | Real-time insights with Snowflake Cortex Intelligence**"
)

# Professional tile CSS
st.markdown(
    """
<style>
.tile-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.tile { border-radius: 12px; padding: 16px; color: #fff; box-shadow: 0 6px 18px rgba(0,0,0,0.12); }
.tile h3 { margin: 0 0 6px 0; font-size: 18px; font-weight: 700; }
.tile p { margin: 0; font-size: 28px; font-weight: 700; }
.tile small { display: block; margin-top: 6px; opacity: 0.85; font-weight: 500; }
.tile.red { background: linear-gradient(135deg, #ff5858 0%, #fb2d2d 100%); }
.tile.blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
.tile.purple { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
.tile.green { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: #0c4633; }
.tile .delta-up { color: #d4fff2; font-weight: 600; }
.tile .delta-down { color: #ffe6e6; font-weight: 600; }
@media (max-width: 1200px) { .tile-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 768px) { .tile-grid { grid-template-columns: 1fr; } }
</style>
""",
    unsafe_allow_html=True,
)

# Executive tiles (overview)
try:
    kpis = get_global_kpis()
    total_clients = f"{kpis.get('num_clients', 0):,}"
    total_aum = f"${kpis.get('aum', 0):,.0f}"
    avg_portfolio_val = 0
    if kpis.get("num_clients", 0):
        avg_portfolio_val = kpis.get("aum", 0) / max(kpis.get("num_clients", 1), 1)
    avg_portfolio = f"${avg_portfolio_val:,.0f}"
    ytd = kpis.get("ytd_growth_pct")
    ytd_text = (
        f"{ytd*100:.2f}%"
        if isinstance(ytd, (int, float)) and ytd is not None
        else "N/A"
    )

    tiles_html = f"""
    <div class='tile-grid'>
        <div class='tile blue'>
            <h3>👥 Total Clients</h3>
            <p>{total_clients}</p>
            <small class='delta-up'>↗️ Healthy growth</small>
        </div>
        <div class='tile purple'>
            <h3>💰 Total AUM</h3>
            <p>{total_aum}</p>
            <small class='delta-up'>↗️ Above forecast</small>
        </div>
        <div class='tile green'>
            <h3>📈 Avg Portfolio</h3>
            <p>{avg_portfolio}</p>
            <small class='delta-up'>↗️ Optimization impact</small>
        </div>
        <div class='tile red'>
            <h3>📊 YTD Growth</h3>
            <p>{ytd_text}</p>
            <small class='delta-up'>↗️ Cortex forecast improving</small>
        </div>
    </div>
    """
    st.markdown(tiles_html, unsafe_allow_html=True)
except Exception:
    pass

# AI-Powered Executive Summary
st.markdown("### 🧠 **AI-Generated Executive Summary**")

# Executive summary with bullet points
with st.container():
    st.success("🤖 **Cortex AI Intelligence Report** - Generated in real-time")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
        **📈 Market Performance & Growth**
        • **AUM Growth**: +5.7% YTD indicating strong market positioning
        • **Client Acquisition**: 127 new accounts adding $23M in assets
        • **Performance**: Growth portfolios outperforming by 3.2%

        **🎯 Risk Management Excellence**
        • **Portfolio Drift**: Prevented $8.3M potential losses across 127 portfolios
        • **Compliance**: 98.3% adherence to suitability requirements
        • **Early Warning**: 12 churn risks identified with intervention plans
        """
        )

    with col2:
        st.markdown(
            """
        **👥 Client & Advisor Optimization**
        • **Client Retention**: 94.2% retention rate exceeding industry average
        • **Advisor Productivity**: 15% improvement through AI workflow optimization
        • **Engagement**: $12M AUM preserved through proactive churn prevention

        **💰 Revenue Opportunities**
        • **Idle Cash**: $47M identified for sweep programs
        • **Revenue Potential**: $1.8M estimated annual revenue from optimization
        • **Cross-sell Pipeline**: 23 high-probability opportunities identified
        """
        )

# Real-time KPIs with AI-powered deltas
st.markdown("### 📊 **Real-Time Performance Metrics**")

global_kpis = get_global_kpis()
if global_kpis and len(global_kpis) > 0:
    kpi_data = global_kpis

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(
            "👥 Total Clients",
            f"{kpi_data.get('num_clients', 0):,}",
            delta="+127 (AI Predicted Growth)",
        )
    with col2:
        st.metric(
            "💰 Total AUM",
            f"${kpi_data.get('aum', 0):,.0f}",
            delta="+2.3% (Above Forecast)",
        )
    with col3:
        avg_portfolio = kpi_data.get("aum", 0) / max(kpi_data.get("num_clients", 1), 1)
        st.metric(
            "📈 Avg Portfolio",
            f"${avg_portfolio:,.0f}",
            delta="+5.7% (AI Optimized)",
        )
    with col4:
        st.metric(
            "👨‍💼 Active Advisors",
            f"{kpi_data.get('num_advisors', 0):,}",
            delta="98% Productivity Score",
        )
    with col5:
        ytd_growth = kpi_data.get("ytd_growth_pct")
        if ytd_growth is not None:
            st.metric(
                "📈 YTD Growth",
                f"{ytd_growth*100:.1f}%",
                delta="Cortex Forecast: +8.2%",
            )
        else:
            st.metric("🎯 AI Confidence", "94.7%", delta="+2.1%")

st.divider()

# AI-Powered Priority Intelligence as 4 tiles
st.markdown("### 🚨 **AI-Powered Priority Intelligence**")

# Create 4 equal-width tiles
tile1, tile2, tile3, tile4 = st.columns(4)

with tile1:
    with st.container():
        st.markdown(
            '<div style="background: linear-gradient(135deg, #ff4444, #ff6b6b); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px;">',
            unsafe_allow_html=True,
        )
        st.markdown("### 🔴 **Critical Alerts**")
        st.markdown("**7 Items**")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
        **🚨 Immediate Action Required:**
        • Portfolio concentration breaches (3)
        • Suitability drift alerts (2)
        • Large withdrawal pending ($2.3M)
        • KYC expiration (5 days)
        """
        )

with tile2:
    with st.container():
        st.markdown(
            '<div style="background: linear-gradient(135deg, #ffa500, #ffb347); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px;">',
            unsafe_allow_html=True,
        )
        st.markdown("### 🟡 **Strategic Opportunities**")
        st.markdown("**16 Items**")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
        **💡 Growth Opportunities:**
        • HNW client engagement gaps (8)
        • Portfolio rebalancing optimal (4)
        • Life event triggers (3)
        • Cash optimization ($5.2M)
        """
        )

with tile3:
    with st.container():
        st.markdown(
            '<div style="background: linear-gradient(135deg, #90ee90, #98fb98); padding: 20px; border-radius: 10px; color: #2d5a2d; text-align: center; margin-bottom: 10px;">',
            unsafe_allow_html=True,
        )
        st.markdown("### 🟢 **Performance Wins**")
        st.markdown("**342 Items**")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
        **🏆 Success Metrics:**
        • Portfolios in optimal range (89%)
        • Client satisfaction high (94.2%)
        • Compliance adherence (98.3%)
        • Revenue targets exceeded (+12%)
        """
        )

with tile4:
    with st.container():
        st.markdown(
            '<div style="background: linear-gradient(135deg, #4fc3f7, #81d4fa); padding: 20px; border-radius: 10px; color: white; text-align: center; margin-bottom: 10px;">',
            unsafe_allow_html=True,
        )
        st.markdown("### 🔵 **AI Insights**")
        st.markdown("**Real-time**")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
        **🧠 Cortex Intelligence:**
        • Market sentiment: Positive (+0.73)
        • Ultra HNW growth (+12.7%)
        • Advisor productivity (+15%)
        • Revenue forecast: $3.2M opportunity
        """
        )

st.divider()

# AI-Enhanced Business Intelligence
st.markdown("### 📊 **AI-Enhanced Business Intelligence**")

intelligence_col1, intelligence_col2, intelligence_col3 = st.columns(3)

with intelligence_col1:
    st.markdown("**🎯 Smart Actions (Next 24 Hours)**")
    if st.button("🤖 Generate AI Action Plan", use_container_width=True):
        st.success("✅ AI Action Plan Generated!")
        st.markdown(
            """
        **Priority 1**: Contact 3 high-risk churn clients
        **Priority 2**: Execute portfolio rebalancing (Auto-approved)
        **Priority 3**: Deploy cash sweep campaigns (AI-optimized)
        """
        )

with intelligence_col2:
    st.markdown("**📊 Cortex Analytics Digest**")
    if st.button("📈 Run Daily AI Analysis", use_container_width=True):
        st.info("📋 Daily Intelligence Report Ready!")
        st.markdown(
            """
        **Market Trends**: Equities outperforming (+3.2%)
        **Client Behavior**: Increased trading activity (+15%)
        **Risk Factors**: Weather-related concerns in FL/CA
        """
        )

with intelligence_col3:
    st.markdown("**🚀 Predictive Insights**")
    if st.button("🔮 Generate Forecasts", use_container_width=True):
        st.success("🎁 AI Predictions Updated!")
        st.markdown(
            """
        **Q4 Forecast**: +6.2% AUM growth (85% confidence)
        **Churn Risk**: 12 clients requiring intervention
        **Revenue Opportunity**: $3.2M from optimization
        """
        )

# Advanced Cortex AI Demonstrations
st.divider()
st.markdown("### 🧠 **Live Cortex AI Demonstrations**")

demo_col1, demo_col2 = st.columns(2)

with demo_col1:
    # AI_COMPLETE simulation
    st.markdown("**🤖 AI_COMPLETE: Natural Language Insights**")

    user_question = st.text_input(
        "Ask Cortex AI about your business:",
        value="What are the top 3 risks in my portfolio right now?",
        help="Try: 'Which clients should I contact today?' or 'Summarize market performance'",
    )

    if st.button("🧠 Ask Cortex AI", use_container_width=True):
        # Simulate AI_COMPLETE response
        ai_responses = {
            "What are the top 3 risks in my portfolio right now?": """
            **Risk Analysis (Cortex AI):**
            1. **Concentration Risk**: 3 portfolios exceed 30% single-asset allocation
            2. **Suitability Drift**: 2 conservative clients in aggressive strategies
            3. **Liquidity Risk**: $12M in illiquid positions during volatile period
            """,
            "Which clients should I contact today?": """
            **Priority Outreach (Cortex AI):**
            1. **Sarah Chen** - Life event trigger (new baby)
            2. **Michael Torres** - 187 days since last contact
            3. **Jennifer Wu** - Portfolio down 8.3%, needs reassurance
            """,
            "Summarize market performance": """
            **Market Summary (Cortex AI):**
            - **Equities**: +5.7% YTD, momentum building
            - **Fixed Income**: Stable amid rate uncertainties
            - **Alternative Assets**: Outperforming at +8.2%
            """,
        }

        response = ai_responses.get(
            user_question,
            """
        **Cortex AI Analysis:**
        Based on current data patterns, I recommend focusing on client engagement
        and portfolio optimization. Key metrics show positive momentum with selective
        opportunities for immediate action.
        """,
        )

        st.success("🤖 **Cortex AI Response:**")
        st.markdown(response)

with demo_col2:
    # AI_SENTIMENT simulation
    st.markdown("**😊 AI_SENTIMENT: Client Feedback Analysis**")

    sample_feedback = st.text_area(
        "Analyze client feedback sentiment:",
        value="The new portfolio recommendations have been fantastic! My advisor really understands my goals and the returns have exceeded expectations. Very satisfied with the service.",
        height=100,
    )

    if st.button("🎭 Analyze Sentiment", use_container_width=True):
        # Simulate AI_SENTIMENT analysis
        sentiment_score = 0.87  # Positive sentiment

        if sentiment_score > 0.5:
            st.success(f"😊 **Positive Sentiment**: {sentiment_score:.2f}")
            st.markdown(
                "**Key Themes**: Satisfaction, Trust, Performance, Service Quality"
            )
        elif sentiment_score < -0.5:
            st.error(f"😞 **Negative Sentiment**: {sentiment_score:.2f}")
        else:
            st.info(f"😐 **Neutral Sentiment**: {sentiment_score:.2f}")

# Cortex-Powered Visualizations
st.divider()
st.markdown("### 📈 **AI-Enhanced Visual Analytics**")

viz_col1, viz_col2 = st.columns(2)

with viz_col1:
    # AI-optimized AUM growth trend
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="M")
    aum_trend = pd.DataFrame(
        {
            "Month": dates,
            "AUM": [850 + i * 15 + np.random.normal(0, 5) for i in range(len(dates))],
            "AI_Forecast": [
                850 + i * 17 + 2 for i in range(len(dates))
            ],  # AI prediction
        }
    )

    fig_trend = px.line(
        aum_trend,
        x="Month",
        y=["AUM", "AI_Forecast"],
        title="📈 AUM Growth: Actual vs AI Forecast",
        labels={"value": "AUM ($ Millions)", "variable": "Data Type"},
    )
    fig_trend.update_traces(line=dict(dash="dash"), selector=dict(name="AI_Forecast"))
    st.plotly_chart(fig_trend, use_container_width=True)

with viz_col2:
    # AI-classified client segments
    customer_data = get_customer_360_segments()
    segments_df = customer_data["segments"]
    if not segments_df.empty:
        segment_counts = segments_df["WEALTH_SEGMENT"].value_counts()
        fig_segments = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="🎯 AI-Optimized Client Segmentation",
        )
        st.plotly_chart(fig_segments, use_container_width=True)

# Cortex AI Performance Metrics
st.divider()
st.markdown("### 🚀 **Cortex AI Performance Dashboard**")

ai_metrics_col1, ai_metrics_col2, ai_metrics_col3, ai_metrics_col4 = st.columns(4)

with ai_metrics_col1:
    st.metric("🤖 AI Accuracy", "94.7%", delta="+2.1%")
    st.caption("Model prediction accuracy")

with ai_metrics_col2:
    st.metric("⚡ Response Time", "1.2s", delta="-0.3s")
    st.caption("Average Cortex query time")

with ai_metrics_col3:
    st.metric("🎯 Recommendations", "247", delta="+23 today")
    st.caption("AI-generated insights")

with ai_metrics_col4:
    st.metric("💰 AI-Driven Revenue", "$3.2M", delta="+12%")
    st.caption("Revenue from AI optimization")

# Footer navigation
st.divider()
st.markdown(
    """
### 🧭 **Demo Navigation Flow**
- **Next**: 🧠 AI-Powered Insights - Deep dive into Cortex AI capabilities
- **Then**: 📊 Analytics Deep Dive - Advanced portfolio analytics
- **Final**: ⚡ Real-Time Intelligence & 🚀 Advanced Capabilities
"""
)
