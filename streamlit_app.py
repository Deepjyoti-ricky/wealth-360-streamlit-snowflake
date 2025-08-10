import os
from typing import Dict, Optional

import pandas as pd
import streamlit as st
import plotly.express as px
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session


# -----------------------------
# Configuration and Connection (Snowpark-first for Streamlit in Snowflake)
# -----------------------------

def _read_secrets_prefixed(prefix: str) -> Dict[str, Optional[str]]:
    values: Dict[str, Optional[str]] = {}
    # Prefer Streamlit secrets if available, fall back to environment variables
    def get_val(key: str) -> Optional[str]:
        if "secrets" in st.__dict__:
            # Try both upper and lower keys: SNOWFLAKE / snowflake
            if prefix in st.secrets:
                section = st.secrets[prefix]
                return section.get(key)
            if prefix.lower() in st.secrets:
                section = st.secrets[prefix.lower()]
                return section.get(key)
        return os.environ.get(f"{prefix}_{key}")

    for key in [
        "USER",
        "PASSWORD",
        "ACCOUNT",
        "WAREHOUSE",
        "DATABASE",
        "SCHEMA",
        "ROLE",
    ]:
        values[key] = get_val(key)
    return values


@st.cache_resource(show_spinner=False)
def get_snowflake_session() -> Session:
    # 1) If running inside Streamlit in Snowflake, use the active session
    try:
        sess = get_active_session()
        if sess is not None:
            # Optionally align db/schema from secrets if provided
            cfg = _read_secrets_prefixed("SNOWFLAKE")
            try:
                if cfg.get("DATABASE"):
                    sess.use_database(cfg["DATABASE"])
                if cfg.get("SCHEMA"):
                    sess.use_schema(cfg["SCHEMA"])
                if cfg.get("WAREHOUSE"):
                    sess.use_warehouse(cfg["WAREHOUSE"])
                if cfg.get("ROLE"):
                    sess.use_role(cfg["ROLE"])
            except Exception:
                # Ignore if not permitted to change context
                pass
            return sess
    except Exception:
        pass

    # 2) Local/dev fallback via secrets (requires full creds)
    cfg = _read_secrets_prefixed("SNOWFLAKE")
    required = ["USER", "PASSWORD", "ACCOUNT", "WAREHOUSE", "DATABASE", "SCHEMA"]
    missing = [k for k in required if not cfg.get(k)]
    if missing:
        raise RuntimeError(
            "Snowflake session not available and missing local secrets: "
            + ", ".join(missing)
        )
    connection_parameters = {
        "account": cfg["ACCOUNT"],
        "user": cfg["USER"],
        "password": cfg["PASSWORD"],
        "warehouse": cfg["WAREHOUSE"],
        "database": cfg.get("DATABASE", "FSI_DEMOS"),
        "schema": cfg.get("SCHEMA", "WEALTH_360"),
    }
    if cfg.get("ROLE"):
        connection_parameters["role"] = cfg["ROLE"]
    return Session.builder.configs(connection_parameters).create()


@st.cache_data(ttl=600, show_spinner=False)
def run_query(sql: str) -> pd.DataFrame:
    session = get_snowflake_session()
    return session.sql(sql).to_pandas()


# -----------------------------
# Reusable Query Helpers
# -----------------------------

