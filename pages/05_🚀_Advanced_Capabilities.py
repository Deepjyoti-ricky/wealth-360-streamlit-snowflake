"""
Advanced Capabilities - Next-Generation Analytics Platform

This page showcases cutting-edge capabilities including geospatial intelligence,
climate risk analysis, predictive modeling, and Snowflake Marketplace integration.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st

from utils.data_functions import get_client_geographic_distribution

st.set_page_config(page_title="Advanced Capabilities", page_icon="🚀", layout="wide")

# Advanced CSS styling
st.markdown(
    """
<style>
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 40px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .capability-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 25px;
        border-radius: 15px;
        color: white;
        margin: 15px 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    .capability-card:hover {
        transform: translateY(-5px);
    }
    .tech-stack-card {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin: 10px 0;
    }
    .marketplace-card {
        background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin: 10px 0;
    }
    .prediction-card {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        margin: 10px 0;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Hero section
st.markdown(
    """
<div class="hero-section">
    <h1>🚀 Advanced Capabilities</h1>
    <h3>Next-Generation Analytics Platform</h3>
    <p style="font-size: 18px; margin-bottom: 0;">
        Cutting-edge geospatial intelligence, climate risk analysis, and predictive modeling
        powered by Snowflake Marketplace data and advanced AI
    </p>
</div>
""",
    unsafe_allow_html=True,
)

# Platform Capabilities Overview
st.markdown("### 🎯 **Platform Capabilities Matrix**")

cap_col1, cap_col2, cap_col3, cap_col4 = st.columns(4)

with cap_col1:
    st.markdown(
        """
    <div class="capability-card">
        <h4>🌍 Geospatial Intelligence</h4>
        <ul style="text-align: left;">
            <li>3D Interactive Maps</li>
            <li>Client Distribution Analysis</li>
            <li>Territory Optimization</li>
            <li>Market Penetration</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with cap_col2:
    st.markdown(
        """
    <div class="capability-card">
        <h4>🌡️ Climate Risk Analytics</h4>
        <ul style="text-align: left;">
            <li>Weather Data Integration</li>
            <li>Environmental Risk Scoring</li>
            <li>Portfolio Climate Exposure</li>
            <li>Adaptation Strategies</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with cap_col3:
    st.markdown(
        """
    <div class="capability-card">
        <h4>🔮 Predictive Modeling</h4>
        <ul style="text-align: left;">
            <li>Market Trend Forecasting</li>
            <li>Client Behavior Prediction</li>
            <li>Risk Assessment Models</li>
            <li>Revenue Optimization</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

with cap_col4:
    st.markdown(
        """
    <div class="capability-card">
        <h4>🛒 Marketplace Integration</h4>
        <ul style="text-align: left;">
            <li>External Data Sources</li>
            <li>Real-time Data Feeds</li>
            <li>Third-party Analytics</li>
            <li>Data Enrichment</li>
        </ul>
    </div>
    """,
        unsafe_allow_html=True,
    )

st.divider()

# Advanced Analytics Tabs
advanced_tabs = st.tabs(
    [
        "🌍 Geospatial Intelligence",
        "🌡️ Climate Risk Analysis",
        "🔮 Predictive Analytics",
        "🛒 Marketplace Integration",
        "🏗️ Technical Architecture",
    ]
)

# Geospatial Intelligence
with advanced_tabs[0]:
    st.markdown("### 🌍 **Geospatial Intelligence Platform**")

    # Geographic metrics
    geo_dist_df = get_client_geographic_distribution()

    if not geo_dist_df.empty:
        # Geographic overview cards
        geo_col1, geo_col2, geo_col3 = st.columns(3)

        total_states = len(geo_dist_df)
        total_aum = geo_dist_df["TOTAL_AUM"].sum()
        high_value_markets = len(
            geo_dist_df[geo_dist_df["MARKET_TIER"] == "High Value Market"]
        )

        with geo_col1:
            st.markdown(
                f"""
            <div class="tech-stack-card">
                <h4>🗺️ Geographic Coverage</h4>
                <h2>{total_states}</h2>
                <p>States with presence</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with geo_col2:
            st.markdown(
                f"""
            <div class="marketplace-card">
                <h4>💰 Geographic AUM</h4>
                <h2>${total_aum:,.0f}</h2>
                <p>Total assets managed</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        with geo_col3:
            st.markdown(
                f"""
            <div class="prediction-card">
                <h4>🎯 High Value Markets</h4>
                <h2>{high_value_markets}</h2>
                <p>Premium market presence</p>
            </div>
            """,
                unsafe_allow_html=True,
            )

        # Enhanced Geographic Visualizations
        geo_viz_col1, geo_viz_col2 = st.columns(2)

        with geo_viz_col1:
            st.markdown("**🗺️ Interactive Market Map**")

            # Create enhanced choropleth map
            fig = px.choropleth(
                geo_dist_df,
                locations="STATE",
                color="TOTAL_AUM",
                locationmode="USA-states",
                scope="usa",
                title="AUM Distribution by State",
                color_continuous_scale="Viridis",
                labels={"TOTAL_AUM": "Total AUM ($)"},
            )
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)

        with geo_viz_col2:
            st.markdown("**📊 Market Tier Analysis**")

            # Market tier distribution
            market_tier_counts = geo_dist_df["MARKET_TIER"].value_counts()
            fig = px.pie(
                values=market_tier_counts.values,
                names=market_tier_counts.index,
                title="Market Tier Distribution",
                color_discrete_map={
                    "High Value Market": "#2E8B57",
                    "Medium Value Market": "#FFD700",
                    "Emerging Market": "#FF6347",
                },
            )
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig, use_container_width=True)

        # 3D Interactive Map with PyDeck
        st.markdown("**🎯 3D Client Distribution Map**")

        # Generate demo data for 3D visualization
        @st.cache_data
        def get_3d_client_data():
            np.random.seed(42)
            cities_data = [
                {
                    "city": "New York",
                    "lat": 40.7128,
                    "lon": -74.0060,
                    "aum": 250000000,
                    "clients": 450,
                },
                {
                    "city": "Los Angeles",
                    "lat": 34.0522,
                    "lon": -118.2437,
                    "aum": 180000000,
                    "clients": 320,
                },
                {
                    "city": "Chicago",
                    "lat": 41.8781,
                    "lon": -87.6298,
                    "aum": 150000000,
                    "clients": 280,
                },
                {
                    "city": "Houston",
                    "lat": 29.7604,
                    "lon": -95.3698,
                    "aum": 120000000,
                    "clients": 220,
                },
                {
                    "city": "Miami",
                    "lat": 25.7617,
                    "lon": -80.1918,
                    "aum": 100000000,
                    "clients": 180,
                },
                {
                    "city": "San Francisco",
                    "lat": 37.7749,
                    "lon": -122.4194,
                    "aum": 200000000,
                    "clients": 250,
                },
                {
                    "city": "Boston",
                    "lat": 42.3601,
                    "lon": -71.0589,
                    "aum": 140000000,
                    "clients": 200,
                },
                {
                    "city": "Seattle",
                    "lat": 47.6062,
                    "lon": -122.3321,
                    "aum": 110000000,
                    "clients": 160,
                },
                {
                    "city": "Denver",
                    "lat": 39.7392,
                    "lon": -104.9903,
                    "aum": 80000000,
                    "clients": 140,
                },
                {
                    "city": "Atlanta",
                    "lat": 33.7490,
                    "lon": -84.3880,
                    "aum": 90000000,
                    "clients": 150,
                },
            ]

            for city in cities_data:
                city["elevation"] = np.log1p(city["aum"] / 1000000) * 100
                city["color"] = [
                    int(255 * (city["aum"] / 250000000)),
                    100,
                    255 - int(255 * (city["aum"] / 250000000)),
                    180,
                ]

            return cities_data

        client_3d_data = get_3d_client_data()

        # Create 3D column chart
        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v8",
                initial_view_state=pdk.ViewState(
                    latitude=39.8283,
                    longitude=-98.5795,
                    zoom=3,
                    pitch=60,
                    bearing=0,
                ),
                layers=[
                    pdk.Layer(
                        "ColumnLayer",
                        data=client_3d_data,
                        get_position=["lon", "lat"],
                        get_elevation="elevation",
                        elevation_scale=200,
                        get_fill_color="color",
                        radius=80000,
                        pickable=True,
                        auto_highlight=True,
                    )
                ],
                tooltip={
                    "html": "<b>City: {city}</b><br>"
                    "AUM: ${aum:,.0f}<br>"
                    "Clients: {clients}",
                    "style": {"backgroundColor": "steelblue", "color": "white"},
                },
            )
        )

# Climate Risk Analysis
with advanced_tabs[1]:
    st.markdown("### 🌡️ **Climate Risk Analysis**")

    # Climate risk overview
    climate_col1, climate_col2, climate_col3 = st.columns(3)

    with climate_col1:
        st.markdown(
            """
        <div class="tech-stack-card">
            <h4>🌊 High Risk Exposure</h4>
            <h2>$705M</h2>
            <p>AUM in high-risk areas</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with climate_col2:
        st.markdown(
            """
        <div class="marketplace-card">
            <h4>🌡️ Climate Score</h4>
            <h2>7.3/10</h2>
            <p>Portfolio resilience</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with climate_col3:
        st.markdown(
            """
        <div class="prediction-card">
            <h4>🛡️ Risk Mitigation</h4>
            <h2>92%</h2>
            <p>Coverage rate</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Climate risk visualizations
    climate_viz_col1, climate_viz_col2 = st.columns(2)

    with climate_viz_col1:
        st.markdown("**🌡️ Climate Risk Heat Map**")

        # Simulated climate risk data
        climate_risk_data = [
            {
                "state": "FL",
                "lat": 27.7663,
                "lon": -81.6868,
                "risk_level": "Very High",
                "aum_exposure": 100000000,
            },
            {
                "state": "CA",
                "lat": 36.1162,
                "lon": -119.6816,
                "risk_level": "High",
                "aum_exposure": 380000000,
            },
            {
                "state": "TX",
                "lat": 31.0545,
                "lon": -97.5635,
                "risk_level": "High",
                "aum_exposure": 120000000,
            },
            {
                "state": "NY",
                "lat": 42.1657,
                "lon": -74.9481,
                "risk_level": "Medium",
                "aum_exposure": 250000000,
            },
            {
                "state": "WA",
                "lat": 47.0379,
                "lon": -122.9015,
                "risk_level": "Medium",
                "aum_exposure": 110000000,
            },
        ]

        risk_colors = {
            "Very High": [255, 0, 0, 200],
            "High": [255, 165, 0, 200],
            "Medium": [255, 255, 0, 200],
            "Low": [0, 255, 0, 200],
        }

        for location in climate_risk_data:
            location["color"] = risk_colors.get(
                location["risk_level"], [128, 128, 128, 200]
            )
            location["elevation"] = np.log1p(location["aum_exposure"] / 1000000) * 150

        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/light-v8",
                initial_view_state=pdk.ViewState(
                    latitude=39.8283,
                    longitude=-98.5795,
                    zoom=3,
                    pitch=45,
                ),
                layers=[
                    pdk.Layer(
                        "ColumnLayer",
                        data=climate_risk_data,
                        get_position=["lon", "lat"],
                        get_elevation="elevation",
                        elevation_scale=100,
                        get_fill_color="color",
                        radius=100000,
                        pickable=True,
                    )
                ],
                tooltip={
                    "html": "<b>State: {state}</b><br>"
                    "Risk Level: {risk_level}<br>"
                    "AUM Exposure: ${aum_exposure:,.0f}",
                    "style": {"backgroundColor": "black", "color": "white"},
                },
            )
        )

    with climate_viz_col2:
        st.markdown("**📊 Risk Distribution Analysis**")

        # Risk level distribution
        risk_data = {
            "Risk Level": ["Very High", "High", "Medium", "Low"],
            "AUM Exposure": [100000000, 500000000, 360000000, 145000000],
            "Client Count": [45, 234, 156, 78],
        }

        fig = go.Figure()
        fig.add_trace(
            go.Bar(
                name="AUM Exposure",
                x=risk_data["Risk Level"],
                y=risk_data["AUM Exposure"],
                yaxis="y",
                marker_color=["#ff0000", "#ffa500", "#ffff00", "#00ff00"],
            )
        )
        fig.add_trace(
            go.Scatter(
                name="Client Count",
                x=risk_data["Risk Level"],
                y=risk_data["Client Count"],
                yaxis="y2",
                mode="lines+markers",
                marker_color="blue",
                line=dict(width=3),
            )
        )

        fig.update_layout(
            title="Climate Risk vs Client Distribution",
            xaxis_title="Risk Level",
            yaxis=dict(title="AUM Exposure ($)", side="left"),
            yaxis2=dict(title="Client Count", side="right", overlaying="y"),
            height=400,
        )

        st.plotly_chart(fig, use_container_width=True)

    # Climate adaptation strategies
    st.markdown("**🛡️ Climate Adaptation Strategies**")

    strategy_col1, strategy_col2, strategy_col3 = st.columns(3)

    with strategy_col1:
        st.markdown(
            """
        **🌊 Flood Risk Mitigation**
        • Diversify geographic exposure
        • Invest in flood-resistant assets
        • Insurance coverage optimization
        • Emergency liquidity planning
        """
        )

    with strategy_col2:
        st.markdown(
            """
        **🔥 Wildfire Protection**
        • Property insurance review
        • Defensible space requirements
        • Alternative evacuation assets
        • Business continuity planning
        """
        )

    with strategy_col3:
        st.markdown(
            """
        **🌡️ Temperature Adaptation**
        • Energy-efficient investments
        • HVAC infrastructure upgrades
        • Renewable energy transition
        • Carbon offset strategies
        """
        )

# Predictive Analytics
with advanced_tabs[2]:
    st.markdown("### 🔮 **Predictive Analytics & Forecasting**")

    # Prediction metrics
    pred_col1, pred_col2, pred_col3 = st.columns(3)

    with pred_col1:
        st.markdown(
            """
        <div class="prediction-card">
            <h4>📈 Forecast Accuracy</h4>
            <h2>94.7%</h2>
            <p>Model performance</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with pred_col2:
        st.markdown(
            """
        <div class="tech-stack-card">
            <h4>🎯 Predictions Generated</h4>
            <h2>1,247</h2>
            <p>This month</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with pred_col3:
        st.markdown(
            """
        <div class="marketplace-card">
            <h4>💰 Revenue Impact</h4>
            <h2>$3.2M</h2>
            <p>From predictions</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Predictive models showcase
    pred_viz_col1, pred_viz_col2 = st.columns(2)

    with pred_viz_col1:
        st.markdown("**📈 AUM Growth Prediction**")

        # Generate prediction data
        import pandas as pd

        dates = pd.date_range(start="2024-01-01", end="2025-06-30", freq="M")
        historical_aum = [850 + i * 15 + np.random.normal(0, 5) for i in range(12)]
        predicted_aum = [
            historical_aum[-1] + (i + 1) * 18 + np.random.normal(0, 3) for i in range(6)
        ]

        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=dates[:12],
                y=historical_aum,
                mode="lines+markers",
                name="Historical AUM",
                line=dict(color="blue", width=3),
            )
        )
        fig.add_trace(
            go.Scatter(
                x=dates[12:],
                y=predicted_aum,
                mode="lines+markers",
                name="Predicted AUM",
                line=dict(color="red", dash="dash", width=3),
            )
        )

        fig.update_layout(
            title="AUM Growth Forecast (Next 6 Months)",
            xaxis_title="Date",
            yaxis_title="AUM ($ Millions)",
            height=400,
        )

        st.plotly_chart(fig, use_container_width=True)

    with pred_viz_col2:
        st.markdown("**🎯 Client Behavior Prediction**")

        # Client behavior prediction matrix
        behavior_data = {
            "Behavior": [
                "High Engagement",
                "Medium Engagement",
                "Low Engagement",
                "Churn Risk",
            ],
            "Predicted": [156, 234, 89, 23],
            "Confidence": [0.94, 0.87, 0.91, 0.96],
        }

        fig = px.bar(
            x=behavior_data["Behavior"],
            y=behavior_data["Predicted"],
            color=behavior_data["Confidence"],
            title="Client Behavior Predictions",
            labels={"y": "Number of Clients", "color": "Confidence Score"},
            color_continuous_scale="Viridis",
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    # Prediction models overview
    st.markdown("**🧠 Machine Learning Models**")

    model_col1, model_col2, model_col3 = st.columns(3)

    with model_col1:
        st.markdown(
            """
        **📊 Time Series Forecasting**
        • ARIMA models for AUM prediction
        • Seasonal decomposition
        • Trend analysis
        • Confidence intervals
        """
        )

    with model_col2:
        st.markdown(
            """
        **🎯 Classification Models**
        • Churn prediction (Random Forest)
        • Risk scoring (XGBoost)
        • Client segmentation (K-means)
        • Behavior prediction (Neural Networks)
        """
        )

    with model_col3:
        st.markdown(
            """
        **🔮 Advanced Analytics**
        • Reinforcement learning for portfolio optimization
        • NLP for sentiment analysis
        • Computer vision for document processing
        • Graph neural networks for relationship analysis
        """
        )

# Marketplace Integration
with advanced_tabs[3]:
    st.markdown("### 🛒 **Snowflake Marketplace Integration**")

    # Marketplace overview
    market_col1, market_col2, market_col3 = st.columns(3)

    with market_col1:
        st.markdown(
            """
        <div class="marketplace-card">
            <h4>📦 Data Products</h4>
            <h2>47</h2>
            <p>Integrated datasets</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with market_col2:
        st.markdown(
            """
        <div class="tech-stack-card">
            <h4>🔄 Real-time Feeds</h4>
            <h2>12</h2>
            <p>Live data streams</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with market_col3:
        st.markdown(
            """
        <div class="prediction-card">
            <h4>💡 Data Enrichment</h4>
            <h2>89%</h2>
            <p>Coverage improvement</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Marketplace data sources
    st.markdown("**📊 Integrated Data Sources**")

    data_sources = {
        "Category": [
            "Financial Markets",
            "Weather & Climate",
            "Demographics",
            "Economic Indicators",
            "Alternative Data",
        ],
        "Providers": [8, 6, 4, 7, 12],
        "Update Frequency": ["Real-time", "Hourly", "Daily", "Daily", "Mixed"],
    }

    # Create a comprehensive data source visualization
    fig = px.sunburst(
        values=[8, 6, 4, 7, 12],
        names=data_sources["Category"],
        title="Marketplace Data Sources Distribution",
    )
    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    # Key marketplace integrations
    st.markdown("**🔗 Key Integrations**")

    integration_col1, integration_col2 = st.columns(2)

    with integration_col1:
        st.markdown(
            """
        **🌡️ Weather & Environment**
        • National Weather Service data
        • Climate risk assessments
        • Environmental impact scoring
        • Natural disaster tracking

        **📈 Financial Market Data**
        • Real-time stock prices
        • Market volatility indices
        • Economic indicators
        • Sector performance metrics
        """
        )

    with integration_col2:
        st.markdown(
            """
        **👥 Demographics & Lifestyle**
        • Census data integration
        • Lifestyle segmentation
        • Income distribution
        • Education levels

        **🏢 Business Intelligence**
        • Industry classifications
        • Company financial data
        • Economic forecasts
        • Regulatory updates
        """
        )

# Technical Architecture
with advanced_tabs[4]:
    st.markdown("### 🏗️ **Technical Architecture**")

    # Architecture overview
    arch_col1, arch_col2, arch_col3 = st.columns(3)

    with arch_col1:
        st.markdown(
            """
        <div class="tech-stack-card">
            <h4>☁️ Cloud Native</h4>
            <p>100% Snowflake-based architecture</p>
            <p>Auto-scaling compute</p>
            <p>Zero-copy data sharing</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with arch_col2:
        st.markdown(
            """
        <div class="marketplace-card">
            <h4>🔒 Security & Governance</h4>
            <p>End-to-end encryption</p>
            <p>Role-based access control</p>
            <p>Data lineage tracking</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    with arch_col3:
        st.markdown(
            """
        <div class="prediction-card">
            <h4>⚡ Performance</h4>
            <p>Sub-second query response</p>
            <p>Unlimited concurrent users</p>
            <p>Real-time data processing</p>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Technology stack
    st.markdown("**🛠️ Technology Stack**")

    tech_stack = {
        "Layer": [
            "Presentation",
            "Application",
            "Data Processing",
            "Storage",
            "External",
        ],
        "Technologies": [
            "Streamlit in Snowflake, React Components",
            "Python, Snowpark, Cortex AI",
            "Snowflake Compute, Apache Spark",
            "Snowflake Data Cloud, Time Travel",
            "Marketplace Data, APIs, Real-time Feeds",
        ],
        "Benefits": [
            "Zero deployment complexity",
            "Native AI integration",
            "Elastic scaling",
            "Built-in governance",
            "Rich data ecosystem",
        ],
    }

    # Create architecture diagram using Plotly
    fig = go.Figure()

    # Add architecture layers
    layers = [
        "External Data",
        "Snowflake Storage",
        "Data Processing",
        "Application Layer",
        "Presentation",
    ]
    colors = ["#ff6b6b", "#4ecdc4", "#45b7d1", "#96ceb4", "#feca57"]

    # Create architecture stack visualization
    for layer, color in zip(layers, colors):
        fig.add_trace(
            go.Bar(
                name=layer,
                x=[layer],
                y=[1],
                marker_color=color,
                text=layer,
                textposition="auto",
                showlegend=False,
            )
        )

    fig.update_layout(
        title="Platform Architecture Stack",
        xaxis_title="Architecture Layers",
        yaxis_title="",
        showlegend=False,
        height=300,
        yaxis=dict(showticklabels=False),
    )

    st.plotly_chart(fig, use_container_width=True)

# Platform ROI and Business Value
st.divider()
st.markdown("### 💰 **Platform ROI & Business Value**")

roi_col1, roi_col2, roi_col3, roi_col4 = st.columns(4)

with roi_col1:
    st.markdown(
        """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #28a745;">
        <h4>💰 Revenue Impact</h4>
        <p><strong>$3.2M</strong> Additional revenue</p>
        <p><strong>23%</strong> Growth increase</p>
        <p><strong>$47M</strong> Optimization identified</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with roi_col2:
    st.markdown(
        """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #007bff;">
        <h4>⏱️ Efficiency Gains</h4>
        <p><strong>80%</strong> Time reduction</p>
        <p><strong>847 hours</strong> Saved monthly</p>
        <p><strong>94.7%</strong> Accuracy improvement</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with roi_col3:
    st.markdown(
        """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #ffc107;">
        <h4>🎯 Risk Reduction</h4>
        <p><strong>92%</strong> Risk mitigation</p>
        <p><strong>$8.3M</strong> Losses prevented</p>
        <p><strong>98.3%</strong> Compliance rate</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

with roi_col4:
    st.markdown(
        """
    <div style="background: #f8f9fa; padding: 20px; border-radius: 10px; border-left: 5px solid #dc3545;">
        <h4>🚀 Innovation Metrics</h4>
        <p><strong>1,247</strong> AI insights</p>
        <p><strong>47</strong> Data products</p>
        <p><strong>100%</strong> Cloud native</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

# Footer with next steps
st.divider()
st.markdown(
    """
### 🎯 **Platform Roadmap**

**🔮 Future Enhancements**
- Quantum computing integration for portfolio optimization
- Advanced NLP for document intelligence
- Blockchain integration for secure transactions
- IoT data streams for real-time insights

**🤝 Get Started**
Ready to transform your wealth management operations?
Contact our team to discuss custom implementations and POC opportunities.
"""
)

# Demo completion message
st.success(
    """
🎉 **Demo Complete!** You've explored the full capabilities of the BFSI Wealth 360 Analytics Platform.
This cutting-edge solution demonstrates Snowflake's power in delivering enterprise-grade financial analytics.
"""
)
