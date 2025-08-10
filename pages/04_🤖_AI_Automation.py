"""
AI & Automation - GenAI features, sentiment, recommendations

This page provides AI-powered features including wealth narrative generation,
KYC operations copilot, and automated client briefing capabilities.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_functions import generate_wealth_narrative, get_kyc_insights

st.set_page_config(page_title="AI & Automation", page_icon="🤖", layout="wide")

# Page header
st.markdown("# 🤖 AI & Automation")
st.caption(
    "🧠 **Advanced AI-powered features for wealth management automation and insights**"
)

# Sub-navigation within AI & Automation
ai_subtabs = st.tabs(
    ["🤖 Wealth Narrative", "📋 KYC Copilot", "🧠 AI Insights", "🎯 Recommendations"]
)

# Wealth Narrative & Client Briefing
with ai_subtabs[0]:
    st.markdown("### 🤖 Wealth Narrative & Client Briefing")
    st.caption(
        "Auto-generate client summaries & talking points | KPIs: Prep time saved, call quality score"
    )

    # Client Selection
    st.markdown("**👤 Select Client for AI Briefing**")
    client_id = st.text_input(
        "Enter Client ID:",
        value="C001",
        help="Enter a client ID to generate AI-powered briefing",
    )

    if st.button("🧠 Generate AI Briefing", type="primary"):
        if client_id:
            narrative_data = generate_wealth_narrative(client_id)

            # Client overview
            overview_df = narrative_data["overview"]
            if not overview_df.empty:
                client_info = overview_df.iloc[0]
                st.subheader(
                    f"👤 Client Profile: {client_info['FIRST_NAME']} {client_info['LAST_NAME']}"
                )

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Risk Tolerance", client_info["RISK_TOLERANCE"])
                col2.metric(
                    "Net Worth",
                    (
                        f"${client_info['NET_WORTH_ESTIMATE']:,.0f}"
                        if pd.notna(client_info["NET_WORTH_ESTIMATE"])
                        else "N/A"
                    ),
                )
                col3.metric("Portfolios", client_info["NUM_PORTFOLIOS"])
                col4.metric("Advisors", client_info["NUM_ADVISORS"])

                # AI-Generated talking points (simulated)
                st.subheader("🤖 AI-Generated Talking Points")
                talking_points = [
                    f"• Risk profile alignment: Client has {client_info['RISK_TOLERANCE']} risk tolerance with {client_info['NUM_PORTFOLIOS']} portfolio(s)",
                    (
                        f"• Wealth positioning: Estimated net worth of ${client_info['NET_WORTH_ESTIMATE']:,.0f}"
                        if pd.notna(client_info["NET_WORTH_ESTIMATE"])
                        else "• Wealth positioning: Net worth estimate not available"
                    ),
                    (
                        f"• Life events: {client_info['LIFE_EVENT']} on {client_info['LIFE_EVENT_DATE']}"
                        if pd.notna(client_info["LIFE_EVENT"])
                        else "• Life events: No recent life events recorded"
                    ),
                ]
                for point in talking_points:
                    st.write(point)

                # AI Recommendations
                st.subheader("🎯 AI-Powered Recommendations")
                st.info("**Strategic Recommendations:**")
                st.markdown(
                    """
                - **Portfolio Optimization**: Consider rebalancing based on current market conditions
                - **Risk Assessment**: Review risk tolerance alignment quarterly
                - **Growth Opportunities**: Explore alternative investment options for diversification
                - **Communication Strategy**: Schedule quarterly reviews to maintain engagement
                """
                )

            # Portfolio summary
            portfolios_df = narrative_data["portfolios"]
            if not portfolios_df.empty:
                st.subheader("💼 Portfolio Summary")
                st.dataframe(portfolios_df, use_container_width=True)

                # Portfolio visualization
                if len(portfolios_df) > 1:
                    fig = px.pie(
                        portfolios_df,
                        values="CURRENT_VALUE",
                        names="STRATEGY_TYPE",
                        title="Portfolio Allocation by Strategy",
                    )
                    st.plotly_chart(fig, use_container_width=True)

            # AI Conversation Starters
            st.subheader("💬 AI-Generated Conversation Starters")
            conversation_starters = [
                "How are you feeling about the current market volatility and its impact on your portfolio?",
                "Have there been any changes in your financial goals since our last conversation?",
                "Would you like to discuss any upcoming major expenses or life changes?",
                "Are you satisfied with your current investment performance and risk level?",
            ]

            for i, starter in enumerate(conversation_starters, 1):
                st.markdown(f"**{i}.** {starter}")

        else:
            st.warning("Please enter a valid Client ID")

    # AI Features Overview
    st.divider()
    st.markdown("### 🧠 **AI Capabilities Overview**")

    col1, col2 = st.columns(2)
    with col1:
        st.info(
            """
        **🤖 Current AI Features:**
        - Auto-generated client summaries
        - Risk profile analysis
        - Portfolio performance insights
        - Conversation starters
        - Strategic recommendations
        """
        )

    with col2:
        st.success(
            """
        **🚀 Planned AI Enhancements:**
        - Natural language querying
        - Predictive analytics
        - Automated report generation
        - Voice-to-text meeting notes
        - Real-time market sentiment
        """
        )

# KYC Operations Copilot
with ai_subtabs[1]:
    st.markdown("### 📋 KYB/KYC Operations Copilot")
    st.caption("Speed up checks & documentation Q&A | KPIs: Cycle time, touchless rate")

    kyc_insights = get_kyc_insights()
    if not kyc_insights.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**📋 KYC Compliance Status**")
            st.dataframe(kyc_insights, use_container_width=True)

        with col2:
            # Priority distribution
            priority_counts = kyc_insights["PRIORITY"].value_counts()
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="KYC Priority Distribution",
                color_discrete_map={
                    "High": "#FF4444",
                    "Medium": "#FFA500",
                    "Low": "#90EE90",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

        # Compliance status analysis
        st.markdown("**📊 Compliance Status Breakdown**")
        status_counts = kyc_insights["COMPLIANCE_STATUS"].value_counts()
        fig2 = px.bar(
            x=status_counts.index,
            y=status_counts.values,
            title="KYC Compliance Status Distribution",
            color=status_counts.index,
        )
        st.plotly_chart(fig2, use_container_width=True)

        # AI Copilot simulation
        st.subheader("🤖 AI-Powered Document Analysis")
        st.info(
            """
        **KYC Copilot Ready** - Upload client documents for instant analysis:
        • Document completeness check
        • Risk indicator extraction
        • Compliance gap identification
        • Auto-generated review summaries
        """
        )

        # High priority items
        high_priority = kyc_insights[kyc_insights["PRIORITY"] == "High"]
        if not high_priority.empty:
            st.markdown("**🚨 High Priority KYC Items**")
            st.error(
                f"Found {len(high_priority)} clients requiring immediate KYC attention"
            )
            st.dataframe(
                high_priority[
                    [
                        "CLIENT_ID",
                        "FIRST_NAME",
                        "LAST_NAME",
                        "COMPLIANCE_STATUS",
                        "DAYS_SINCE_UPDATE",
                    ]
                ],
                use_container_width=True,
            )

    else:
        st.success("✅ All clients are up to date with KYC requirements.")

# AI Insights Dashboard
with ai_subtabs[2]:
    st.markdown("### 🧠 AI Insights & Analytics")

    # Simulated AI metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("🤖 AI Recommendations", "127", delta="+23 this week")
    col2.metric("📊 Automated Reports", "89%", delta="+5% efficiency")
    col3.metric("⏱️ Time Saved", "47 hours", delta="Per week")
    col4.metric("🎯 Accuracy Rate", "94.2%", delta="+2.1%")

    # AI Usage Analytics
    st.markdown("**📈 AI Feature Usage Analytics**")

    # Simulated usage data
    ai_usage_data = pd.DataFrame(
        {
            "Feature": [
                "Wealth Narrative",
                "KYC Copilot",
                "Risk Analysis",
                "Client Briefing",
                "Document Review",
            ],
            "Usage_Count": [156, 89, 234, 198, 67],
            "Success_Rate": [94.2, 87.5, 91.8, 96.1, 88.9],
            "Time_Saved_Hours": [23.4, 15.7, 31.2, 28.9, 8.3],
        }
    )

    col1, col2 = st.columns(2)

    with col1:
        fig1 = px.bar(
            ai_usage_data,
            x="Feature",
            y="Usage_Count",
            title="AI Feature Usage (This Month)",
            labels={"Usage_Count": "Number of Uses"},
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        fig2 = px.bar(
            ai_usage_data,
            x="Feature",
            y="Time_Saved_Hours",
            title="Time Saved by AI Features (Hours)",
            labels={"Time_Saved_Hours": "Hours Saved"},
        )
        st.plotly_chart(fig2, use_container_width=True)

    # AI Performance Metrics
    st.markdown("**🎯 AI Performance Metrics**")
    st.dataframe(ai_usage_data, use_container_width=True, hide_index=True)

    # AI Feedback and Learning
    st.markdown("**📚 AI Learning & Feedback**")
    feedback_col1, feedback_col2 = st.columns(2)

    with feedback_col1:
        st.info(
            """
        **🎓 Continuous Learning:**
        - Model training on new data patterns
        - User feedback integration
        - Performance optimization
        - Accuracy improvements
        """
        )

    with feedback_col2:
        st.success(
            """
        **📊 Recent Improvements:**
        - 12% increase in recommendation accuracy
        - 25% faster document processing
        - Enhanced natural language understanding
        - Better risk prediction models
        """
        )

# AI Recommendations Engine
with ai_subtabs[3]:
    st.markdown("### 🎯 AI Recommendations Engine")

    # Global AI Recommendations
    st.markdown("**🧠 AI-Powered Business Insights**")

    recommendations = [
        {
            "category": "Portfolio Optimization",
            "recommendation": "Consider rebalancing 23 portfolios showing significant drift from target allocations",
            "impact": "High",
            "confidence": "94%",
            "action": "Schedule rebalancing reviews",
        },
        {
            "category": "Client Engagement",
            "recommendation": "15 high-value clients haven't been contacted in 90+ days",
            "impact": "High",
            "confidence": "97%",
            "action": "Initiate outreach campaigns",
        },
        {
            "category": "Risk Management",
            "recommendation": "7 portfolios show suitability misalignment with client risk tolerance",
            "impact": "Critical",
            "confidence": "91%",
            "action": "Immediate risk assessment",
        },
        {
            "category": "Revenue Optimization",
            "recommendation": "$47M in idle cash could generate additional $1.8M annually",
            "impact": "High",
            "confidence": "89%",
            "action": "Implement cash sweep programs",
        },
    ]

    for rec in recommendations:
        with st.expander(f"{rec['category']} - {rec['impact']} Impact", expanded=True):
            col1, col2, col3 = st.columns([3, 1, 1])

            with col1:
                st.markdown(f"**Recommendation:** {rec['recommendation']}")
                st.markdown(f"**Suggested Action:** {rec['action']}")

            with col2:
                if rec["impact"] == "Critical":
                    st.error(f"Impact: {rec['impact']}")
                elif rec["impact"] == "High":
                    st.warning(f"Impact: {rec['impact']}")
                else:
                    st.info(f"Impact: {rec['impact']}")

            with col3:
                st.metric("Confidence", rec["confidence"])

    # AI Action Center
    st.markdown("**⚡ AI Action Center**")

    action_col1, action_col2, action_col3 = st.columns(3)

    with action_col1:
        if st.button("🚀 Execute High-Priority Actions", use_container_width=True):
            st.success("✅ High-priority actions queued for execution!")

    with action_col2:
        if st.button("📊 Generate AI Report", use_container_width=True):
            st.success("✅ AI-powered report generated!")

    with action_col3:
        if st.button("🔄 Refresh AI Insights", use_container_width=True):
            st.success("✅ AI insights refreshed!")

# AI Summary
st.divider()
st.markdown("### 📋 **AI & Automation Summary**")

summary_col1, summary_col2, summary_col3 = st.columns(3)

with summary_col1:
    st.markdown("#### 🤖 **AI Utilization**")
    st.metric("Active AI Features", "12")
    st.metric("Weekly Usage", "1,247 actions")
    st.metric("Automation Rate", "89%")

with summary_col2:
    st.markdown("#### ⏱️ **Efficiency Gains**")
    st.metric("Time Saved (Weekly)", "47 hours")
    st.metric("Cost Reduction", "23%")
    st.metric("Accuracy Improvement", "+12%")

with summary_col3:
    st.markdown("#### 🎯 **Impact Metrics**")
    st.metric("Client Satisfaction", "+8.7%")
    st.metric("Advisor Productivity", "+15%")
    st.metric("Compliance Rate", "98.2%")