def get_global_kpis() -> Dict[str, Optional[float]]:
    # Clients
    clients_df = run_query("SELECT COUNT(DISTINCT CLIENT_ID) AS CNT FROM CLIENTS")
    num_clients = int(clients_df.loc[0, "CNT"]) if not clients_df.empty else 0

    # Advisors
    advisors_df = run_query("SELECT COUNT(DISTINCT ADVISOR_ID) AS CNT FROM ADVISORS")
    num_advisors = int(advisors_df.loc[0, "CNT"]) if not advisors_df.empty else 0

    # AUM (latest non-cash market value across all portfolios)
    aum_sql = """
        WITH latest AS (
            SELECT PORTFOLIO_ID, MAX(TIMESTAMP) AS MAX_TS
            FROM POSITION_HISTORY
            GROUP BY PORTFOLIO_ID
        )
        SELECT COALESCE(SUM(ph.MARKET_VALUE), 0) AS AUM
        FROM POSITION_HISTORY ph
        JOIN latest lt
          ON ph.PORTFOLIO_ID = lt.PORTFOLIO_ID AND ph.TIMESTAMP = lt.MAX_TS
        WHERE ph.TICKER <> 'CASH'
    """
    aum_df = run_query(aum_sql)
    aum = float(aum_df.loc[0, "AUM"]) if not aum_df.empty else 0.0

    # YTD growth (verified query style)
    ytd_sql = """
        WITH port AS (
            SELECT p.PORTFOLIO_ID,
                   TO_TIMESTAMP(DATE_TRUNC('YEAR', CURRENT_DATE)) AS START_OF_YEAR,
                   TO_TIMESTAMP(CURRENT_DATE) AS END_DATE
            FROM PORTFOLIOS AS p
        ),
        daily_portfolio_value AS (
            SELECT ph.PORTFOLIO_ID, ph.TIMESTAMP, SUM(ph.MARKET_VALUE) AS TOT_MARKET_VALUE
            FROM POSITION_HISTORY AS ph
            WHERE ph.TICKER <> 'CASH'
            GROUP BY 1,2
        ),
        start_of_year_value AS (
            SELECT 1 AS JOIN_ID, p.START_OF_YEAR, SUM(TOT_MARKET_VALUE) AS TOT_MARKET_VALUE
            FROM port AS p
            ASOF JOIN daily_portfolio_value AS pv
            MATCH_CONDITION (p.START_OF_YEAR >= pv.TIMESTAMP)
            ON p.PORTFOLIO_ID = pv.PORTFOLIO_ID
            GROUP BY 1,2
        ),
        latest_value AS (
            SELECT 1 AS JOIN_ID, p.END_DATE, SUM(TOT_MARKET_VALUE) AS TOT_MARKET_VALUE
            FROM port AS p
            ASOF JOIN daily_portfolio_value AS pv
            MATCH_CONDITION (p.END_DATE >= pv.TIMESTAMP)
            ON p.PORTFOLIO_ID = pv.PORTFOLIO_ID
            GROUP BY 1,2
        )
        SELECT (l.TOT_MARKET_VALUE - s.TOT_MARKET_VALUE)
               / NULLIF(NULLIF(s.TOT_MARKET_VALUE, 0), 0) AS YTD_GROWTH_PCT
        FROM latest_value AS l
        JOIN start_of_year_value AS s ON (l.JOIN_ID = s.JOIN_ID)
    """
    ytd_df = run_query(ytd_sql)
    ytd_growth_pct = float(ytd_df.loc[0, "YTD_GROWTH_PCT"]) if not ytd_df.empty else None

    return {
        "num_clients": num_clients,
        "num_advisors": num_advisors,
        "aum": aum,
        "ytd_growth_pct": ytd_growth_pct,
    }


def get_hnw_low_engagement(threshold_days: int = 180, net_worth_threshold: int = 1_000_000) -> pd.DataFrame:
    sql = f"""
        WITH last_interaction AS (
            SELECT i.CLIENT_ID, MAX(i.TIMESTAMP) AS LAST_INTERACTION_DATE
            FROM INTERACTIONS AS i
            GROUP BY i.CLIENT_ID
        )
        SELECT DISTINCT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME, c.NET_WORTH_ESTIMATE,
               li.LAST_INTERACTION_DATE
        FROM CLIENTS AS c
        LEFT OUTER JOIN last_interaction AS li ON c.CLIENT_ID = li.CLIENT_ID
        WHERE c.NET_WORTH_ESTIMATE > {net_worth_threshold}
          AND (li.LAST_INTERACTION_DATE IS NULL OR li.LAST_INTERACTION_DATE < DATEADD(DAY, -{threshold_days}, CURRENT_DATE))
        ORDER BY c.NET_WORTH_ESTIMATE DESC NULLS LAST
    """
    return run_query(sql)


