"""
Real-Time Intelligence - Live Monitoring and Automated Workflows

This page provides real-time monitoring dashboards, automated alerts,
and live intelligence feeds powered by Cortex AI.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st

st.set_page_config(page_title="Real-Time Intelligence", page_icon="⚡", layout="wide")

# Sidebar - Real-Time Configuration & Controls
st.sidebar.markdown("## ⚡ **Real-Time Controls**")

# Alert Management
st.sidebar.markdown("### 🚨 **Alert Management**")
auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh", value=True)
alert_frequency = st.sidebar.selectbox(
    "Alert Frequency", ["Real-time", "Every 30s", "Every 1min", "Every 5min"], index=0
)

alert_priority_filter = st.sidebar.multiselect(
    "Alert Priority Filter",
    ["🔴 Critical", "🟡 High", "🟠 Medium", "🟢 Low", "ℹ️ Info"],
    default=["🔴 Critical", "🟡 High"],
)

# Monitoring Scope
st.sidebar.markdown("### 🌍 **Monitoring Scope**")
monitoring_regions = st.sidebar.multiselect(
    "Geographic Regions",
    ["North America", "Europe", "Asia Pacific", "Latin America", "Global"],
    default=["Global"],
)

client_segments = st.sidebar.multiselect(
    "Client Segments",
    ["High Net Worth", "Ultra High Net Worth", "Institutional", "Retail", "All"],
    default=["All"],
)

# Real-Time Thresholds
st.sidebar.markdown("### ⚖️ **Real-Time Thresholds**")
risk_alert_threshold = st.sidebar.slider("Risk Alert Level", 0, 100, 75, 5)
volume_alert_threshold = st.sidebar.slider("Volume Alert (% change)", 0, 500, 150, 25)
latency_threshold = st.sidebar.slider("Latency Alert (ms)", 100, 5000, 1000, 100)

# System Performance Monitoring
st.sidebar.markdown("### 📊 **System Performance**")
system_load = st.sidebar.metric("System Load", "23%", "↘️ -2%")
active_connections = st.sidebar.metric("Active Connections", "1,247", "↗️ +89")
data_throughput = st.sidebar.metric("Data Throughput", "12.3 GB/s", "↗️ +1.2")

# Automation Controls
st.sidebar.markdown("### 🤖 **Automation Controls**")
enable_auto_response = st.sidebar.checkbox("🤖 Auto Response", value=False)
enable_smart_routing = st.sidebar.checkbox("🧠 Smart Alert Routing", value=True)
enable_predictive_alerts = st.sidebar.checkbox("🔮 Predictive Alerts", value=True)

# Emergency Controls
st.sidebar.markdown("### 🆘 **Emergency Controls**")
if st.sidebar.button("🛑 Emergency Stop", use_container_width=True, type="secondary"):
    st.sidebar.warning("Emergency protocols activated!")

if st.sidebar.button("🔄 System Reset", use_container_width=True):
    st.sidebar.success("System reset completed!")

# Live Data Export
st.sidebar.markdown("### 📤 **Live Data Export**")
if st.sidebar.button("📊 Export Live Dashboard", use_container_width=True):
    st.sidebar.success("Live dashboard exported!")

if st.sidebar.button("🚨 Export Alert Log", use_container_width=True):
    st.sidebar.success("Alert log exported!")

# Navigation
st.sidebar.markdown("### 🧭 **Navigation**")
if st.sidebar.button("📊 Analytics Deep Dive ←", use_container_width=True):
    st.switch_page("pages/03_📊_Analytics_Deep_Dive.py")

if st.sidebar.button("🚀 Advanced Capabilities →", use_container_width=True):
    st.switch_page("pages/05_🚀_Advanced_Capabilities.py")

# Custom CSS for real-time styling
st.markdown(
    """
<style>
    .realtime-card {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 20px;
        border-radius: 15px;
        color: white;
        margin: 10px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
        50% { box-shadow: 0 8px 35px rgba(0,0,0,0.25); }
        100% { box-shadow: 0 8px 25px rgba(0,0,0,0.15); }
    }
    .alert-card {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px 0;
        animation: blink 1s infinite;
    }
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.7; }
    }
    .monitor-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 15px;
        border-radius: 10px;
        color: white;
        margin: 5px 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Page header with live timestamp
