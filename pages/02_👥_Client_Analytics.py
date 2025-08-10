"""
Client Analytics - Customer insights, churn, outreach, sentiment

This page provides comprehensive client insights including customer 360,
next best actions, churn prevention, event outreach, and sentiment analysis.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import plotly.express as px
import streamlit as st

from utils.data_functions import (
    get_churn_early_warning,
    get_customer_360_segments,
    get_event_driven_opportunities,
    get_next_best_actions,
    get_sentiment_analysis,
)

st.set_page_config(page_title="Client Analytics", page_icon="👥", layout="wide")

# Page header
st.markdown("# 👥 Client Analytics & Relationship Management")
st.caption(
    "🎯 **Comprehensive client insights: segmentation, churn prediction, outreach, and engagement analytics**"
)

# Sub-navigation within Client Analytics
client_subtabs = st.tabs(
    [
        "🎯 Customer 360",
        "🎁 Next Best Actions",
        "⚠️ Churn Prevention",
        "📅 Event Outreach",
        "💬 Sentiment & Feedback",
    ]
)

# Customer 360 & Segmentation
with client_subtabs[0]:
    st.markdown("### 🎯 Customer 360 & Segmentation")

    customer_data = get_customer_360_segments()
    segments_df = customer_data["segments"]
    engagement_df = customer_data["engagement"]

    if not segments_df.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📊 Wealth Segment Distribution**")
            segment_counts = segments_df["WEALTH_SEGMENT"].value_counts()
            fig = px.pie(
                values=segment_counts.values,
                names=segment_counts.index,
                title="Client Distribution by Wealth Segment",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            if not engagement_df.empty:
                st.markdown("**📞 Engagement Patterns**")
                fig2 = px.scatter(
                    engagement_df.head(50),
                    x="DAYS_SINCE_LAST_CONTACT",
                    y="TOTAL_INTERACTIONS",
                    hover_data=["FIRST_NAME", "LAST_NAME"],
                    title="Interactions vs Days Since Last Contact",
                )
                st.plotly_chart(fig2, use_container_width=True)

        # Segment Analysis
        st.markdown("**💰 Wealth Segment Analysis**")
        segment_analysis = (
            segments_df.groupby("WEALTH_SEGMENT")
            .agg(
                {
                    "CLIENT_ID": "count",
                    "NET_WORTH_ESTIMATE": ["mean", "sum"],
                    "PORTFOLIO_VALUE": ["mean", "sum"],
                    "ANNUAL_INCOME": "mean",
                }
            )
            .round(2)
        )

        segment_analysis.columns = [
            "Client Count",
            "Avg Net Worth",
            "Total Net Worth",
            "Avg Portfolio",
            "Total Portfolio",
            "Avg Income",
        ]
        st.dataframe(segment_analysis, use_container_width=True)

        st.markdown("**💰 Top 20 Clients by Portfolio Value**")
        st.dataframe(segments_df.head(20), use_container_width=True)

    else:
        st.warning("No customer segmentation data available.")

# Next Best Actions
with client_subtabs[1]:
    st.markdown("### 🎁 Next Best Action - Cross/Upsell Recommendations")

    next_best_actions = get_next_best_actions()
    if not next_best_actions.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**🎯 Personalized Recommendations**")
            st.dataframe(next_best_actions, use_container_width=True)

        with col2:
            # Action type distribution
            action_counts = next_best_actions["RECOMMENDED_ACTION"].value_counts()
            fig = px.pie(
                values=action_counts.values,
                names=action_counts.index,
                title="Recommendation Types",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Priority distribution
            priority_counts = next_best_actions["PRIORITY"].value_counts()
            st.markdown("**📊 Priority Distribution**")
            col_high, col_med, col_low = st.columns(3)
            col_high.metric("🔴 High", priority_counts.get("High", 0))
            col_med.metric("🟡 Medium", priority_counts.get("Medium", 0))
            col_low.metric("🟢 Low", priority_counts.get("Low", 0))

        # Revenue Impact Analysis
        st.markdown("**💰 Revenue Impact Analysis**")
        fig3 = px.bar(
            next_best_actions.head(15),
            x="RECOMMENDED_ACTION",
            y="ESTIMATED_REVENUE_IMPACT",
            color="PRIORITY",
            title="Estimated Revenue Impact by Recommendation",
            color_discrete_map={
                "High": "#FF4444",
                "Medium": "#FFA500",
                "Low": "#90EE90",
            },
        )
        fig3.update_xaxes(tickangle=45)
        st.plotly_chart(fig3, use_container_width=True)

    else:
        st.info("No cross-sell/upsell opportunities identified at this time.")

# Churn Prevention
with client_subtabs[2]:
    st.markdown("### ⚠️ Churn Early Warning & Prevention")

    churn_warnings = get_churn_early_warning()
    if not churn_warnings.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**⚠️ High-Risk Clients**")
            st.dataframe(churn_warnings, use_container_width=True)

        with col2:
            # Risk level distribution
            risk_counts = churn_warnings["RISK_LEVEL"].value_counts()
            fig = px.bar(
                x=risk_counts.index,
                y=risk_counts.values,
                title="Churn Risk Distribution",
                color=risk_counts.index,
                color_discrete_map={
                    "High": "#FF4444",
                    "Medium": "#FFA500",
                    "Low": "#90EE90",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            # Risk factor analysis
            risk_factor_counts = churn_warnings["RISK_FACTOR"].value_counts()
            st.markdown("**📊 Risk Factors**")
            for factor, count in risk_factor_counts.items():
                st.markdown(f"- **{factor}**: {count} clients")

        # Intervention Recommendations
        st.markdown("**🎯 Recommended Interventions**")
        intervention_data = (
            churn_warnings.groupby(["RISK_LEVEL", "RISK_FACTOR"])
            .size()
            .reset_index(name="CLIENT_COUNT")
        )

        for _, row in intervention_data.iterrows():
            risk_level = row["RISK_LEVEL"]
            risk_factor = row["RISK_FACTOR"]
            count = row["CLIENT_COUNT"]

            if risk_level == "High":
                st.error(
                    f"🔴 **{risk_factor}** ({count} clients) - Immediate outreach required"
                )
            else:
                st.warning(
                    f"🟡 **{risk_factor}** ({count} clients) - Schedule follow-up within 30 days"
                )

    else:
        st.success("✅ No high-risk clients identified!")

# Event-Driven Outreach
with client_subtabs[3]:
    st.markdown("### 📅 Event-Driven Outreach Opportunities")

    outreach_opportunities = get_event_driven_opportunities()
    if not outreach_opportunities.empty:
        col1, col2 = st.columns([3, 1])

        with col1:
            st.markdown("**📅 Outreach Opportunities**")
            st.dataframe(outreach_opportunities, use_container_width=True)

        with col2:
            # Outreach type distribution
            outreach_counts = outreach_opportunities["OUTREACH_TYPE"].value_counts()
            fig = px.pie(
                values=outreach_counts.values,
                names=outreach_counts.index,
                title="Outreach Types",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Priority summary
            priority_counts = outreach_opportunities["PRIORITY"].value_counts()
            st.markdown("**📊 Priority Summary**")
            st.metric("🔴 High Priority", priority_counts.get("High", 0))
            st.metric("🟡 Medium Priority", priority_counts.get("Medium", 0))
            st.metric("🟢 Low Priority", priority_counts.get("Low", 0))

        # Life Event Analysis
        life_events = outreach_opportunities[
            outreach_opportunities["LIFE_EVENT"].notna()
        ]
        if not life_events.empty:
            st.markdown("**🎉 Life Event Opportunities**")
            event_counts = life_events["LIFE_EVENT"].value_counts()
            fig2 = px.bar(
                x=event_counts.values,
                y=event_counts.index,
                orientation="h",
                title="Life Events Requiring Outreach",
                labels={"x": "Number of Clients", "y": "Life Event Type"},
            )
            st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("No immediate outreach opportunities identified.")

# Sentiment Analysis
with client_subtabs[4]:
    st.markdown("### 💬 Client Sentiment & Feedback Intelligence")

    sentiment_data = get_sentiment_analysis()
    if not sentiment_data.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**💬 Recent Interactions Analysis**")
            st.dataframe(sentiment_data, use_container_width=True)

        with col2:
            # Sentiment distribution
            sentiment_counts = sentiment_data["SENTIMENT_SCORE"].value_counts()
            fig = px.bar(
                x=sentiment_counts.index,
                y=sentiment_counts.values,
                title="Sentiment Distribution",
                color=sentiment_counts.index,
                color_discrete_map={
                    "Positive": "#90EE90",
                    "Neutral": "#FFD700",
                    "Negative": "#FF6B6B",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            # Priority level analysis
            priority_counts = sentiment_data["PRIORITY_LEVEL"].value_counts()
            st.markdown("**📊 Priority Levels**")
            st.metric("🔴 High Priority", priority_counts.get("High", 0))
            st.metric("🟡 Medium Priority", priority_counts.get("Medium", 0))
            st.metric("🟢 Low Priority", priority_counts.get("Low", 0))

        # Negative Sentiment Alerts
        negative_sentiment = sentiment_data[
            sentiment_data["SENTIMENT_SCORE"] == "Negative"
        ]
        if not negative_sentiment.empty:
            st.markdown("**🚨 Negative Sentiment Alerts**")
            st.error(
                f"Found {len(negative_sentiment)} interactions with negative sentiment requiring immediate attention"
            )
            st.dataframe(
                negative_sentiment[
                    [
                        "CLIENT_ID",
                        "FIRST_NAME",
                        "LAST_NAME",
                        "TIMESTAMP",
                        "OUTCOME_NOTES",
                    ]
                ],
                use_container_width=True,
            )

        # Channel Analysis
        channel_sentiment = (
            sentiment_data.groupby(["CHANNEL", "SENTIMENT_SCORE"])
            .size()
            .unstack(fill_value=0)
        )
        if not channel_sentiment.empty:
            st.markdown("**📞 Sentiment by Communication Channel**")
            fig3 = px.bar(
                channel_sentiment,
                title="Sentiment Distribution by Channel",
                color_discrete_map={
                    "Positive": "#90EE90",
                    "Neutral": "#FFD700",
                    "Negative": "#FF6B6B",
                },
            )
            st.plotly_chart(fig3, use_container_width=True)

    else:
        st.info("Sentiment analysis data not available.")

# Summary and Actions
st.divider()
st.markdown("### 📋 **Client Analytics Summary & Action Items**")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### 🎯 **Segmentation Insights**")
    if not segments_df.empty:
        total_clients = len(segments_df)
        hnw_clients = len(
            segments_df[
                segments_df["WEALTH_SEGMENT"].isin(["Ultra HNW", "Very HNW", "HNW"])
            ]
        )
        st.metric("Total Clients", f"{total_clients:,}")
        st.metric("HNW+ Clients", f"{hnw_clients:,}")
        st.metric("HNW+ Percentage", f"{hnw_clients/total_clients*100:.1f}%")

with col2:
    st.markdown("#### ⚠️ **Risk Summary**")
    if not churn_warnings.empty:
        high_risk = len(churn_warnings[churn_warnings["RISK_LEVEL"] == "High"])
        medium_risk = len(churn_warnings[churn_warnings["RISK_LEVEL"] == "Medium"])
        st.metric("High Risk Clients", high_risk, delta="Immediate action needed")
        st.metric("Medium Risk Clients", medium_risk, delta="Follow-up required")

with col3:
    st.markdown("#### 🎯 **Opportunities**")
    if not next_best_actions.empty:
        high_value_opportunities = len(
            next_best_actions[next_best_actions["PRIORITY"] == "High"]
        )
        potential_revenue = next_best_actions["ESTIMATED_REVENUE_IMPACT"].sum()
        st.metric("High-Value Opportunities", high_value_opportunities)
        st.metric("Potential Revenue", f"${potential_revenue:,.0f}")