def get_advisor_productivity(window_days: int = 90) -> pd.DataFrame:
    sql = f"""
        WITH latest AS (
            SELECT PORTFOLIO_ID, MAX(TIMESTAMP) AS MAX_TS
            FROM POSITION_HISTORY
            GROUP BY PORTFOLIO_ID
        ),
        portfolio_aum AS (
            SELECT ph.PORTFOLIO_ID, SUM(ph.MARKET_VALUE) AS PORTFOLIO_AUM
            FROM POSITION_HISTORY ph
            JOIN latest lt
              ON ph.PORTFOLIO_ID = lt.PORTFOLIO_ID AND ph.TIMESTAMP = lt.MAX_TS
            WHERE ph.TICKER <> 'CASH'
            GROUP BY 1
        ),
        advisor_clients AS (
            SELECT r.ADVISOR_ID, r.CLIENT_ID
            FROM ADVISOR_CLIENT_RELATIONSHIPS r
            WHERE r.STATUS = 'Active'
        ),
        advisor_portfolios AS (
            SELECT ac.ADVISOR_ID, p.PORTFOLIO_ID
            FROM advisor_clients ac
            JOIN PORTFOLIOS p ON p.CLIENT_ID = ac.CLIENT_ID
        ),
        recent_interactions AS (
            SELECT i.ADVISOR_ID, COUNT(*) AS INTERACTIONS_90D
            FROM INTERACTIONS i
            WHERE i.TIMESTAMP >= DATEADD(DAY, -{window_days}, CURRENT_DATE)
            GROUP BY 1
        )
        SELECT ap.ADVISOR_ID,
               adv.NAME AS ADVISOR_NAME,
               COUNT(DISTINCT ap.PORTFOLIO_ID) AS NUM_PORTFOLIOS,
               COUNT(DISTINCT ac2.CLIENT_ID) AS NUM_CLIENTS,
               COALESCE(SUM(pa.PORTFOLIO_AUM), 0) AS TOTAL_AUM,
               COALESCE(ri.INTERACTIONS_90D, 0) AS INTERACTIONS_90D
        FROM advisor_portfolios ap
        JOIN advisor_clients ac2 ON ap.ADVISOR_ID = ac2.ADVISOR_ID
        LEFT JOIN portfolio_aum pa ON ap.PORTFOLIO_ID = pa.PORTFOLIO_ID
        JOIN ADVISORS adv ON adv.ADVISOR_ID = ap.ADVISOR_ID
        LEFT JOIN recent_interactions ri ON ri.ADVISOR_ID = ap.ADVISOR_ID
        GROUP BY ap.ADVISOR_ID, adv.NAME, ri.INTERACTIONS_90D
        ORDER BY TOTAL_AUM DESC
    """
    return run_query(sql)


def get_asset_allocation_latest() -> pd.DataFrame:
    sql = """
        WITH latest AS (
            SELECT PORTFOLIO_ID, MAX(TIMESTAMP) AS MAX_TS
            FROM POSITION_HISTORY
            GROUP BY PORTFOLIO_ID
        )
        SELECT ph.ASSET_CLASS, SUM(ph.MARKET_VALUE) AS TOTAL_VALUE
        FROM POSITION_HISTORY ph
        JOIN latest lt
          ON ph.PORTFOLIO_ID = lt.PORTFOLIO_ID AND ph.TIMESTAMP = lt.MAX_TS
        WHERE ph.TICKER <> 'CASH'
        GROUP BY ph.ASSET_CLASS
        ORDER BY TOTAL_VALUE DESC
    """
    return run_query(sql)


