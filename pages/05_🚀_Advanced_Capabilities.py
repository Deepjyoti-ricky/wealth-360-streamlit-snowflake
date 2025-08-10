"""
Advanced Capabilities - Next-Generation Analytics Platform

This page showcases cutting-edge capabilities including geospatial intelligence,
climate risk analysis, predictive modeling, and Snowflake Marketplace integration.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
import streamlit as st

from utils.data_functions import get_client_geographic_distribution

st.set_page_config(page_title="Advanced Capabilities", page_icon="🚀", layout="wide")

# Sidebar - Advanced Analytics Configuration
st.sidebar.markdown("## 🚀 **Advanced Configuration**")

# Geospatial Settings
st.sidebar.markdown("### 🗺️ **Geospatial Settings**")
map_style = st.sidebar.selectbox(
    "Default Map Style",
    ["Light", "Dark", "Satellite", "Streets", "Outdoors", "Custom"],
    index=0,
)

geospatial_precision = st.sidebar.selectbox(
    "Geospatial Precision",
    ["City Level", "State Level", "County Level", "ZIP Code Level"],
    index=1,
)

enable_3d_visualization = st.sidebar.checkbox("🎯 Enable 3D Visualization", value=True)
enable_clustering = st.sidebar.checkbox("🔍 Enable Data Clustering", value=True)

# Climate Risk Configuration
st.sidebar.markdown("### 🌡️ **Climate Risk Settings**")
climate_risk_models = st.sidebar.multiselect(
    "Active Risk Models",
    ["Flood Risk", "Wildfire Risk", "Hurricane Risk", "Drought Risk", "Sea Level Rise"],
    default=["Flood Risk", "Wildfire Risk"],
)

risk_time_horizon = st.sidebar.selectbox(
    "Risk Time Horizon",
    ["1 Year", "5 Years", "10 Years", "25 Years", "50 Years"],
    index=2,
)

climate_scenario = st.sidebar.selectbox(
    "Climate Scenario",
    [
        "Current Conditions",
        "RCP 2.6 (Best Case)",
        "RCP 4.5 (Moderate)",
        "RCP 8.5 (Worst Case)",
    ],
    index=1,
)

# Advanced Analytics Options
st.sidebar.markdown("### 🔬 **Advanced Analytics**")
enable_ml_models = st.sidebar.checkbox("🤖 Machine Learning Models", value=True)
enable_predictive_analytics = st.sidebar.checkbox("🔮 Predictive Analytics", value=True)
enable_external_data = st.sidebar.checkbox("🌐 External Data Sources", value=True)

# Data Sources Configuration
st.sidebar.markdown("### 📊 **Data Sources**")
marketplace_data = st.sidebar.multiselect(
    "Snowflake Marketplace Data",
    ["Weather & Environment", "Economic Indicators", "Real Estate", "Demographics"],
    default=["Weather & Environment"],
)

# Performance & Optimization
st.sidebar.markdown("### ⚡ **Performance Settings**")
computation_mode = st.sidebar.selectbox(
    "Computation Mode",
    ["Real-time", "Batch Processing", "Hybrid", "On-Demand"],
    index=0,
)

cache_strategy = st.sidebar.selectbox(
    "Cache Strategy", ["Aggressive", "Balanced", "Conservative", "No Cache"], index=1
)

# Visualization Controls
st.sidebar.markdown("### 🎨 **Visualization Controls**")
color_scheme = st.sidebar.selectbox(
    "Color Scheme",
    ["Default", "High Contrast", "Colorblind Friendly", "Custom"],
    index=0,
)

animation_speed = st.sidebar.slider("Animation Speed", 0.1, 3.0, 1.0, 0.1)
detail_level = st.sidebar.slider("Detail Level", 1, 10, 7, 1)

# Export & Integration
st.sidebar.markdown("### 📤 **Export & Integration**")
if st.sidebar.button("🗺️ Export Geospatial Report", use_container_width=True):
    st.sidebar.success("Geospatial report exported!")

if st.sidebar.button("🌡️ Export Climate Analysis", use_container_width=True):
    st.sidebar.success("Climate analysis exported!")

if st.sidebar.button("🤖 Export ML Insights", use_container_width=True):
    st.sidebar.success("ML insights exported!")

# Navigation
st.sidebar.markdown("### 🧭 **Navigation**")
if st.sidebar.button("⚡ Real-Time Intelligence ←", use_container_width=True):
    st.switch_page("pages/04_⚡_Real_Time_Intelligence.py")

if st.sidebar.button("🎯 Back to Overview", use_container_width=True):
    st.switch_page("pages/01_🎯_Business_Overview.py")

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
        <h4>🎯 Advanced Analytics</h4>
        <ul style="text-align: left;">
            <li>Real-time Monitoring</li>
            <li>Interactive Dashboards</li>
            <li>Custom Visualizations</li>
            <li>Performance Optimization</li>
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

        # Multi-Map Visualization Dashboard
        st.markdown("**🗺️ Multi-Dimensional Geographic Analytics**")

        # Create tabbed map interface
        map_tabs = st.tabs(
            [
                "🏛️ State-Level Analysis",
                "🏙️ Metropolitan Areas",
                "🔥 Heat Map Analysis",
                "📈 Growth Trajectories",
            ]
        )

        with map_tabs[0]:
            # Enhanced state-level map using PyDeck (ScatterplotLayer over state centroids)
            # Prepare state centroids for USA (lat/lon for state abbreviations)
            state_centroids = {
                "AL": {"lat": 32.806671, "lon": -86.791130},
                "AK": {"lat": 61.370716, "lon": -152.404419},
                "AZ": {"lat": 33.729759, "lon": -111.431221},
                "AR": {"lat": 34.969704, "lon": -92.373123},
                "CA": {"lat": 36.116203, "lon": -119.681564},
                "CO": {"lat": 39.059811, "lon": -105.311104},
                "CT": {"lat": 41.597782, "lon": -72.755371},
                "DE": {"lat": 39.318523, "lon": -75.507141},
                "DC": {"lat": 38.905985, "lon": -77.033418},
                "FL": {"lat": 27.766279, "lon": -81.686783},
                "GA": {"lat": 33.040619, "lon": -83.643074},
                "HI": {"lat": 21.094318, "lon": -157.498337},
                "ID": {"lat": 44.240459, "lon": -114.478828},
                "IL": {"lat": 40.349457, "lon": -88.986137},
                "IN": {"lat": 39.849426, "lon": -86.258278},
                "IA": {"lat": 42.011539, "lon": -93.210526},
                "KS": {"lat": 38.526600, "lon": -96.726486},
                "KY": {"lat": 37.668140, "lon": -84.670067},
                "LA": {"lat": 31.169546, "lon": -91.867805},
                "ME": {"lat": 44.693947, "lon": -69.381927},
                "MD": {"lat": 39.063946, "lon": -76.802101},
                "MA": {"lat": 42.230171, "lon": -71.530106},
                "MI": {"lat": 43.326618, "lon": -84.536095},
                "MN": {"lat": 45.694454, "lon": -93.900192},
                "MS": {"lat": 32.741646, "lon": -89.678696},
                "MO": {"lat": 38.456085, "lon": -92.288368},
                "MT": {"lat": 46.921925, "lon": -110.454353},
                "NE": {"lat": 41.125370, "lon": -98.268082},
                "NV": {"lat": 38.313515, "lon": -117.055374},
                "NH": {"lat": 43.452492, "lon": -71.563896},
                "NJ": {"lat": 40.298904, "lon": -74.521011},
                "NM": {"lat": 34.840515, "lon": -106.248482},
                "NY": {"lat": 42.165726, "lon": -74.948051},
                "NC": {"lat": 35.630066, "lon": -79.806419},
                "ND": {"lat": 47.528912, "lon": -99.784012},
                "OH": {"lat": 40.388783, "lon": -82.764915},
                "OK": {"lat": 35.565342, "lon": -96.928917},
                "OR": {"lat": 44.572021, "lon": -122.070938},
                "PA": {"lat": 40.590752, "lon": -77.209755},
                "RI": {"lat": 41.680893, "lon": -71.511780},
                "SC": {"lat": 33.856892, "lon": -80.945007},
                "SD": {"lat": 44.299782, "lon": -99.438828},
                "TN": {"lat": 35.747845, "lon": -86.692345},
                "TX": {"lat": 31.054487, "lon": -97.563461},
                "UT": {"lat": 40.150032, "lon": -111.862434},
                "VT": {"lat": 44.045876, "lon": -72.710686},
                "VA": {"lat": 37.769337, "lon": -78.169968},
                "WA": {"lat": 47.400902, "lon": -121.490494},
                "WV": {"lat": 38.491226, "lon": -80.954453},
                "WI": {"lat": 44.268543, "lon": -89.616508},
                "WY": {"lat": 42.755966, "lon": -107.302490},
            }

            # Merge with geographic distribution data
            state_rows = []
            for _, row in geo_dist_df.iterrows():
                state_code = str(row.get("STATE", "")).upper()
                if state_code in state_centroids:
                    centroid = state_centroids[state_code]
                    total_aum = float(row.get("TOTAL_AUM", 0) or 0)
                    client_count = int(row.get("CLIENT_COUNT", 0) or 0)
                    market_tier = str(row.get("MARKET_TIER", "N/A") or "N/A")
                    state_rows.append(
                        {
                            "STATE": state_code,
                            "lat": centroid["lat"],
                            "lon": centroid["lon"],
                            "TOTAL_AUM": total_aum,
                            "CLIENT_COUNT": client_count,
                            "MARKET_TIER": market_tier,
                        }
                    )

            if state_rows:
                state_df = pd.DataFrame(state_rows)
                # Normalize AUM for color and radius
                aum_min = float(state_df["TOTAL_AUM"].min())
                aum_max = float(state_df["TOTAL_AUM"].max())
                span = (aum_max - aum_min) or 1.0
                norm = (state_df["TOTAL_AUM"] - aum_min) / span

                # Color gradient: low AUM -> blue, high AUM -> red
                state_df["color_r"] = (50 + (norm * 205)).astype(int)
                state_df["color_g"] = (80 + (norm * 120)).astype(int)
                state_df["color_b"] = (255 - (norm * 205)).astype(int)
                state_df["color_a"] = 220

                # Radius scaled by sqrt(AUM) for better visual distribution
                state_df["radius"] = np.sqrt(state_df["TOTAL_AUM"].clip(lower=0)) / 50.0

                # Map style mapping from sidebar selection
                style_map = {
                    "Light": "mapbox://styles/mapbox/light-v8",
                    "Dark": "mapbox://styles/mapbox/dark-v11",
                    "Satellite": "mapbox://styles/mapbox/satellite-v9",
                    "Streets": "mapbox://styles/mapbox/streets-v12",
                    "Outdoors": "mapbox://styles/mapbox/outdoors-v12",
                    "Custom": "mapbox://styles/mapbox/light-v8",
                }
                selected_map_style = style_map.get(
                    map_style, "mapbox://styles/mapbox/light-v8"
                )

                st.pydeck_chart(
                    pdk.Deck(
                        map_style=selected_map_style,
                        initial_view_state=pdk.ViewState(
                            latitude=37.0902,
                            longitude=-95.7129,
                            zoom=3.6,
                            pitch=30,
                        ),
                        layers=[
                            # Bubbles sized and colored by AUM
                            pdk.Layer(
                                "ScatterplotLayer",
                                data=state_df,
                                get_position=["lon", "lat"],
                                get_fill_color=[
                                    "color_r",
                                    "color_g",
                                    "color_b",
                                    "color_a",
                                ],
                                get_radius="radius",
                                radius_scale=6000,
                                radius_min_pixels=8,
                                radius_max_pixels=80,
                                pickable=True,
                                auto_highlight=True,
                            ),
                            # Optional labels
                            pdk.Layer(
                                "TextLayer",
                                data=state_df,
                                get_position=["lon", "lat"],
                                get_text="STATE",
                                get_color=[255, 255, 255, 200],
                                get_size=14,
                                get_alignment_baseline="bottom",
                            ),
                        ],
                        tooltip={
                            "html": "<b>{STATE}</b><br/>AUM: ${TOTAL_AUM:,.0f}<br/>Clients: {CLIENT_COUNT}<br/>Tier: {MARKET_TIER}",
                            "style": {
                                "backgroundColor": "rgba(0,0,0,0.8)",
                                "color": "white",
                            },
                        },
                    ),
                    use_container_width=True,
                    height=600,
                )
            else:
                st.info("No state-level data available to plot")

            # State insights
            st.markdown("**📊 Top Performing States**")
            top_states = geo_dist_df.nlargest(5, "TOTAL_AUM")
            for _, state in top_states.iterrows():
                st.markdown(
                    f"• **{state['STATE']}**: ${state['TOTAL_AUM']:,.0f} ({state['MARKET_TIER']})"
                )

        with map_tabs[1]:
            # 3D Metropolitan Scatter Plot
            @st.cache_data
            def get_metro_data():
                np.random.seed(42)
                return [
                    {
                        "metro": "New York-Newark",
                        "lat": 40.7128,
                        "lon": -74.0060,
                        "aum": 280000000,
                        "clients": 520,
                        "advisors": 45,
                    },
                    {
                        "metro": "Los Angeles-Long Beach",
                        "lat": 34.0522,
                        "lon": -118.2437,
                        "aum": 190000000,
                        "clients": 340,
                        "advisors": 32,
                    },
                    {
                        "metro": "Chicago-Naperville",
                        "lat": 41.8781,
                        "lon": -87.6298,
                        "aum": 165000000,
                        "clients": 295,
                        "advisors": 28,
                    },
                    {
                        "metro": "San Francisco-Oakland",
                        "lat": 37.7749,
                        "lon": -122.4194,
                        "aum": 220000000,
                        "clients": 280,
                        "advisors": 35,
                    },
                    {
                        "metro": "Boston-Cambridge",
                        "lat": 42.3601,
                        "lon": -71.0589,
                        "aum": 155000000,
                        "clients": 225,
                        "advisors": 25,
                    },
                    {
                        "metro": "Washington-Arlington",
                        "lat": 38.9072,
                        "lon": -77.0369,
                        "aum": 145000000,
                        "clients": 210,
                        "advisors": 23,
                    },
                    {
                        "metro": "Miami-Fort Lauderdale",
                        "lat": 25.7617,
                        "lon": -80.1918,
                        "aum": 110000000,
                        "clients": 195,
                        "advisors": 22,
                    },
                    {
                        "metro": "Seattle-Tacoma",
                        "lat": 47.6062,
                        "lon": -122.3321,
                        "aum": 125000000,
                        "clients": 180,
                        "advisors": 20,
                    },
                    {
                        "metro": "Denver-Aurora",
                        "lat": 39.7392,
                        "lon": -104.9903,
                        "aum": 95000000,
                        "clients": 155,
                        "advisors": 18,
                    },
                    {
                        "metro": "Atlanta-Sandy Springs",
                        "lat": 33.7490,
                        "lon": -84.3880,
                        "aum": 105000000,
                        "clients": 165,
                        "advisors": 19,
                    },
                ]

            metro_data_list = get_metro_data()

            # Convert to DataFrame and add calculated fields
            metro_df = pd.DataFrame(metro_data_list)
            metro_df["size"] = metro_df["aum"] / 1000000  # Scale for visualization
            metro_df["color_r"] = np.minimum(
                255, (255 * (metro_df["aum"] / 280000000)).astype(int)
            )
            metro_df["color_g"] = 100
            metro_df["color_b"] = np.maximum(
                50, (255 - 255 * (metro_df["aum"] / 280000000)).astype(int)
            )
            metro_df["color_a"] = 220

            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v8",
                    initial_view_state=pdk.ViewState(
                        latitude=39.8283,
                        longitude=-98.5795,
                        zoom=4,
                        pitch=40,
                        bearing=15,
                    ),
                    layers=[
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=metro_df,
                            get_position=["lon", "lat"],
                            get_fill_color=["color_r", "color_g", "color_b", "color_a"],
                            get_radius="size",
                            radius_scale=8000,
                            radius_min_pixels=15,
                            radius_max_pixels=60,
                            pickable=True,
                            auto_highlight=True,
                        )
                    ],
                    tooltip={
                        "html": "<b>{metro}</b><br/>"
                        "AUM: ${aum:,.0f}<br/>"
                        "Clients: {clients}<br/>"
                        "Advisors: {advisors}",
                        "style": {
                            "backgroundColor": "rgba(0,0,0,0.8)",
                            "color": "white",
                            "fontSize": "12px",
                        },
                    },
                ),
                use_container_width=True,
                height=500,
            )

        with map_tabs[2]:
            # Hexagonal Heat Map
            @st.cache_data
            def get_heatmap_data():
                np.random.seed(123)
                locations = []
                # Generate more data points for better heat map
                base_cities = [
                    (40.7128, -74.0060),
                    (34.0522, -118.2437),
                    (41.8781, -87.6298),
                    (37.7749, -122.4194),
                    (42.3601, -71.0589),
                    (38.9072, -77.0369),
                    (25.7617, -80.1918),
                    (47.6062, -122.3321),
                    (39.7392, -104.9903),
                    (33.7490, -84.3880),
                    (29.7604, -95.3698),
                    (33.4484, -112.0740),
                ]

                for base_lat, base_lon in base_cities:
                    # Add main location
                    locations.append(
                        {
                            "lat": base_lat,
                            "lon": base_lon,
                            "weight": np.random.uniform(50, 200),
                        }
                    )
                    # Add nearby scattered points
                    for _ in range(np.random.randint(8, 15)):
                        locations.append(
                            {
                                "lat": base_lat + np.random.normal(0, 0.5),
                                "lon": base_lon + np.random.normal(0, 0.8),
                                "weight": np.random.uniform(10, 80),
                            }
                        )

                return locations

            heatmap_data_list = get_heatmap_data()

            # Convert to DataFrame
            heatmap_df = pd.DataFrame(heatmap_data_list)

            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/dark-v11",
                    initial_view_state=pdk.ViewState(
                        latitude=39.8283,
                        longitude=-98.5795,
                        zoom=4,
                        pitch=30,
                    ),
                    layers=[
                        pdk.Layer(
                            "HexagonLayer",
                            data=heatmap_df,
                            get_position=["lon", "lat"],
                            get_weight="weight",
                            radius=50000,
                            elevation_scale=300,
                            elevation_range=[0, 1000],
                            pickable=True,
                            extruded=True,
                            coverage=0.8,
                            auto_highlight=True,
                        )
                    ],
                ),
                use_container_width=True,
                height=500,
            )

            st.info(
                "🔥 **Heat Map Insights**: Hexagonal aggregation shows client density and wealth concentration patterns across major metropolitan areas."
            )

        with map_tabs[3]:
            # Growth trajectory visualization
            @st.cache_data
            def get_growth_trajectory():
                np.random.seed(456)
                routes = []
                growth_centers = [
                    {
                        "name": "Silicon Valley",
                        "lat": 37.3861,
                        "lon": -122.0839,
                        "growth": 15.2,
                    },
                    {
                        "name": "Austin Tech",
                        "lat": 30.2672,
                        "lon": -97.7431,
                        "growth": 12.8,
                    },
                    {
                        "name": "Research Triangle",
                        "lat": 35.7796,
                        "lon": -78.6382,
                        "growth": 11.5,
                    },
                    {
                        "name": "Boston Innovation",
                        "lat": 42.3601,
                        "lon": -71.0589,
                        "growth": 9.7,
                    },
                    {
                        "name": "NYC Financial",
                        "lat": 40.7128,
                        "lon": -74.0060,
                        "growth": 8.3,
                    },
                ]

                # Create connections between growth centers
                for i, start in enumerate(growth_centers):
                    for j, end in enumerate(growth_centers[i + 1 :], i + 1):
                        routes.append(
                            {
                                "start_lat": start["lat"],
                                "start_lon": start["lon"],
                                "end_lat": end["lat"],
                                "end_lon": end["lon"],
                                "growth_flow": min(start["growth"], end["growth"]),
                                "color": [
                                    255,
                                    int(
                                        255 * (min(start["growth"], end["growth"]) / 15)
                                    ),
                                    0,
                                    120,
                                ],
                            }
                        )

                return growth_centers, routes

            growth_centers_list, growth_routes_list = get_growth_trajectory()

            # Convert to DataFrames
            growth_centers_df = pd.DataFrame(growth_centers_list)
            growth_routes_df = pd.DataFrame(growth_routes_list)

            st.pydeck_chart(
                pdk.Deck(
                    map_style="mapbox://styles/mapbox/light-v8",
                    initial_view_state=pdk.ViewState(
                        latitude=37.0902,
                        longitude=-95.7129,
                        zoom=4,
                        pitch=45,
                        bearing=20,
                    ),
                    layers=[
                        # Growth flow lines
                        pdk.Layer(
                            "ArcLayer",
                            data=growth_routes_df,
                            get_source_position=["start_lon", "start_lat"],
                            get_target_position=["end_lon", "end_lat"],
                            get_source_color="color",
                            get_target_color="color",
                            get_width="growth_flow",
                            width_scale=1000,
                            pickable=True,
                        ),
                        # Growth centers
                        pdk.Layer(
                            "ScatterplotLayer",
                            data=growth_centers_df,
                            get_position=["lon", "lat"],
                            get_fill_color=[255, 165, 0, 200],
                            get_radius="growth",
                            radius_scale=8000,
                            pickable=True,
                        ),
                    ],
                    tooltip={
                        "html": "<b>{name}</b><br/>Growth Rate: {growth}%",
                        "style": {"backgroundColor": "orange", "color": "white"},
                    },
                ),
                use_container_width=True,
                height=500,
            )

            st.success(
                "📈 **Growth Trajectories**: Arc visualization shows wealth migration patterns and emerging market connections across high-growth regions."
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

    # Advanced Climate Risk Visualization Suite
    st.markdown("**🌡️ Multi-Layer Climate Risk Analysis**")

    # Climate risk tabs
    climate_tabs = st.tabs(
        [
            "🌊 Flood Risk Zones",
            "🔥 Wildfire Risk",
            "🌪️ Storm Patterns",
            "📊 Risk Analytics",
        ]
    )

    with climate_tabs[0]:
        # Flood risk visualization
        @st.cache_data
        def get_flood_risk_data():
            np.random.seed(789)

            # Coastal and river cities with flood risk
            high_risk_areas = [
                {
                    "city": "Miami",
                    "lat": 25.7617,
                    "lon": -80.1918,
                    "risk": "Extreme",
                    "aum": 85000000,
                },
                {
                    "city": "New Orleans",
                    "lat": 29.9511,
                    "lon": -90.0715,
                    "risk": "Very High",
                    "aum": 45000000,
                },
                {
                    "city": "Houston",
                    "lat": 29.7604,
                    "lon": -95.3698,
                    "risk": "High",
                    "aum": 120000000,
                },
                {
                    "city": "Norfolk",
                    "lat": 36.8468,
                    "lon": -76.2852,
                    "risk": "High",
                    "aum": 25000000,
                },
                {
                    "city": "Charleston",
                    "lat": 32.7765,
                    "lon": -79.9311,
                    "risk": "High",
                    "aum": 35000000,
                },
                {
                    "city": "Tampa",
                    "lat": 27.9506,
                    "lon": -82.4572,
                    "risk": "Very High",
                    "aum": 65000000,
                },
                {
                    "city": "Jacksonville",
                    "lat": 30.3322,
                    "lon": -81.6557,
                    "risk": "Medium",
                    "aum": 55000000,
                },
            ]

            risk_colors = {
                "Extreme": [139, 0, 0, 220],  # Dark red
                "Very High": [255, 0, 0, 200],  # Red
                "High": [255, 140, 0, 180],  # Orange
                "Medium": [255, 215, 0, 160],  # Gold
                "Low": [50, 205, 50, 140],  # Green
            }

            for area in high_risk_areas:
                area["color"] = risk_colors[area["risk"]]
                area["radius"] = area["aum"] / 100000  # Scale radius by AUM

            return high_risk_areas

        flood_data_list = get_flood_risk_data()

        # Convert to DataFrame
        flood_df = pd.DataFrame(flood_data_list)

        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/satellite-v9",
                initial_view_state=pdk.ViewState(
                    latitude=29.0,
                    longitude=-87.0,
                    zoom=5,
                    pitch=30,
                    bearing=0,
                ),
                layers=[
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=flood_df,
                        get_position=["lon", "lat"],
                        get_fill_color="color",
                        get_radius="radius",
                        radius_scale=300,
                        radius_min_pixels=20,
                        radius_max_pixels=80,
                        pickable=True,
                        auto_highlight=True,
                    )
                ],
                tooltip={
                    "html": "<b>🌊 {city}</b><br/>"
                    "Flood Risk: {risk}<br/>"
                    "AUM at Risk: ${aum:,.0f}",
                    "style": {"backgroundColor": "navy", "color": "white"},
                },
            ),
            use_container_width=True,
            height=500,
        )

        total_flood_risk = flood_df["aum"].sum()
        st.warning(
            f"🌊 **Flood Risk Exposure**: ${total_flood_risk:,.0f} AUM in flood-prone areas"
        )

    with climate_tabs[1]:
        # Wildfire risk visualization
        @st.cache_data
        def get_wildfire_risk_data():
            np.random.seed(321)

            # Western US cities with wildfire risk
            fire_risk_areas = [
                {
                    "city": "Los Angeles",
                    "lat": 34.0522,
                    "lon": -118.2437,
                    "risk": "Extreme",
                    "aum": 180000000,
                },
                {
                    "city": "San Francisco",
                    "lat": 37.7749,
                    "lon": -122.4194,
                    "risk": "Very High",
                    "aum": 220000000,
                },
                {
                    "city": "Sacramento",
                    "lat": 38.5816,
                    "lon": -121.4944,
                    "risk": "High",
                    "aum": 85000000,
                },
                {
                    "city": "San Diego",
                    "lat": 32.7157,
                    "lon": -117.1611,
                    "risk": "High",
                    "aum": 95000000,
                },
                {
                    "city": "Phoenix",
                    "lat": 33.4484,
                    "lon": -112.0740,
                    "risk": "Medium",
                    "aum": 75000000,
                },
                {
                    "city": "Denver",
                    "lat": 39.7392,
                    "lon": -104.9903,
                    "risk": "Medium",
                    "aum": 95000000,
                },
                {
                    "city": "Portland",
                    "lat": 45.5152,
                    "lon": -122.6784,
                    "risk": "High",
                    "aum": 65000000,
                },
            ]

            fire_colors = {
                "Extreme": [178, 34, 34, 220],  # Dark red
                "Very High": [255, 69, 0, 200],  # Red orange
                "High": [255, 140, 0, 180],  # Orange
                "Medium": [255, 215, 0, 160],  # Gold
                "Low": [154, 205, 50, 140],  # Yellow green
            }

            for area in fire_risk_areas:
                area["color"] = fire_colors[area["risk"]]
                area["elevation"] = area["aum"] / 1000000  # Scale height by AUM

            return fire_risk_areas

        wildfire_data_list = get_wildfire_risk_data()

        # Convert to DataFrame
        wildfire_df = pd.DataFrame(wildfire_data_list)

        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/outdoors-v12",
                initial_view_state=pdk.ViewState(
                    latitude=37.0,
                    longitude=-119.0,
                    zoom=5,
                    pitch=50,
                    bearing=30,
                ),
                layers=[
                    pdk.Layer(
                        "ColumnLayer",
                        data=wildfire_df,
                        get_position=["lon", "lat"],
                        get_elevation="elevation",
                        elevation_scale=800,
                        get_fill_color="color",
                        radius=25000,
                        pickable=True,
                        auto_highlight=True,
                    )
                ],
                tooltip={
                    "html": "<b>🔥 {city}</b><br/>"
                    "Fire Risk: {risk}<br/>"
                    "AUM at Risk: ${aum:,.0f}",
                    "style": {"backgroundColor": "darkred", "color": "white"},
                },
            ),
            use_container_width=True,
            height=500,
        )

        total_fire_risk = wildfire_df["aum"].sum()
        st.error(
            f"🔥 **Wildfire Risk Exposure**: ${total_fire_risk:,.0f} AUM in fire-prone areas"
        )

    with climate_tabs[2]:
        # Storm pattern visualization
        @st.cache_data
        def get_storm_pattern_data():
            np.random.seed(654)
            storm_paths = []

            # Hurricane and tornado prone areas
            storm_areas = [
                {
                    "city": "Miami",
                    "lat": 25.7617,
                    "lon": -80.1918,
                    "storm_type": "Hurricane",
                    "frequency": 8.5,
                },
                {
                    "city": "Tampa",
                    "lat": 27.9506,
                    "lon": -82.4572,
                    "storm_type": "Hurricane",
                    "frequency": 7.2,
                },
                {
                    "city": "New Orleans",
                    "lat": 29.9511,
                    "lon": -90.0715,
                    "storm_type": "Hurricane",
                    "frequency": 6.8,
                },
                {
                    "city": "Oklahoma City",
                    "lat": 35.4676,
                    "lon": -97.5164,
                    "storm_type": "Tornado",
                    "frequency": 12.3,
                },
                {
                    "city": "Dallas",
                    "lat": 32.7767,
                    "lon": -96.7970,
                    "storm_type": "Tornado",
                    "frequency": 9.1,
                },
                {
                    "city": "Kansas City",
                    "lat": 39.0997,
                    "lon": -94.5786,
                    "storm_type": "Tornado",
                    "frequency": 8.7,
                },
                {
                    "city": "Atlanta",
                    "lat": 33.7490,
                    "lon": -84.3880,
                    "storm_type": "Severe Storm",
                    "frequency": 15.2,
                },
            ]

            # Create storm path connections
            for i, start in enumerate(storm_areas[:-1]):
                end = storm_areas[i + 1]
                storm_paths.append(
                    {
                        "start_lat": start["lat"],
                        "start_lon": start["lon"],
                        "end_lat": end["lat"],
                        "end_lon": end["lon"],
                        "intensity": (start["frequency"] + end["frequency"]) / 2,
                        "color": [255, int(255 * (start["frequency"] / 15)), 0, 150],
                    }
                )

            return storm_areas, storm_paths

        storm_areas_list, storm_paths_list = get_storm_pattern_data()

        # Convert to DataFrames
        storm_areas_df = pd.DataFrame(storm_areas_list)
        storm_paths_df = pd.DataFrame(storm_paths_list)

        st.pydeck_chart(
            pdk.Deck(
                map_style="mapbox://styles/mapbox/dark-v11",
                initial_view_state=pdk.ViewState(
                    latitude=32.0,
                    longitude=-90.0,
                    zoom=4,
                    pitch=40,
                    bearing=10,
                ),
                layers=[
                    # Storm paths
                    pdk.Layer(
                        "ArcLayer",
                        data=storm_paths_df,
                        get_source_position=["start_lon", "start_lat"],
                        get_target_position=["end_lon", "end_lat"],
                        get_source_color="color",
                        get_target_color="color",
                        get_width="intensity",
                        width_scale=500,
                        pickable=True,
                    ),
                    # Storm centers
                    pdk.Layer(
                        "ScatterplotLayer",
                        data=storm_areas_df,
                        get_position=["lon", "lat"],
                        get_fill_color=[255, 255, 0, 200],
                        get_radius="frequency",
                        radius_scale=5000,
                        pickable=True,
                    ),
                ],
                tooltip={
                    "html": "<b>🌪️ {city}</b><br/>"
                    "Storm Type: {storm_type}<br/>"
                    "Annual Frequency: {frequency}",
                    "style": {"backgroundColor": "purple", "color": "white"},
                },
            ),
            use_container_width=True,
            height=500,
        )

        st.info(
            "🌪️ **Storm Pattern Analysis**: Arc visualization shows seasonal storm corridors and frequency patterns affecting portfolio locations."
        )

    with climate_tabs[3]:
        # Risk analytics dashboard
        st.markdown("**📊 Comprehensive Risk Analytics**")

        # Create combined risk analysis
        risk_summary = {
            "Risk Type": ["Flood", "Wildfire", "Storm", "Combined"],
            "AUM at Risk": [430000000, 815000000, 320000000, 1200000000],
            "Mitigation Cost": [12000000, 28000000, 8000000, 35000000],
            "Insurance Coverage": [85, 72, 91, 79],
        }

        # Multi-metric visualization
        fig = go.Figure()

        # AUM at Risk bars
        fig.add_trace(
            go.Bar(
                name="AUM at Risk ($M)",
                x=risk_summary["Risk Type"],
                y=[x / 1000000 for x in risk_summary["AUM at Risk"]],
                yaxis="y",
                marker_color=["#4472C4", "#E70013", "#FFC000", "#70AD47"],
                opacity=0.8,
            )
        )

        # Insurance coverage line
        fig.add_trace(
            go.Scatter(
                name="Insurance Coverage (%)",
                x=risk_summary["Risk Type"],
                y=risk_summary["Insurance Coverage"],
                yaxis="y2",
                mode="lines+markers",
                marker=dict(size=10, color="red"),
                line=dict(width=3, color="red"),
            )
        )

        fig.update_layout(
            title="Climate Risk Portfolio Analysis",
            xaxis_title="Risk Category",
            yaxis=dict(title="AUM at Risk ($M)", side="left"),
            yaxis2=dict(
                title="Insurance Coverage (%)",
                side="right",
                overlaying="y",
                range=[0, 100],
            ),
            height=500,
            hovermode="x unified",
        )

        st.plotly_chart(fig, use_container_width=True)

        # Risk mitigation recommendations
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**🛡️ Risk Mitigation Strategies**")
            st.markdown(
                """
            **Immediate Actions:**
            • Increase insurance coverage for wildfire zones (72% → 85%)
            • Implement flood-resistant investment strategies
            • Diversify geographic portfolio concentration

            **Medium-term Planning:**
            • Climate stress testing for all portfolios
            • ESG integration in investment selection
            • Alternative asset allocation in low-risk regions
            """
            )

        with col2:
            st.markdown("**📈 Risk-Adjusted Returns**")
            risk_adjusted_data = {
                "Region": ["Low Risk", "Medium Risk", "High Risk", "Very High Risk"],
                "Expected Return": [6.2, 7.8, 9.1, 11.3],
                "Climate Risk Factor": [1.0, 1.15, 1.35, 1.65],
            }

            fig_ra = px.scatter(
                x=risk_adjusted_data["Climate Risk Factor"],
                y=risk_adjusted_data["Expected Return"],
                size=[50, 75, 100, 125],
                color=risk_adjusted_data["Region"],
                title="Risk vs Return Analysis",
                labels={"x": "Climate Risk Factor", "y": "Expected Return (%)"},
            )
            st.plotly_chart(fig_ra, use_container_width=True)

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