current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
st.markdown(
    f"""
<div class="realtime-card">
    <h1>⚡ Real-Time Intelligence Command Center</h1>
    <h3>Live monitoring and automated workflows powered by Cortex AI</h3>
    <p style="font-size: 16px; margin-bottom: 0;">🕐 Last Updated: {current_time} | Status: 🟢 All Systems Operational</p>
</div>
""",
    unsafe_allow_html=True,
)

# Real-time dashboard tabs
realtime_tabs = st.tabs(
    [
        "🔴 Live Alerts",
        "📊 Monitoring Dashboard",
        "🗺️ Global Intelligence",
        "🤖 AI Automation",
        "⚡ Performance Center",
    ]
)

# Live Alerts Tab
with realtime_tabs[0]:
    st.markdown("### 🔴 **Live Alert Stream**")

    # Alert priority filters
    alert_col1, alert_col2, alert_col3 = st.columns([2, 1, 1])

    with alert_col1:
        alert_filter = st.multiselect(
            "Filter Alert Types:",
            ["Critical", "High", "Medium", "Low", "Info"],
            default=["Critical", "High"],
        )

    with alert_col2:
        auto_refresh = st.checkbox("🔄 Auto Refresh", value=True)

    with alert_col3:
        if st.button("🔔 Clear All", use_container_width=True):
            st.success("All alerts cleared!")

    # Live alerts feed
    @st.cache_data(ttl=30)  # Refresh every 30 seconds
    def get_live_alerts():
        np.random.seed(int(datetime.now().timestamp()) % 1000)
        alerts = []

        alert_types = [
            {
                "type": "Critical",
                "icon": "🔴",
                "msg": "Portfolio concentration breach detected",
                "client": "Sarah Chen",
                "value": "$12.3M",
            },
            {
                "type": "High",
                "icon": "🟡",
                "msg": "Large withdrawal request pending",
                "client": "Michael Torres",
                "value": "$2.8M",
            },
            {
                "type": "Critical",
                "icon": "🔴",
                "msg": "Suitability drift alert triggered",
                "client": "Dr. Jennifer Wu",
                "value": "$15.2M",
            },
            {
                "type": "Medium",
                "icon": "🟠",
                "msg": "Client engagement gap exceeded 180 days",
                "client": "Robert Kim",
                "value": "$6.8M",
            },
            {
                "type": "High",
                "icon": "🟡",
                "msg": "Risk score anomaly detected",
                "client": "Lisa Rodriguez",
                "value": "$9.4M",
            },
            {
                "type": "Info",
                "icon": "🔵",
                "msg": "Rebalancing opportunity identified",
                "client": "David Chen",
                "value": "$4.2M",
            },
        ]

        for i in range(np.random.randint(8, 15)):
            alert = np.random.choice(alert_types)
            timestamp = datetime.now() - timedelta(minutes=np.random.randint(1, 120))
            alerts.append(
                {
                    **alert,
                    "timestamp": timestamp.strftime("%H:%M:%S"),
                    "id": f"ALT_{i+1:03d}",
                }
            )

        return sorted(alerts, key=lambda x: x["timestamp"], reverse=True)

    live_alerts = get_live_alerts()

    # Display alerts
    st.markdown("**🚨 Active Alerts (Real-time Feed):**")

    for alert in live_alerts[:10]:  # Show top 10 alerts
        if alert["type"] in alert_filter:
            if alert["type"] == "Critical":
                st.markdown(
                    f"""
                <div class="alert-card">
                    <b>{alert['icon']} {alert['type'].upper()} | {alert['timestamp']}</b><br>
                    <b>Client:</b> {alert['client']} ({alert['value']})<br>
                    <b>Alert:</b> {alert['msg']}<br>
                    <b>ID:</b> {alert['id']}
                </div>
                """,
                    unsafe_allow_html=True,
                )
            else:
                priority_color = {
                    "High": "#FFA500",
                    "Medium": "#FFD700",
                    "Low": "#90EE90",
                    "Info": "#87CEEB",
                }
                st.markdown(
                    f"""
                <div style="background: {priority_color.get(alert['type'], '#gray')}; padding: 10px; border-radius: 8px; margin: 5px 0; color: white;">
                    <b>{alert['icon']} {alert['type']} | {alert['timestamp']}</b> - {alert['client']} ({alert['value']}): {alert['msg']}
                </div>
                """,
                    unsafe_allow_html=True,
                )

    if auto_refresh:
        st.rerun()