def get_market_events_impact() -> pd.DataFrame:
    sql = """
        WITH daily_portfolio_value AS (
            SELECT ph.PORTFOLIO_ID, ph.TIMESTAMP, SUM(ph.MARKET_VALUE) AS TOT_MARKET_VALUE
            FROM POSITION_HISTORY ph
            WHERE ph.TICKER <> 'CASH'
            GROUP BY 1,2
        ),
        all_ports AS (
            SELECT DISTINCT PORTFOLIO_ID FROM PORTFOLIOS
        ),
        start_vals AS (
            SELECT me.EVENT_ID, me.EVENT_NAME, me.START_DATE,
                   SUM(pv.TOT_MARKET_VALUE) AS START_AUM
            FROM MARKET_EVENTS me
            CROSS JOIN all_ports p
            ASOF JOIN daily_portfolio_value pv
            MATCH_CONDITION (me.START_DATE >= pv.TIMESTAMP)
            ON pv.PORTFOLIO_ID = p.PORTFOLIO_ID
            GROUP BY me.EVENT_ID, me.EVENT_NAME, me.START_DATE
        ),
        end_vals AS (
            SELECT me.EVENT_ID, me.END_DATE,
                   SUM(pv.TOT_MARKET_VALUE) AS END_AUM
            FROM MARKET_EVENTS me
            CROSS JOIN all_ports p
            ASOF JOIN daily_portfolio_value pv
            MATCH_CONDITION (me.END_DATE >= pv.TIMESTAMP)
            ON pv.PORTFOLIO_ID = p.PORTFOLIO_ID
            GROUP BY me.EVENT_ID, me.END_DATE
        )
        SELECT s.EVENT_ID, s.EVENT_NAME, s.START_DATE, e.END_DATE,
               s.START_AUM, e.END_AUM,
               (e.END_AUM - s.START_AUM) AS CHANGE_AUM,
               (e.END_AUM - s.START_AUM) / NULLIF(NULLIF(s.START_AUM, 0), 0) AS CHANGE_PCT
        FROM start_vals s
        JOIN end_vals e ON s.EVENT_ID = e.EVENT_ID
        ORDER BY s.START_DATE
    """
    return run_query(sql)


def get_suitability_mismatches() -> pd.DataFrame:
    sql = """
        SELECT c.CLIENT_ID,
               c.FIRST_NAME,
               c.LAST_NAME,
               c.RISK_TOLERANCE,
               p.PORTFOLIO_ID,
               p.STRATEGY_TYPE
        FROM CLIENTS c
        JOIN PORTFOLIOS p ON p.CLIENT_ID = c.CLIENT_ID
    """
    df = run_query(sql)
    if df.empty:
        return df

    # Simple suitability matrix
    allowed = {
        "Conservative": {"Conservative", "Balanced"},
        "Moderate": {"Balanced", "Moderate", "Growth"},
        "Balanced": {"Balanced", "Moderate", "Growth"},
        "Growth": {"Growth", "Aggressive Growth"},
        "Aggressive Growth": {"Aggressive Growth"},
    }
    def is_mismatch(row) -> bool:
        risk = row.get("RISK_TOLERANCE") or ""
        strat = row.get("STRATEGY_TYPE") or ""
        if risk not in allowed:
            return False
        return strat not in allowed[risk]

    df["SUITABILITY_MISMATCH"] = df.apply(is_mismatch, axis=1)
    return df[df["SUITABILITY_MISMATCH"]]


def get_concentration_breaches(threshold_pct: float = 0.3) -> pd.DataFrame:
    sql = """
        WITH latest AS (
            SELECT PORTFOLIO_ID, MAX(TIMESTAMP) AS MAX_TS
            FROM POSITION_HISTORY
            GROUP BY PORTFOLIO_ID
        ),
        latest_positions AS (
            SELECT ph.PORTFOLIO_ID, ph.TICKER, ph.MARKET_VALUE
            FROM POSITION_HISTORY ph
            JOIN latest lt
              ON ph.PORTFOLIO_ID = lt.PORTFOLIO_ID AND ph.TIMESTAMP = lt.MAX_TS
            WHERE ph.TICKER <> 'CASH'
        ),
        totals AS (
            SELECT PORTFOLIO_ID, SUM(MARKET_VALUE) AS TOTAL
            FROM latest_positions
            GROUP BY 1
        )
        SELECT lp.PORTFOLIO_ID, lp.TICKER,
               lp.MARKET_VALUE,
               t.TOTAL,
               lp.MARKET_VALUE / NULLIF(NULLIF(t.TOTAL, 0), 0) AS PCT_OF_PORTFOLIO
        FROM latest_positions lp
        JOIN totals t USING (PORTFOLIO_ID)
        WHERE lp.MARKET_VALUE / NULLIF(NULLIF(t.TOTAL, 0), 0) >= {threshold_pct}
        ORDER BY PCT_OF_PORTFOLIO DESC
    """
    return run_query(sql)


