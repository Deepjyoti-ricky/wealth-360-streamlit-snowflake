"""
Geographic Insights - Geospatial analytics and climate risk

This page provides comprehensive geospatial analytics including client distribution,
climate risk analysis, and interactive 3D visualizations using PyDeck.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import numpy as np
import plotly.express as px
import pydeck as pdk
import streamlit as st

from utils.data_functions import get_client_geographic_distribution

st.set_page_config(page_title="Geographic Insights", page_icon="🌍", layout="wide")

# Page header
st.markdown("# 🌍 Geographic Insights & Climate Risk")
st.caption(
    "🗺️ **Location-based insights using Snowflake Weather & POI data | KPIs: Geographic AUM distribution, climate risk exposure, market penetration**"
)

# Geographic Distribution Analysis
st.markdown("### 🗺️ Geographic Distribution & Market Concentration")
geo_dist_df = get_client_geographic_distribution()

if not geo_dist_df.empty:
    # Top states by AUM
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**🏆 Top States by AUM**")
        top_states = geo_dist_df.head(10)
        fig1 = px.bar(
            top_states,
            x="TOTAL_AUM",
            y="STATE",
            orientation="h",
            title="Top 10 States by Assets Under Management",
            labels={"TOTAL_AUM": "Total AUM ($)", "STATE": "State"},
        )
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        st.markdown("**📊 Market Tier Distribution**")
        market_tier_counts = geo_dist_df["MARKET_TIER"].value_counts()
        fig2 = px.pie(
            values=market_tier_counts.values,
            names=market_tier_counts.index,
            title="Market Tier Distribution",
            color_discrete_map={
                "High Value Market": "#2E8B57",
                "Medium Value Market": "#FFD700",
                "Emerging Market": "#FF6347",
            },
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Geographic metrics table
    st.markdown("**📋 State-by-State Analysis**")
    st.dataframe(geo_dist_df, use_container_width=True)

    # Risk tolerance by geography
    st.markdown("**⚖️ Risk Tolerance Geographic Distribution**")
    fig3 = px.scatter(
        geo_dist_df,
        x="PCT_CONSERVATIVE",
        y="PCT_AGGRESSIVE",
        size="TOTAL_AUM",
        color="MARKET_TIER",
        hover_data=["STATE", "CLIENT_COUNT"],
        title="Conservative vs Aggressive Risk Tolerance by State",
        labels={
            "PCT_CONSERVATIVE": "% Conservative Clients",
            "PCT_AGGRESSIVE": "% Aggressive Growth Clients",
        },
    )
    st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("Geographic distribution data not available.")

# Interactive Maps Section
st.divider()
st.markdown("### 🗺️ **Interactive 3D Visualizations**")


# Simulated location data for demonstration
@st.cache_data
def get_demo_location_data():
    """Generate demo location data for visualization"""
    np.random.seed(42)

    # Major US cities with coordinates
    cities_data = [
        {
            "city": "New York",
            "state": "NY",
            "lat": 40.7128,
            "lon": -74.0060,
            "aum": 250000000,
            "clients": 450,
            "risk": "Moderate",
        },
        {
            "city": "Los Angeles",
            "state": "CA",
            "lat": 34.0522,
            "lon": -118.2437,
            "aum": 180000000,
            "clients": 320,
            "risk": "Growth",
        },
        {
            "city": "Chicago",
            "state": "IL",
            "lat": 41.8781,
            "lon": -87.6298,
            "aum": 150000000,
            "clients": 280,
            "risk": "Balanced",
        },
        {
            "city": "Houston",
            "state": "TX",
            "lat": 29.7604,
            "lon": -95.3698,
            "aum": 120000000,
            "clients": 220,
            "risk": "Growth",
        },
        {
            "city": "Miami",
            "state": "FL",
            "lat": 25.7617,
            "lon": -80.1918,
            "aum": 100000000,
            "clients": 180,
            "risk": "Aggressive Growth",
        },
        {
            "city": "San Francisco",
            "state": "CA",
            "lat": 37.7749,
            "lon": -122.4194,
            "aum": 200000000,
            "clients": 250,
            "risk": "Growth",
        },
        {
            "city": "Boston",
            "state": "MA",
            "lat": 42.3601,
            "lon": -71.0589,
            "aum": 140000000,
            "clients": 200,
            "risk": "Conservative",
        },
        {
            "city": "Seattle",
            "state": "WA",
            "lat": 47.6062,
            "lon": -122.3321,
            "aum": 110000000,
            "clients": 160,
            "risk": "Balanced",
        },
        {
            "city": "Denver",
            "state": "CO",
            "lat": 39.7392,
            "lon": -104.9903,
            "aum": 80000000,
            "clients": 140,
            "risk": "Growth",
        },
        {
            "city": "Atlanta",
            "state": "GA",
            "lat": 33.7490,
            "lon": -84.3880,
            "aum": 90000000,
            "clients": 150,
            "risk": "Moderate",
        },
    ]

    # Add some random variation and additional cities
    for i, city in enumerate(cities_data):
        city["lat"] += np.random.normal(0, 0.1)
        city["lon"] += np.random.normal(0, 0.1)
        city["portfolio_size"] = np.log1p(
            city["aum"] / 1000000
        )  # Log scale for visualization

    return cities_data


# Map visualizations
map_subtabs = st.tabs(
    ["🏘️ Client Distribution", "🌡️ Climate Risk", "👥 Advisor Coverage"]
)

with map_subtabs[0]:
    st.markdown("### 🏘️ Client Location & Portfolio Distribution")

    client_locations = get_demo_location_data()

    # Color mapping for risk tolerance
    risk_colors = {
        "Conservative": [70, 130, 180, 180],  # Steel Blue
        "Moderate": [255, 165, 0, 180],  # Orange
        "Balanced": [50, 205, 50, 180],  # Lime Green
        "Growth": [255, 99, 71, 180],  # Tomato
        "Aggressive Growth": [220, 20, 60, 180],  # Crimson
    }

    # Add color to data
    for location in client_locations:
        location["color"] = risk_colors.get(location["risk"], [128, 128, 128, 180])

    # Create PyDeck visualization
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=39.8283,
                longitude=-98.5795,
                zoom=3,
                pitch=45,  # 3D effect
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=client_locations,
                    get_position=["lon", "lat"],
                    get_color="color",
                    get_radius="portfolio_size",
                    radius_scale=20,
                    radius_min_pixels=3,
                    radius_max_pixels=30,
                    pickable=True,
                    filled=True,
                    stroked=True,
                    stroke_width=1,
                    stroke_color=[255, 255, 255, 100],
                )
            ],
            tooltip={
                "html": "<b>{city}, {state}</b><br>"
                "AUM: ${aum:,.0f}<br>"
                "Clients: {clients}<br>"
                "Risk Profile: {risk}",
                "style": {"backgroundColor": "steelblue", "color": "white"},
            },
        )
    )

with map_subtabs[1]:
    st.markdown("### 🌡️ Climate Risk Heat Map")

    # Simulated climate risk data
    climate_risk_data = [
        {
            "state": "FL",
            "lat": 27.7663,
            "lon": -81.6868,
            "risk_level": "Very High",
            "aum_exposure": 100000000,
            "risk_type": "Hurricane",
        },
        {
            "state": "CA",
            "lat": 36.1162,
            "lon": -119.6816,
            "risk_level": "High",
            "aum_exposure": 380000000,
            "risk_type": "Wildfire/Earthquake",
        },
        {
            "state": "TX",
            "lat": 31.0545,
            "lon": -97.5635,
            "risk_level": "High",
            "aum_exposure": 120000000,
            "risk_type": "Extreme Heat",
        },
        {
            "state": "LA",
            "lat": 31.1695,
            "lon": -91.8678,
            "risk_level": "Very High",
            "aum_exposure": 45000000,
            "risk_type": "Hurricane/Flood",
        },
        {
            "state": "AZ",
            "lat": 33.7298,
            "lon": -111.4312,
            "risk_level": "Medium",
            "aum_exposure": 60000000,
            "risk_type": "Extreme Heat",
        },
        {
            "state": "NY",
            "lat": 42.1657,
            "lon": -74.9481,
            "risk_level": "Medium",
            "aum_exposure": 250000000,
            "risk_type": "Sea Level Rise",
        },
        {
            "state": "WA",
            "lat": 47.0379,
            "lon": -122.9015,
            "risk_level": "Medium",
            "aum_exposure": 110000000,
            "risk_type": "Wildfire",
        },
        {
            "state": "CO",
            "lat": 39.0598,
            "lon": -105.3111,
            "risk_level": "Low",
            "aum_exposure": 80000000,
            "risk_type": "Drought",
        },
    ]

    # Color mapping for risk levels
    risk_level_colors = {
        "Very High": [255, 0, 0, 200],  # Red
        "High": [255, 165, 0, 200],  # Orange
        "Medium": [255, 255, 0, 200],  # Yellow
        "Low": [0, 255, 0, 200],  # Green
    }

    # Add colors and elevation
    for location in climate_risk_data:
        location["color"] = risk_level_colors.get(
            location["risk_level"], [128, 128, 128, 200]
        )
        location["elevation"] = np.log1p(location["aum_exposure"] / 1000000) * 100

    # 3D Column visualization
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/dark-v9",
            initial_view_state=pdk.ViewState(
                latitude=39.8283,
                longitude=-98.5795,
                zoom=3,
                pitch=50,
                bearing=0,
            ),
            layers=[
                pdk.Layer(
                    "ColumnLayer",
                    data=climate_risk_data,
                    get_position=["lon", "lat"],
                    get_elevation="elevation",
                    elevation_scale=100,
                    get_fill_color="color",
                    radius=50000,
                    pickable=True,
                    auto_highlight=True,
                )
            ],
            tooltip={
                "html": "<b>State: {state}</b><br>"
                "Climate Risk: {risk_level}<br>"
                "Risk Type: {risk_type}<br>"
                "AUM Exposure: ${aum_exposure:,.0f}",
                "style": {"backgroundColor": "black", "color": "white"},
            },
        )
    )

with map_subtabs[2]:
    st.markdown("### 👥 Advisor Territory Coverage")

    # Simulated advisor data
    advisor_data = [
        {
            "name": "John Smith",
            "lat": 40.7589,
            "lon": -73.9851,
            "coverage": "Regional",
            "clients": 45,
            "aum": 75000000,
        },
        {
            "name": "Sarah Johnson",
            "lat": 34.0522,
            "lon": -118.2437,
            "coverage": "State",
            "clients": 38,
            "aum": 62000000,
        },
        {
            "name": "Mike Chen",
            "lat": 37.7749,
            "lon": -122.4194,
            "coverage": "Local",
            "clients": 28,
            "aum": 45000000,
        },
        {
            "name": "Lisa Rodriguez",
            "lat": 25.7617,
            "lon": -80.1918,
            "coverage": "Regional",
            "clients": 52,
            "aum": 85000000,
        },
        {
            "name": "David Wilson",
            "lat": 41.8781,
            "lon": -87.6298,
            "coverage": "National",
            "clients": 67,
            "aum": 120000000,
        },
        {
            "name": "Emily Brown",
            "lat": 29.7604,
            "lon": -95.3698,
            "coverage": "State",
            "clients": 41,
            "aum": 68000000,
        },
        {
            "name": "James Lee",
            "lat": 47.6062,
            "lon": -122.3321,
            "coverage": "Regional",
            "clients": 35,
            "aum": 58000000,
        },
        {
            "name": "Maria Garcia",
            "lat": 39.7392,
            "lon": -104.9903,
            "coverage": "Local",
            "clients": 29,
            "aum": 42000000,
        },
    ]

    # Coverage type colors
    coverage_colors = {
        "National": [255, 0, 0, 200],  # Red
        "Regional": [255, 165, 0, 200],  # Orange
        "State": [0, 255, 0, 200],  # Green
        "Local": [0, 0, 255, 200],  # Blue
    }

    # Add colors and scaled AUM
    for advisor in advisor_data:
        advisor["color"] = coverage_colors.get(
            advisor["coverage"], [128, 128, 128, 200]
        )
        advisor["aum_size"] = np.log1p(advisor["aum"] / 1000000)

    # Combined hexagon and scatter visualization
    st.pydeck_chart(
        pdk.Deck(
            map_style="mapbox://styles/mapbox/light-v9",
            initial_view_state=pdk.ViewState(
                latitude=39.8283,
                longitude=-98.5795,
                zoom=4,
                pitch=30,
            ),
            layers=[
                # Hexagon layer for advisor density
                pdk.Layer(
                    "HexagonLayer",
                    data=advisor_data,
                    get_position=["lon", "lat"],
                    get_weight="aum",
                    radius=100000,
                    elevation_scale=10,
                    elevation_range=[0, 3000],
                    pickable=True,
                    extruded=True,
                    coverage=0.8,
                    auto_highlight=True,
                ),
                # Scatter layer for individual advisors
                pdk.Layer(
                    "ScatterplotLayer",
                    data=advisor_data,
                    get_position=["lon", "lat"],
                    get_color="color",
                    get_radius="aum_size",
                    radius_scale=100,
                    radius_min_pixels=5,
                    radius_max_pixels=20,
                    pickable=True,
                    filled=True,
                    stroked=True,
                    stroke_width=2,
                    stroke_color=[255, 255, 255, 200],
                ),
            ],
            tooltip={
                "html": "<b>{name}</b><br>"
                "Coverage: {coverage}<br>"
                "Clients: {clients}<br>"
                "Total AUM: ${aum:,.0f}",
                "style": {"backgroundColor": "navy", "color": "white"},
            },
        )
    )

# Map Legend
st.markdown("### 🎨 Map Legend")
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        """
    **Client Location Map**
    - 🔵 Conservative (Steel Blue)
    - 🟠 Moderate (Orange)
    - 🟢 Balanced (Green)
    - 🔴 Growth (Tomato)
    - ⚫ Aggressive Growth (Crimson)
    - *Size = Portfolio Value*
    """
    )

with col2:
    st.markdown(
        """
    **Climate Risk Map**
    - 🔴 Very High Risk
    - 🟠 High Risk
    - 🟡 Medium Risk
    - 🟢 Low Risk
    - *Height = AUM Exposure*
    """
    )

with col3:
    st.markdown(
        """
    **Advisor Coverage Map**
    - 🔴 National Coverage
    - 🟠 Regional Coverage
    - 🟢 State Coverage
    - 🔵 Local Coverage
    - *Hexagons = AUM Density*
    """
    )

# Geographic Analytics Summary
st.divider()
st.markdown("### 📊 **Geographic Analytics Summary**")

if not geo_dist_df.empty:
    geo_col1, geo_col2, geo_col3, geo_col4 = st.columns(4)

    with geo_col1:
        st.markdown("#### 🏆 **Top Market**")
        top_state = geo_dist_df.iloc[0]
        st.metric("State", top_state["STATE"])
        st.metric("AUM", f"${top_state['TOTAL_AUM']:,.0f}")
        st.metric("Clients", f"{top_state['CLIENT_COUNT']:,}")

    with geo_col2:
        st.markdown("#### 🌍 **Market Coverage**")
        total_states = len(geo_dist_df)
        high_value_markets = len(
            geo_dist_df[geo_dist_df["MARKET_TIER"] == "High Value Market"]
        )
        st.metric("Total States", total_states)
        st.metric("High Value Markets", high_value_markets)
        st.metric("Coverage Rate", f"{high_value_markets/total_states*100:.1f}%")

    with geo_col3:
        st.markdown("#### ⚖️ **Risk Profile**")
        avg_conservative = geo_dist_df["PCT_CONSERVATIVE"].mean()
        avg_aggressive = geo_dist_df["PCT_AGGRESSIVE"].mean()
        st.metric("Avg Conservative %", f"{avg_conservative:.1f}%")
        st.metric("Avg Aggressive %", f"{avg_aggressive:.1f}%")

    with geo_col4:
        st.markdown("#### 🌡️ **Climate Exposure**")
        # Simulated climate metrics
        st.metric("High Risk States", "4")
        st.metric("Exposed AUM", "$705M")
        st.metric("Risk Mitigation", "92%")
