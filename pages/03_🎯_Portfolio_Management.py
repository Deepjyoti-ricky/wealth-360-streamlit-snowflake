"""
Portfolio Management - Risk, drift, rebalancing, cash management

This page provides comprehensive portfolio analytics including suitability alerts,
drift analysis, idle cash management, and transaction anomaly detection.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import plotly.express as px
import streamlit as st

from utils.data_functions import (
    get_advisor_productivity,
    get_idle_cash_analysis,
    get_portfolio_drift_analysis,
    get_suitability_risk_alerts,
    get_trade_fee_anomalies,
)

st.set_page_config(page_title="Portfolio Management", page_icon="🎯", layout="wide")

# Page header
st.markdown("# 🎯 Portfolio Management & Risk Analytics")
st.caption(
    "📊 **Comprehensive portfolio analytics: risk monitoring, drift analysis, and performance optimization**"
)

# Sub-navigation within Portfolio Management
portfolio_subtabs = st.tabs(
    [
        "⚖️ Suitability & Risk",
        "📊 Portfolio Drift",
        "💰 Idle Cash Management",
        "🔍 Transaction Anomalies",
        "👥 Advisor Performance",
    ]
)

# Suitability & Risk Alerts
with portfolio_subtabs[0]:
    st.markdown("### ⚖️ Suitability & Risk Drift Alerts")
    st.caption(
        "Ensure portfolio aligns to client risk tolerance | KPIs: Suitability breaches, time-to-remediate"
    )

    suitability_alerts = get_suitability_risk_alerts()
    if not suitability_alerts.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**⚠️ Risk Misalignment Alerts**")
            st.dataframe(suitability_alerts, use_container_width=True)

        with col2:
            # Alert level distribution
            alert_counts = suitability_alerts["ALERT_LEVEL"].value_counts()
            fig = px.pie(
                values=alert_counts.values,
                names=alert_counts.index,
                title="Alert Level Distribution",
                color_discrete_map={
                    "High": "#FF4444",
                    "Medium": "#FFA500",
                    "Low": "#90EE90",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            # Summary metrics
            st.markdown("**📊 Risk Summary**")
            high_alerts = len(
                suitability_alerts[suitability_alerts["ALERT_LEVEL"] == "High"]
            )
            medium_alerts = len(
                suitability_alerts[suitability_alerts["ALERT_LEVEL"] == "Medium"]
            )
            st.metric("🔴 High Priority", high_alerts, delta="Immediate action")
            st.metric("🟡 Medium Priority", medium_alerts, delta="Review required")

        # Alignment Analysis
        st.markdown("**📊 Risk Alignment Analysis**")
        alignment_analysis = (
            suitability_alerts.groupby(["ALIGNMENT_STATUS", "ALERT_LEVEL"])
            .agg({"TOTAL_PORTFOLIO_VALUE": ["count", "sum", "mean"]})
            .round(2)
        )
        alignment_analysis.columns = ["Portfolio Count", "Total Value", "Avg Value"]
        st.dataframe(alignment_analysis, use_container_width=True)

        # Top Misaligned Portfolios
        st.markdown("**🎯 Top Priority Portfolios for Review**")
        top_misaligned = suitability_alerts.nlargest(10, "TOTAL_PORTFOLIO_VALUE")
        fig2 = px.bar(
            top_misaligned,
            x="PORTFOLIO_ID",
            y="TOTAL_PORTFOLIO_VALUE",
            color="ALIGNMENT_STATUS",
            title="Top 10 Misaligned Portfolios by Value",
            labels={"TOTAL_PORTFOLIO_VALUE": "Portfolio Value ($)"},
        )
        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.success("✅ All portfolios are aligned with client risk tolerance!")

# Portfolio Drift Analysis
with portfolio_subtabs[1]:
    st.markdown("### 📊 Portfolio Drift & Rebalancing")
    st.caption(
        "Alert on asset-class drift vs strategy | KPIs: Drift % over threshold, rebalance yield"
    )

    drift_analysis = get_portfolio_drift_analysis()
    if not drift_analysis.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**📊 Portfolio Drift Analysis**")
            st.dataframe(drift_analysis, use_container_width=True)

        with col2:
            # Drift level distribution
            drift_counts = drift_analysis["DRIFT_LEVEL"].value_counts()
            fig = px.bar(
                x=drift_counts.index,
                y=drift_counts.values,
                title="Drift Level Distribution",
                color=drift_counts.index,
                color_discrete_map={
                    "High": "#FF4444",
                    "Medium": "#FFA500",
                    "Low": "#90EE90",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

        # Asset Class Drift Analysis
        st.markdown("**📈 Asset Class Drift Patterns**")
        asset_drift = (
            drift_analysis.groupby("ASSET_CLASS")
            .agg({"DRIFT_PCT": ["mean", "max", "count"], "CURRENT_VALUE": "sum"})
            .round(2)
        )
        asset_drift.columns = [
            "Avg Drift %",
            "Max Drift %",
            "Portfolio Count",
            "Total Value",
        ]
        st.dataframe(asset_drift, use_container_width=True)

        # Drift vs Target Visualization
        fig3 = px.scatter(
            drift_analysis,
            x="TARGET_PCT",
            y="CURRENT_PCT",
            size="CURRENT_VALUE",
            color="ASSET_CLASS",
            hover_data=["PORTFOLIO_ID", "STRATEGY_TYPE"],
            title="Current vs Target Asset Allocation",
            labels={"TARGET_PCT": "Target %", "CURRENT_PCT": "Current %"},
        )
        # Add diagonal line for perfect alignment
        fig3.add_shape(
            type="line",
            x0=0,
            y0=0,
            x1=100,
            y1=100,
            line=dict(color="red", dash="dash"),
            name="Perfect Alignment",
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Rebalancing Recommendations
        high_drift = drift_analysis[drift_analysis["DRIFT_LEVEL"] == "High"]
        if not high_drift.empty:
            st.markdown("**🎯 Immediate Rebalancing Required**")
            st.error(
                f"Found {len(high_drift)} portfolios with high drift requiring immediate rebalancing"
            )
            st.dataframe(
                high_drift[
                    [
                        "PORTFOLIO_ID",
                        "STRATEGY_TYPE",
                        "ASSET_CLASS",
                        "CURRENT_PCT",
                        "TARGET_PCT",
                        "DRIFT_PCT",
                    ]
                ],
                use_container_width=True,
            )

    else:
        st.success("✅ All portfolios are within acceptable drift thresholds!")

# Idle Cash Management
with portfolio_subtabs[2]:
    st.markdown("### 💰 Idle Cash & Cash-Sweep Analysis")
    st.caption("Monetize idle balances | KPIs: Cash ratio, NII uplift")

    idle_cash = get_idle_cash_analysis()
    if not idle_cash.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**💰 Idle Cash Opportunities**")
            st.dataframe(idle_cash, use_container_width=True)

        with col2:
            # Sweep priority distribution
            priority_counts = idle_cash["SWEEP_PRIORITY"].value_counts()
            fig = px.pie(
                values=priority_counts.values,
                names=priority_counts.index,
                title="Cash Sweep Priority",
                color_discrete_map={
                    "High Priority": "#FF4444",
                    "Medium Priority": "#FFA500",
                    "Low Priority": "#90EE90",
                    "Acceptable": "#87CEEB",
                },
            )
            st.plotly_chart(fig, use_container_width=True)

            # Summary metrics
            total_idle_cash = idle_cash["CASH_BALANCE"].sum()
            potential_income = idle_cash["POTENTIAL_ANNUAL_INCOME"].sum()
            st.metric("💰 Total Idle Cash", f"${total_idle_cash:,.0f}")
            st.metric("📈 Potential Income", f"${potential_income:,.0f}")

        # Cash Analysis by Portfolio Strategy
        st.markdown("**📊 Cash Analysis by Strategy Type**")
        strategy_analysis = (
            idle_cash.groupby("STRATEGY_TYPE")
            .agg(
                {
                    "CASH_BALANCE": ["count", "sum", "mean"],
                    "CASH_PERCENTAGE": "mean",
                    "POTENTIAL_ANNUAL_INCOME": "sum",
                }
            )
            .round(2)
        )
        strategy_analysis.columns = [
            "Portfolio Count",
            "Total Cash",
            "Avg Cash",
            "Avg Cash %",
            "Potential Income",
        ]
        st.dataframe(strategy_analysis, use_container_width=True)

        # Cash vs Portfolio Size Analysis
        fig2 = px.scatter(
            idle_cash,
            x="TOTAL_PORTFOLIO_VALUE",
            y="CASH_BALANCE",
            size="CASH_PERCENTAGE",
            color="SWEEP_PRIORITY",
            hover_data=["CLIENT_ID", "FIRST_NAME", "LAST_NAME"],
            title="Cash Balance vs Portfolio Size",
            labels={
                "TOTAL_PORTFOLIO_VALUE": "Portfolio Value ($)",
                "CASH_BALANCE": "Cash Balance ($)",
            },
        )
        st.plotly_chart(fig2, use_container_width=True)

        # High Priority Cash Sweep
        high_priority = idle_cash[idle_cash["SWEEP_PRIORITY"] == "High Priority"]
        if not high_priority.empty:
            st.markdown("**🚨 High Priority Cash Sweep Opportunities**")
            st.warning(f"Found {len(high_priority)} portfolios with high cash balances")
            total_high_priority_cash = high_priority["CASH_BALANCE"].sum()
            potential_high_priority_income = high_priority[
                "POTENTIAL_ANNUAL_INCOME"
            ].sum()

            col_cash, col_income = st.columns(2)
            col_cash.metric("High Priority Cash", f"${total_high_priority_cash:,.0f}")
            col_income.metric(
                "Potential Annual Income", f"${potential_high_priority_income:,.0f}"
            )

    else:
        st.success("✅ No significant idle cash balances identified!")

# Transaction Anomalies
with portfolio_subtabs[3]:
    st.markdown("### 🔍 Trade & Transaction Anomaly Detection")
    st.caption(
        "Catch unusual patterns and operational outliers | KPIs: Transaction integrity, operational risk detection"
    )

    anomalies_df = get_trade_fee_anomalies()
    if not anomalies_df.empty:
        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("**⚠️ Recent Transaction Anomalies**")
            st.dataframe(anomalies_df, use_container_width=True)

        with col2:
            # Anomaly type distribution
            anomaly_counts = anomalies_df["ANOMALY_TYPE"].value_counts()
            fig = px.pie(
                values=anomaly_counts.values,
                names=anomaly_counts.index,
                title="Transaction Anomaly Types",
            )
            st.plotly_chart(fig, use_container_width=True)

        # Transaction Analysis
        st.markdown("**📊 Transaction Anomaly Analysis**")
        fig2 = px.scatter(
            anomalies_df,
            x="TOTAL_AMOUNT",
            y="DEVIATION_FROM_AVG_PCT",
            color="ANOMALY_TYPE",
            size="QUANTITY",
            hover_data=["TICKER", "FIRST_NAME", "LAST_NAME"],
            title="Transaction Amount vs Deviation from Average (Anomalies Only)",
            labels={
                "TOTAL_AMOUNT": "Transaction Amount ($)",
                "DEVIATION_FROM_AVG_PCT": "Deviation from Average (%)",
            },
        )
        st.plotly_chart(fig2, use_container_width=True)

        # Anomaly Timeline
        fig3 = px.scatter(
            anomalies_df,
            x="TIMESTAMP",
            y="TOTAL_AMOUNT",
            color="ANOMALY_TYPE",
            hover_data=["TICKER", "CLIENT_ID"],
            title="Anomaly Timeline - Last 90 Days",
            labels={"TIMESTAMP": "Date", "TOTAL_AMOUNT": "Transaction Amount ($)"},
        )
        st.plotly_chart(fig3, use_container_width=True)

        # Critical Anomalies
        critical_anomalies = anomalies_df[
            anomalies_df["ANOMALY_TYPE"].isin(
                ["Unusually Large Transaction", "Statistical Outlier - High Value"]
            )
        ]
        if not critical_anomalies.empty:
            st.markdown("**🚨 Critical Anomalies Requiring Investigation**")
            st.error(f"Found {len(critical_anomalies)} critical transaction anomalies")
            st.dataframe(
                critical_anomalies[
                    [
                        "TRANSACTION_ID",
                        "CLIENT_ID",
                        "TOTAL_AMOUNT",
                        "ANOMALY_TYPE",
                        "TIMESTAMP",
                    ]
                ],
                use_container_width=True,
            )

    else:
        st.success("✅ No transaction anomalies detected in the last 90 days.")

# Advisor Performance
with portfolio_subtabs[4]:
    st.markdown("### 👥 Advisor Productivity & Coverage")
    st.caption(
        "Improve book management & cadences | KPIs: Coverage %, last-contact SLA, meetings/client"
    )

    # Get filters from session state
    advisor_window = st.session_state.get("advisor_window", 90)

    advisor_data = get_advisor_productivity(advisor_window)
    if not advisor_data.empty:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**👥 Advisor Performance Metrics**")
            st.dataframe(advisor_data, use_container_width=True)

        with col2:
            # AUM distribution by advisor
            fig = px.bar(
                advisor_data.head(10),
                x="ADVISOR_NAME",
                y="TOTAL_AUM",
                title="Top 10 Advisors by AUM",
                labels={"TOTAL_AUM": "Total AUM ($)"},
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)

        # Advisor Efficiency Analysis
        st.markdown("**📊 Advisor Efficiency Metrics**")
        efficiency_col1, efficiency_col2 = st.columns(2)

        with efficiency_col1:
            fig2 = px.scatter(
                advisor_data,
                x="TOTAL_CLIENTS",
                y="TOTAL_AUM",
                size="INTERACTIONS_PER_CLIENT",
                color="SPECIALIZATION",
                hover_data=["ADVISOR_NAME"],
                title="Clients vs AUM (Size = Interactions per Client)",
                labels={
                    "TOTAL_CLIENTS": "Number of Clients",
                    "TOTAL_AUM": "Total AUM ($)",
                },
            )
            st.plotly_chart(fig2, use_container_width=True)

        with efficiency_col2:
            fig3 = px.bar(
                advisor_data.head(10),
                x="ADVISOR_NAME",
                y="AUM_PER_CLIENT",
                title="AUM per Client by Advisor",
                labels={"AUM_PER_CLIENT": "AUM per Client ($)"},
            )
            fig3.update_xaxes(tickangle=45)
            st.plotly_chart(fig3, use_container_width=True)

        # Specialization Analysis
        st.markdown("**🎯 Performance by Specialization**")
        specialization_analysis = (
            advisor_data.groupby("SPECIALIZATION")
            .agg(
                {
                    "TOTAL_CLIENTS": ["count", "sum", "mean"],
                    "TOTAL_AUM": ["sum", "mean"],
                    "INTERACTIONS_PER_CLIENT": "mean",
                }
            )
            .round(2)
        )
        specialization_analysis.columns = [
            "Advisor Count",
            "Total Clients",
            "Avg Clients",
            "Total AUM",
            "Avg AUM",
            "Avg Interactions/Client",
        ]
        st.dataframe(specialization_analysis, use_container_width=True)

        # Top and Bottom Performers
        col_top, col_bottom = st.columns(2)

        with col_top:
            st.markdown("**🏆 Top Performers (by AUM)**")
            top_performers = advisor_data.nlargest(5, "TOTAL_AUM")[
                ["ADVISOR_NAME", "TOTAL_AUM", "TOTAL_CLIENTS"]
            ]
            st.dataframe(top_performers, use_container_width=True, hide_index=True)

        with col_bottom:
            st.markdown("**📈 Growth Opportunities (by Interactions/Client)**")
            low_engagement = advisor_data.nsmallest(5, "INTERACTIONS_PER_CLIENT")[
                ["ADVISOR_NAME", "INTERACTIONS_PER_CLIENT", "TOTAL_CLIENTS"]
            ]
            st.dataframe(low_engagement, use_container_width=True, hide_index=True)

    else:
        st.warning("No advisor performance data available.")

# Summary Dashboard
st.divider()
st.markdown("### 📋 **Portfolio Management Summary**")

summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)

with summary_col1:
    st.markdown("#### ⚖️ **Risk Alerts**")
    if not suitability_alerts.empty:
        total_alerts = len(suitability_alerts)
        high_risk_alerts = len(
            suitability_alerts[suitability_alerts["ALERT_LEVEL"] == "High"]
        )
        st.metric("Total Alerts", total_alerts)
        st.metric("High Priority", high_risk_alerts)

with summary_col2:
    st.markdown("#### 📊 **Drift Analysis**")
    if not drift_analysis.empty:
        total_drift = len(drift_analysis)
        high_drift = len(drift_analysis[drift_analysis["DRIFT_LEVEL"] == "High"])
        st.metric("Portfolios with Drift", total_drift)
        st.metric("High Drift", high_drift)

with summary_col3:
    st.markdown("#### 💰 **Cash Optimization**")
    if not idle_cash.empty:
        total_cash = idle_cash["CASH_BALANCE"].sum()
        potential_income = idle_cash["POTENTIAL_ANNUAL_INCOME"].sum()
        st.metric("Idle Cash", f"${total_cash:,.0f}")
        st.metric("Potential Income", f"${potential_income:,.0f}")

with summary_col4:
    st.markdown("#### 🔍 **Anomalies**")
    if not anomalies_df.empty:
        total_anomalies = len(anomalies_df)
        critical_count = len(
            anomalies_df[
                anomalies_df["ANOMALY_TYPE"].isin(
                    ["Unusually Large Transaction", "Statistical Outlier - High Value"]
                )
            ]
        )
        st.metric("Total Anomalies", total_anomalies)
        st.metric("Critical", critical_count)