def get_interactions_summary(window_days: int = 365) -> Dict[str, pd.DataFrame]:
    by_channel = run_query(
        f"""
        SELECT CHANNEL, COUNT(*) AS CNT
        FROM INTERACTIONS
        WHERE TIMESTAMP >= DATEADD(DAY, -{window_days}, CURRENT_DATE)
        GROUP BY 1
        ORDER BY CNT DESC
        """
    )
    by_type = run_query(
        f"""
        SELECT INTERACTION_TYPE, COUNT(*) AS CNT
        FROM INTERACTIONS
        WHERE TIMESTAMP >= DATEADD(DAY, -{window_days}, CURRENT_DATE)
        GROUP BY 1
        ORDER BY CNT DESC
        """
    )
    complaints = run_query(
        f"""
        SELECT DATE_TRUNC('MONTH', TIMESTAMP) AS MONTH, COUNT(*) AS COMPLAINTS
        FROM INTERACTIONS
        WHERE INTERACTION_TYPE = 'Complaint'
          AND TIMESTAMP >= DATEADD(DAY, -{window_days}, CURRENT_DATE)
        GROUP BY 1
        ORDER BY 1
        """
    )
    top_clients = run_query(
        f"""
        SELECT CLIENT_ID, COUNT(*) AS INTERACTIONS
        FROM INTERACTIONS
        WHERE TIMESTAMP >= DATEADD(DAY, -{window_days}, CURRENT_DATE)
        GROUP BY 1
        ORDER BY INTERACTIONS DESC
        LIMIT 20
        """
    )
    return {
        "by_channel": by_channel,
        "by_type": by_type,
        "complaints": complaints,
        "top_clients": top_clients,
    }


# -----------------------------
# UI Layout
# -----------------------------

st.set_page_config(
    page_title="BFSI Wealth 360 – Analytics",
    page_icon="💹",
    layout="wide",
)

st.title("BFSI Wealth 360 – Analytics & Use Cases")
st.caption("Powered by Snowflake – Schema: FSI_DEMOS.WEALTH_360")

# Sidebar – connection status and filters
with st.sidebar:
    st.header("Configuration")
    try:
        _ = get_snowflake_session()
        st.success("Connected to Snowflake")
    except Exception as e:
        st.error("Snowflake connection failed. Configure secrets to continue.")
        st.exception(e)
        st.stop()

    st.divider()
    st.subheader("Filters")
    hnw_threshold = st.number_input("HNW Threshold (USD)", min_value=100000, value=1_000_000, step=100000)
    low_engagement_days = st.slider("Low Engagement if last touch older than (days)", min_value=30, max_value=365, value=180, step=15)
    advisor_window_days = st.slider("Advisor activity window (days)", min_value=30, max_value=365, value=90, step=15)
    interactions_window_days = st.slider("Engagement window (days)", min_value=30, max_value=1095, value=365, step=30)
    concentration_threshold = st.slider("Concentration threshold (%)", min_value=5, max_value=80, value=30, step=5) / 100.0


tabs = st.tabs([
    "Overview",
    "HNW Retention",
    "Advisor Productivity",
    "Portfolio Performance",
    "Compliance & Risk",
    "Market Events Impact",
    "Digital Engagement",
])