# Monitoring Dashboard Tab
with realtime_tabs[1]:
    st.markdown("### 📊 **Real-Time Monitoring Dashboard**")

    # Key metrics row
    metrics_col1, metrics_col2, metrics_col3, metrics_col4, metrics_col5 = st.columns(5)

    with metrics_col1:
        st.markdown(
            """
        <div class="monitor-card">
            <h4>🔴 Critical Alerts</h4>
            <h2>7</h2>
            <p>Last 24h: +3</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with metrics_col2:
        st.markdown(
            """
        <div class="monitor-card">
            <h4>💰 AUM at Risk</h4>
            <h2>$47M</h2>
            <p>Requires attention</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with metrics_col3:
        st.markdown(
            """
        <div class="monitor-card">
            <h4>⚡ Response Time</h4>
            <h2>1.2s</h2>
            <p>Avg system response</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with metrics_col4:
        st.markdown(
            """
        <div class="monitor-card">
            <h4>🎯 Accuracy</h4>
            <h2>94.7%</h2>
            <p>AI prediction rate</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with metrics_col5:
        st.markdown(
            """
        <div class="monitor-card">
            <h4>🚀 Automated</h4>
            <h2>89%</h2>
            <p>Process automation</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Live monitoring charts
    monitor_col1, monitor_col2 = st.columns(2)

    with monitor_col1:
        # Real-time activity feed
        @st.cache_data(ttl=10)
        def get_activity_data():
            times = [
                (datetime.now() - timedelta(minutes=i)).strftime("%H:%M")
                for i in range(30, 0, -1)
            ]
            activities = [np.random.randint(50, 200) for _ in times]
            return times, activities

        times, activities = get_activity_data()

        fig_activity = go.Figure()
        fig_activity.add_trace(
            go.Scatter(
                x=times,
                y=activities,
                mode="lines+markers",
                name="Activity Level",
                line=dict(color="#00ff41", width=3),
                marker=dict(size=6),
            )
        )
        fig_activity.update_layout(
            title="Live System Activity (30 min)",
            xaxis_title="Time",
            yaxis_title="Activity Level",
            height=400,
            plot_bgcolor="rgba(0,0,0,0.1)",
        )
        st.plotly_chart(fig_activity, use_container_width=True)

    with monitor_col2:
        # System health indicators
        health_data = {
            "Component": [
                "Database",
                "API Gateway",
                "AI Models",
                "Security",
                "Network",
            ],
            "Status": [99.9, 99.8, 98.5, 100.0, 99.2],
            "Response_Time": [12, 45, 1200, 8, 23],
        }

        fig_health = go.Figure()

        # Add status bars
        fig_health.add_trace(
            go.Bar(
                name="Uptime %",
                y=health_data["Component"],
                x=health_data["Status"],
                orientation="h",
                marker=dict(
                    color=[
                        "green" if x > 99 else "orange" if x > 95 else "red"
                        for x in health_data["Status"]
                    ]
                ),
            )
        )

        fig_health.update_layout(
            title="System Health Monitor", xaxis_title="Uptime (%)", height=400
        )
        st.plotly_chart(fig_health, use_container_width=True)

    # Live transaction monitoring
    st.markdown("**💳 Live Transaction Monitoring**")

    @st.cache_data(ttl=5)
    def get_transaction_stream():
        transactions = []
        for i in range(15):
            transaction = {
                "time": (datetime.now() - timedelta(seconds=i * 10)).strftime(
                    "%H:%M:%S"
                ),
                "type": np.random.choice(["Buy", "Sell", "Transfer", "Withdrawal"]),
                "amount": np.random.randint(1000, 50000),
                "client": np.random.choice(
                    ["Sarah C.", "Michael T.", "Jennifer W.", "Robert K.", "Lisa R."]
                ),
                "status": np.random.choice(
                    ["Completed", "Processing", "Pending"], p=[0.7, 0.2, 0.1]
                ),
            }
            transactions.append(transaction)
        return transactions

    transactions = get_transaction_stream()

    # Display as streaming table
    transaction_df = pd.DataFrame(transactions)

    # Color code by status
    def highlight_status(val):
        if val == "Completed":
            return "background-color: #90EE90"
        elif val == "Processing":
            return "background-color: #FFD700"
        else:
            return "background-color: #FFA07A"

    styled_df = transaction_df.style.applymap(highlight_status, subset=["status"])
    st.dataframe(styled_df, hide_index=True, use_container_width=True)

# Global Intelligence Map Tab
with realtime_tabs[2]:
    st.markdown("### 🗺️ **Global Intelligence Map**")

    # Map type selector
    map_type = st.selectbox(
        "Select Intelligence View:",
        [
            "🌍 Global Activity",
            "💰 Transaction Flow",
            "🚨 Risk Hotspots",
            "📈 Market Sentiment",
        ],
    )

    if map_type == "🌍 Global Activity":
        # Global activity map
        @st.cache_data
        def get_global_activity():
            np.random.seed(42)
            cities = [
                {
                    "city": "New York",
                    "lat": 40.7128,
                    "lon": -74.0060,
                    "activity": np.random.randint(80, 120),
                },
                {
                    "city": "London",
                    "lat": 51.5074,
                    "lon": -0.1278,
                    "activity": np.random.randint(60, 100),
                },
                {
                    "city": "Tokyo",
                    "lat": 35.6762,
                    "lon": 139.6503,
                    "activity": np.random.randint(70, 110),
                },
                {
                    "city": "Singapore",
                    "lat": 1.3521,
                    "lon": 103.8198,
                    "activity": np.random.randint(50, 90),
                },
                {
                    "city": "Sydney",
                    "lat": -33.8688,
                    "lon": 151.2093,
                    "activity": np.random.randint(40, 80),
                },
                {
                    "city": "Toronto",
                    "lat": 43.6532,
                    "lon": -79.3832,
                    "activity": np.random.randint(45, 85),
                },
                {
                    "city": "Frankfurt",
                    "lat": 50.1109,
                    "lon": 8.6821,
                    "activity": np.random.randint(55, 95),
                },
                {
                    "city": "Hong Kong",
                    "lat": 22.3193,
                    "lon": 114.1694,
                    "activity": np.random.randint(65, 105),
                },
            ]

            for city in cities:
                city["color"] = [
                    min(255, city["activity"] * 2),
                    100,
                    max(50, 255 - city["activity"]),
                    200,
                ]
                city["radius"] = city["activity"] * 1000

            return cities

        global_data_list = get_global_activity()

        # Convert to DataFrame
        global_df = pd.DataFrame(global_data_list)

        st.pydeck_chart(
            pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=20,
                    longitude=0,
                    zoom=1.5,
                    pitch=30,
                ),
                layers=[
                    pdk.Layer(
                        "TileLayer",
                        data="https://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
                        min_zoom=0,
                        max_zoom=19,
                        tile_size=256,
                    ),
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=global_df,
                        get_position=["lon", "lat"],
                        get_fill_color="color",
                        get_radius="radius",
                        radius_scale=50,
                        pickable=True,
                        auto_highlight=True,
                    ),
                ],
                tooltip={
                    "html": "<b>🌍 {city}</b><br/>Activity Level: {activity}",
                    "style": {"backgroundColor": "darkblue", "color": "white"},
                },
            ),
            use_container_width=True,
            height=500,
        )

        st.info(
            "🌍 **Global Activity**: Real-time client activity and system usage across major financial centers."
        )

    elif map_type == "💰 Transaction Flow":
        # Transaction flow visualization
        @st.cache_data
        def get_transaction_flows():
            flows = [
                {
                    "source_lat": 40.7128,
                    "source_lon": -74.0060,
                    "target_lat": 51.5074,
                    "target_lon": -0.1278,
                    "amount": 15000000,
                },
                {
                    "source_lat": 35.6762,
                    "source_lon": 139.6503,
                    "target_lat": 1.3521,
                    "target_lon": 103.8198,
                    "amount": 8000000,
                },
                {
                    "source_lat": 40.7128,
                    "source_lon": -74.0060,
                    "target_lat": 35.6762,
                    "target_lon": 139.6503,
                    "amount": 12000000,
                },
                {
                    "source_lat": 51.5074,
                    "source_lon": -0.1278,
                    "target_lat": 50.1109,
                    "target_lon": 8.6821,
                    "amount": 6000000,
                },
                {
                    "source_lat": 43.6532,
                    "source_lon": -79.3832,
                    "target_lat": 40.7128,
                    "target_lon": -74.0060,
                    "amount": 9000000,
                },
            ]

            for flow in flows:
                flow["color"] = (
                    [0, 255, 0, 150]
                    if flow["amount"] > 10000000
                    else [255, 255, 0, 150]
                )
                flow["width"] = flow["amount"] / 1000000

            return flows

        transaction_flows_list = get_transaction_flows()

        # Convert to DataFrame
        transaction_flows_df = pd.DataFrame(transaction_flows_list)

        st.pydeck_chart(
            pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=35,
                    longitude=0,
                    zoom=1.2,
                    pitch=40,
                ),
                layers=[
                    pdk.Layer(
                        "TileLayer",
                        data="https://c.tile.openstreetmap.org/{z}/{x}/{y}.png",
                        min_zoom=0,
                        max_zoom=19,
                        tile_size=256,
                    ),
                    pdk.Layer(
                        "ArcLayer",
                        data=transaction_flows_df,
                        get_source_position=["source_lon", "source_lat"],
                        get_target_position=["target_lon", "target_lat"],
                        get_source_color="color",
                        get_target_color="color",
                        get_width="width",
                        width_scale=1000,
                        pickable=True,
                    ),
                ],
                tooltip={
                    "html": "<b>💰 Transaction Flow</b><br/>Amount: ${amount:,.0f}",
                    "style": {"backgroundColor": "green", "color": "white"},
                },
            ),
            use_container_width=True,
            height=500,
        )

        st.success(
            "💰 **Transaction Flow**: Live capital movement and cross-border transaction patterns."
        )

# AI Automation Tab
with realtime_tabs[3]:
    st.markdown("### 🤖 **AI Automation Control Center**")

    # Automation status
    automation_col1, automation_col2, automation_col3 = st.columns(3)

    with automation_col1:
        st.markdown("**🔄 Active Automations**")
        automations = [
            "✅ Portfolio Rebalancing",
            "✅ Risk Monitoring",
            "✅ Client Alerts",
            "✅ Compliance Checks",
            "⏸️ Report Generation",
        ]
        for automation in automations:
            st.markdown(automation)

    with automation_col2:
        st.markdown("**📊 Automation Performance**")
        st.metric("🎯 Success Rate", "97.3%", delta="+1.2%")
        st.metric("⚡ Avg Processing", "2.4s", delta="-0.5s")
        st.metric("💰 Cost Savings", "$45K", delta="+$8K")

    with automation_col3:
        st.markdown("**🚀 Quick Actions**")
        if st.button("🔄 Trigger Rebalancing", use_container_width=True):
            st.success("✅ Rebalancing automation triggered!")
        if st.button("📊 Generate Reports", use_container_width=True):
            st.info("📋 Report generation started...")
        if st.button("🚨 Run Risk Scan", use_container_width=True):
            st.warning("🔍 Risk scan initiated...")

    # Automation workflow visualization
    st.markdown("**🔄 Live Automation Workflows**")

    workflow_data = {
        "Stage": [
            "Data Ingestion",
            "AI Analysis",
            "Decision Engine",
            "Action Execution",
            "Verification",
        ],
        "Status": ["✅ Complete", "⚡ Processing", "⏳ Queue", "⏸️ Pending", "📋 Ready"],
        "Processing_Time": [0.3, 1.8, 0.6, 2.1, 0.4],
        "Success_Rate": [99.9, 97.3, 98.7, 96.2, 99.1],
    }

    fig_workflow = go.Figure()

    # Add processing time bars
    fig_workflow.add_trace(
        go.Bar(
            name="Processing Time (s)",
            x=workflow_data["Stage"],
            y=workflow_data["Processing_Time"],
            yaxis="y",
            marker_color="skyblue",
        )
    )

    # Add success rate line
    fig_workflow.add_trace(
        go.Scatter(
            name="Success Rate (%)",
            x=workflow_data["Stage"],
            y=workflow_data["Success_Rate"],
            yaxis="y2",
            mode="lines+markers",
            marker_color="green",
            line=dict(width=3),
        )
    )

    fig_workflow.update_layout(
        title="Automation Pipeline Performance",
        xaxis_title="Workflow Stage",
        yaxis=dict(title="Processing Time (seconds)", side="left"),
        yaxis2=dict(title="Success Rate (%)", side="right", overlaying="y"),
        height=400,
    )

    st.plotly_chart(fig_workflow, use_container_width=True)

# Performance Center Tab
with realtime_tabs[4]:
    st.markdown("### ⚡ **Performance Center**")

    # Performance metrics grid
    perf_col1, perf_col2 = st.columns(2)

    with perf_col1:
        st.markdown("**🚀 System Performance**")

        # CPU and Memory usage
        cpu_usage = np.random.uniform(60, 85)
        memory_usage = np.random.uniform(45, 70)

        fig_resources = go.Figure()

        fig_resources.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=cpu_usage,
                domain={"x": [0, 0.48], "y": [0, 1]},
                title={"text": "CPU Usage %"},
                delta={"reference": 70},
                gauge={
                    "axis": {"range": [None, 100]},
                    "bar": {"color": "darkblue"},
                    "steps": [
                        {"range": [0, 50], "color": "lightgray"},
                        {"range": [50, 80], "color": "yellow"},
                        {"range": [80, 100], "color": "red"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 90,
                    },
                },
            )
        )

        fig_resources.add_trace(
            go.Indicator(
                mode="gauge+number+delta",
                value=memory_usage,
                domain={"x": [0.52, 1], "y": [0, 1]},
                title={"text": "Memory Usage %"},
                delta={"reference": 60},
                gauge={
                    "axis": {"range": [None, 100]},
                    "bar": {"color": "darkgreen"},
                    "steps": [
                        {"range": [0, 50], "color": "lightgray"},
                        {"range": [50, 80], "color": "yellow"},
                        {"range": [80, 100], "color": "red"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 90,
                    },
                },
            )
        )

        fig_resources.update_layout(height=400)
        st.plotly_chart(fig_resources, use_container_width=True)

    with perf_col2:
        st.markdown("**📊 Performance Trends**")

        # Performance trend over time
        hours = list(range(24))
        response_times = [np.random.uniform(0.8, 2.5) for _ in hours]
        throughput = [np.random.uniform(800, 1500) for _ in hours]

        fig_trends = go.Figure()

        fig_trends.add_trace(
            go.Scatter(
                x=hours,
                y=response_times,
                mode="lines+markers",
                name="Response Time (s)",
                yaxis="y",
                line=dict(color="blue"),
            )
        )

        fig_trends.add_trace(
            go.Scatter(
                x=hours,
                y=throughput,
                mode="lines+markers",
                name="Throughput (req/min)",
                yaxis="y2",
                line=dict(color="red"),
            )
        )

        fig_trends.update_layout(
            title="24-Hour Performance Trends",
            xaxis_title="Hour of Day",
            yaxis=dict(title="Response Time (s)", side="left"),
            yaxis2=dict(title="Throughput (req/min)", side="right", overlaying="y"),
            height=400,
        )

        st.plotly_chart(fig_trends, use_container_width=True)

    # Live performance table
    st.markdown("**📈 Live Performance Metrics**")

    perf_metrics = pd.DataFrame(
        {
            "Metric": [
                "API Response Time",
                "Database Query Time",
                "AI Model Inference",
                "Cache Hit Rate",
                "Error Rate",
            ],
            "Current": ["1.2s", "0.3s", "2.1s", "94.7%", "0.02%"],
            "Target": ["<2.0s", "<0.5s", "<3.0s", ">90%", "<0.1%"],
            "Status": ["🟢 Good", "🟢 Good", "🟢 Good", "🟢 Good", "🟢 Good"],
            "Trend": ["↗️ +5%", "↘️ -2%", "↗️ +8%", "↗️ +1%", "↘️ -15%"],
        }
    )

    st.dataframe(perf_metrics, hide_index=True, use_container_width=True)

# Footer with system status
st.divider()
st.markdown(
    """
### 🔄 **System Status Summary**
- **🟢 All Systems Operational** | Last Incident: None in 47 days
- **⚡ Real-time Processing**: 1,247 events/minute | **🎯 AI Accuracy**: 94.7%
- **🚀 Automation Level**: 89% automated workflows | **💰 Cost Optimization**: $45K/month saved
"""
)

# Auto-refresh indicator
if st.button("🔄 Force Refresh Dashboard"):
    st.rerun()