# Overview
with tabs[0]:
    st.subheader("Firm Overview")
    kpis = get_global_kpis()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clients", f"{kpis['num_clients']:,}")
    c2.metric("Advisors", f"{kpis['num_advisors']:,}")
    c3.metric("AUM (latest)", f"${kpis['aum']:,.0f}")
    if kpis["ytd_growth_pct"] is not None:
        c4.metric("YTD Growth", f"{kpis['ytd_growth_pct']*100:.2f}%")
    else:
        c4.metric("YTD Growth", "N/A")

    st.divider()
    st.subheader("Asset Allocation (Latest Snapshot)")
    alloc_df = get_asset_allocation_latest()
    if not alloc_df.empty:
        fig = px.pie(alloc_df, names="ASSET_CLASS", values="TOTAL_VALUE", hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No allocation data available.")


# HNW Retention
with tabs[1]:
    st.subheader("High Net Worth – Low Engagement Clients")
    hnw_df = get_hnw_low_engagement(threshold_days=low_engagement_days, net_worth_threshold=int(hnw_threshold))
    if hnw_df.empty:
        st.success("No HNW clients currently flagged for low engagement.")
    else:
        st.dataframe(hnw_df, use_container_width=True)


# Advisor Productivity
with tabs[2]:
    st.subheader("Advisor Productivity & Coverage")
    adv_df = get_advisor_productivity(window_days=advisor_window_days)
    if not adv_df.empty:
        st.dataframe(adv_df, use_container_width=True)
        fig = px.bar(adv_df, x="ADVISOR_NAME", y="TOTAL_AUM", title="AUM by Advisor", text_auto=True)
        fig.update_layout(xaxis_title="Advisor", yaxis_title="Total AUM (USD)")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No advisor productivity data available.")


# Portfolio Performance
with tabs[3]:
    st.subheader("Firm-Level Performance (YTD)")
    ytd = get_global_kpis().get("ytd_growth_pct")
    if ytd is not None:
        st.metric("YTD Growth (Firm AUM)", f"{ytd*100:.2f}%")
    else:
        st.info("YTD growth unavailable.")

    st.divider()
    st.subheader("Allocation – Latest Snapshot")
    alloc_df = get_asset_allocation_latest()
    if not alloc_df.empty:
        fig2 = px.bar(alloc_df, x="ASSET_CLASS", y="TOTAL_VALUE", title="Allocation by Asset Class")
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No allocation data available.")


# Compliance & Risk
with tabs[4]:
    st.subheader("Suitability Mismatches")
    mism = get_suitability_mismatches()
    if mism.empty:
        st.success("No suitability mismatches detected.")
    else:
        st.dataframe(mism[["CLIENT_ID", "FIRST_NAME", "LAST_NAME", "RISK_TOLERANCE", "PORTFOLIO_ID", "STRATEGY_TYPE"]], use_container_width=True)

    st.divider()
    st.subheader("Concentration Breaches")
    conc = get_concentration_breaches(threshold_pct=concentration_threshold)
    if conc.empty:
        st.success("No concentration breaches at the selected threshold.")
    else:
        conc_disp = conc.copy()
        conc_disp["PCT_OF_PORTFOLIO"] = (conc_disp["PCT_OF_PORTFOLIO"] * 100).round(2)
        st.dataframe(conc_disp, use_container_width=True)


# Market Events Impact
with tabs[5]:
    st.subheader("Market Events – AUM Impact")
    me = get_market_events_impact()
    if me.empty:
        st.info("No market event impact data available.")
    else:
        st.dataframe(me, use_container_width=True)
        fig = px.bar(me, x="EVENT_NAME", y="CHANGE_PCT", title="AUM % Change by Market Event")
        st.plotly_chart(fig, use_container_width=True)


# Digital Engagement
with tabs[6]:
    st.subheader("Engagement by Channel and Type")
    sums = get_interactions_summary(window_days=interactions_window_days)
    if not sums["by_channel"].empty:
        fig = px.bar(sums["by_channel"], x="CHANNEL", y="CNT", title="Interactions by Channel")
        st.plotly_chart(fig, use_container_width=True)
    if not sums["by_type"].empty:
        fig2 = px.bar(sums["by_type"], x="INTERACTION_TYPE", y="CNT", title="Interactions by Type")
        st.plotly_chart(fig2, use_container_width=True)
    if not sums["complaints"].empty:
        fig3 = px.line(sums["complaints"], x="MONTH", y="COMPLAINTS", title="Complaints Over Time")
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()
    st.subheader("Top Clients by Interactions")
    st.dataframe(sums["top_clients"], use_container_width=True)

