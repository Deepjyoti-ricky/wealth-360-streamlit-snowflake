"""
Wealth 360 Analytics - Professional BFSI Streamlit Application

This application provides comprehensive analytics for Banking, Financial Services,
and Insurance (BFSI) use cases using Snowflake's wealth management dataset.

Author: Deepjyoti Dev, Senior Data Cloud Architect, Snowflake GXC Team
Contact: deepjyoti.dev@snowflake.com | +917205672310
Version: 1.0.0
License: MIT
"""

import logging
import os
from typing import Any, Dict, Optional

import pandas as pd
import plotly.express as px
import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.context import get_active_session

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------------------
# Configuration and Connection (Snowpark-first for Streamlit in Snowflake)
# -----------------------------


def _read_secrets_prefixed(prefix: str) -> Dict[str, Optional[str]]:
    """
    Read configuration secrets with a given prefix.
    Safe for use in both Streamlit in Snowflake and local environments.

    Args:
        prefix: Configuration section prefix (e.g., 'SNOWFLAKE')

    Returns:
        Dictionary of configuration values
    """
    values: Dict[str, Optional[str]] = {}

    def get_val(key: str) -> Optional[str]:
        # First try environment variables (always safe)
        env_val = os.environ.get(f"{prefix}_{key}")
        if env_val:
            return env_val

        # Only try Streamlit secrets if we're in a local development environment
        # Skip secrets entirely in Streamlit in Snowflake to avoid errors
        try:
            # Check if we're likely in Streamlit in Snowflake by looking for active session
            from snowflake.snowpark.context import get_active_session

            get_active_session()
            # If we get here without exception, we're in Streamlit in Snowflake
            # Don't try to access secrets
            return None
        except Exception:
            # We're in local development, try secrets
            try:
                if hasattr(st, "secrets"):
                    if prefix in st.secrets:
                        section = st.secrets[prefix]
                        return section.get(key)
                    if prefix.lower() in st.secrets:
                        section = st.secrets[prefix.lower()]
                        return section.get(key)
            except Exception:
                # Secrets not available or accessible
                pass

        return None

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
    """
    Get Snowflake session - prioritizes active session in Streamlit in Snowflake,
    falls back to credentials-based session for local development.

    Returns:
        Snowflake Snowpark Session object

    Raises:
        RuntimeError: If session cannot be established
    """
    # 1) If running inside Streamlit in Snowflake, use the active session
    try:
        sess = get_active_session()
        if sess is not None:
            logger.info("✅ Using active Snowflake session from Streamlit in Snowflake")

            # For Streamlit in Snowflake, use the current session context as-is
            # Context overrides are optional and only used for local development
            logger.info("Using current session context from Streamlit in Snowflake")

            return sess
    except Exception as e:
        logger.info(f"Active session not available, trying credentials: {e}")

    # 2) Local/dev fallback via secrets (requires full creds)
    logger.info("Attempting local session with credentials")
    try:
        cfg = _read_secrets_prefixed("SNOWFLAKE")
        required = ["USER", "PASSWORD", "ACCOUNT", "WAREHOUSE", "DATABASE", "SCHEMA"]
        missing = [k for k in required if not cfg.get(k)]
        if missing:
            error_msg = (
                "❌ Snowflake session not available. For Streamlit in Snowflake, no configuration needed. "
                "For local development, missing secrets: " + ", ".join(missing)
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)
    except Exception as e:
        if "secrets" in str(e).lower():
            # More helpful error for missing secrets files
            error_msg = (
                "❌ Running outside Streamlit in Snowflake and no secrets configured. "
                "Either run in Streamlit in Snowflake (no config needed) or configure local secrets."
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        raise

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

    logger.info(f"Creating session for account: {cfg['ACCOUNT']}")
    return Session.builder.configs(connection_parameters).create()


@st.cache_data(ttl=600, show_spinner=False)
def run_query(sql: str) -> pd.DataFrame:
    """
    Execute SQL query and return results as pandas DataFrame.

    Args:
        sql: SQL query string to execute

    Returns:
        pandas DataFrame with query results

    Raises:
        Exception: If query execution fails
    """
    try:
        session = get_snowflake_session()
        logger.debug(f"Executing query: {sql[:100]}...")
        result = session.sql(sql).to_pandas()
        logger.info(f"Query returned {len(result)} rows")
        return result
    except Exception as e:
        logger.error(f"Query execution failed: {e}")
        st.error(f"Database query failed: {str(e)}")
        return pd.DataFrame()  # Return empty DataFrame on error


# -----------------------------
# Reusable Query Helpers
# -----------------------------


def get_global_kpis() -> Dict[str, Any]:
    """
    Calculate firm-level KPIs including client count, advisor count, AUM, and YTD growth.

    Returns:
        Dictionary containing:
        - num_clients: Total number of clients
        - num_advisors: Total number of advisors
        - aum: Assets under management (latest snapshot)
        - ytd_growth_pct: Year-to-date growth percentage
    """
    # Clients
    clients_df = run_query("SELECT COUNT(DISTINCT CLIENT_ID) AS CNT FROM CLIENTS")
    num_clients = (
        int(clients_df.loc[0, "CNT"])
        if not clients_df.empty and "CNT" in clients_df.columns
        else 0
    )

    # Advisors
    advisors_df = run_query("SELECT COUNT(DISTINCT ADVISOR_ID) AS CNT FROM ADVISORS")
    num_advisors = (
        int(advisors_df.loc[0, "CNT"])
        if not advisors_df.empty and "CNT" in advisors_df.columns
        else 0
    )

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
    aum = (
        float(aum_df.loc[0, "AUM"])
        if not aum_df.empty and "AUM" in aum_df.columns
        else 0.0
    )

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
    ytd_growth_pct = (
        float(ytd_df.loc[0, "YTD_GROWTH_PCT"])
        if not ytd_df.empty
        and "YTD_GROWTH_PCT" in ytd_df.columns
        and pd.notna(ytd_df.loc[0, "YTD_GROWTH_PCT"])
        else None
    )

    return {
        "num_clients": num_clients,
        "num_advisors": num_advisors,
        "aum": aum,
        "ytd_growth_pct": ytd_growth_pct,
    }


def get_hnw_low_engagement(
    threshold_days: int = 180, net_worth_threshold: int = 1_000_000
) -> pd.DataFrame:
    """
    Identify high net worth clients with low recent engagement.

    Args:
        threshold_days: Days since last interaction to consider "low engagement"
        net_worth_threshold: Minimum net worth to qualify as "high net worth"

    Returns:
        DataFrame with client details and last interaction dates
    """
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
    sql = f"""
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
# Advanced Use Case Functions
# -----------------------------


def get_customer_360_segments() -> Dict[str, pd.DataFrame]:
    """Customer 360 & Segmentation - Single view across balances, portfolios, behavior"""

    # Client segmentation by AUM
    segments_sql = """
        WITH latest_positions AS (
            SELECT p.PORTFOLIO_ID, p.CLIENT_ID, MAX(ph.TIMESTAMP) AS MAX_TS
            FROM PORTFOLIOS p
            JOIN POSITION_HISTORY ph ON p.PORTFOLIO_ID = ph.PORTFOLIO_ID
            GROUP BY 1, 2
        ),
        client_aum AS (
            SELECT lp.CLIENT_ID,
                   SUM(ph.MARKET_VALUE) AS TOTAL_AUM,
                   COUNT(DISTINCT lp.PORTFOLIO_ID) AS NUM_PORTFOLIOS
            FROM latest_positions lp
            JOIN POSITION_HISTORY ph ON lp.PORTFOLIO_ID = ph.PORTFOLIO_ID AND lp.MAX_TS = ph.TIMESTAMP
            WHERE ph.TICKER <> 'CASH'
            GROUP BY 1
        )
        SELECT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME, c.RISK_TOLERANCE,
               ca.TOTAL_AUM, ca.NUM_PORTFOLIOS,
               CASE
                   WHEN ca.TOTAL_AUM >= 10000000 THEN 'Ultra High Net Worth (>$10M)'
                   WHEN ca.TOTAL_AUM >= 5000000 THEN 'High Net Worth ($5-10M)'
                   WHEN ca.TOTAL_AUM >= 1000000 THEN 'Affluent ($1-5M)'
                   WHEN ca.TOTAL_AUM >= 250000 THEN 'Mass Affluent ($250K-1M)'
                   ELSE 'Emerging Wealth (<$250K)'
               END AS WEALTH_SEGMENT,
               c.NET_WORTH_ESTIMATE
        FROM CLIENTS c
        LEFT JOIN client_aum ca ON c.CLIENT_ID = ca.CLIENT_ID
        ORDER BY ca.TOTAL_AUM DESC NULLS LAST
    """

    # Engagement patterns
    engagement_sql = """
        SELECT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME,
               COUNT(i.INTERACTION_ID) AS TOTAL_INTERACTIONS,
               MAX(i.TIMESTAMP) AS LAST_INTERACTION,
               DATEDIFF(DAY, MAX(i.TIMESTAMP), CURRENT_DATE) AS DAYS_SINCE_LAST_CONTACT,
               COUNT(DISTINCT i.CHANNEL) AS CHANNELS_USED,
               COUNT(CASE WHEN i.INTERACTION_TYPE = 'Complaint' THEN 1 END) AS COMPLAINTS
        FROM CLIENTS c
        LEFT JOIN INTERACTIONS i ON c.CLIENT_ID = i.CLIENT_ID
        GROUP BY 1, 2, 3
        ORDER BY TOTAL_INTERACTIONS DESC
    """

    return {
        "segments": run_query(segments_sql),
        "engagement": run_query(engagement_sql),
    }


def get_next_best_actions() -> pd.DataFrame:
    """Next Best Action - Cross/upsell recommendations based on behavior patterns"""

    sql = """
        WITH client_profile AS (
            SELECT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME, c.RISK_TOLERANCE,
                   COUNT(DISTINCT p.PORTFOLIO_ID) AS NUM_PORTFOLIOS,
                   SUM(ph.MARKET_VALUE) AS TOTAL_AUM,
                   MAX(i.TIMESTAMP) AS LAST_INTERACTION
            FROM CLIENTS c
            LEFT JOIN PORTFOLIOS p ON c.CLIENT_ID = p.CLIENT_ID
            LEFT JOIN POSITION_HISTORY ph ON p.PORTFOLIO_ID = ph.PORTFOLIO_ID
            LEFT JOIN INTERACTIONS i ON c.CLIENT_ID = i.CLIENT_ID
            WHERE ph.TICKER <> 'CASH' OR ph.TICKER IS NULL
            GROUP BY 1, 2, 3, 4
        ),
        recommendations AS (
            SELECT CLIENT_ID, FIRST_NAME, LAST_NAME, RISK_TOLERANCE, TOTAL_AUM,
                   CASE
                       WHEN NUM_PORTFOLIOS = 0 THEN 'Portfolio Setup - Start Investment Journey'
                       WHEN NUM_PORTFOLIOS = 1 AND TOTAL_AUM > 500000 THEN 'Diversification - Add Second Portfolio'
                       WHEN RISK_TOLERANCE = 'Conservative' AND TOTAL_AUM > 1000000 THEN 'Tax Optimization - Municipal Bonds'
                       WHEN RISK_TOLERANCE IN ('Growth', 'Aggressive Growth') AND NUM_PORTFOLIOS < 3 THEN 'Alternative Investments - REITs/Commodities'
                       WHEN DATEDIFF(DAY, LAST_INTERACTION, CURRENT_DATE) > 180 THEN 'Re-engagement - Portfolio Review Meeting'
                       WHEN TOTAL_AUM > 2000000 THEN 'Wealth Planning - Estate & Trust Services'
                       ELSE 'Relationship Deepening - Financial Planning Session'
                   END AS RECOMMENDED_ACTION,
                   CASE
                       WHEN TOTAL_AUM > 5000000 THEN 'High'
                       WHEN TOTAL_AUM > 1000000 THEN 'Medium'
                       ELSE 'Low'
                   END AS PRIORITY,
                   ROUND(TOTAL_AUM * 0.02, 0) AS ESTIMATED_REVENUE_IMPACT
            FROM client_profile
        )
        SELECT * FROM recommendations
        ORDER BY
            CASE PRIORITY WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
            TOTAL_AUM DESC
        LIMIT 50
    """
    return run_query(sql)


def get_churn_early_warning() -> pd.DataFrame:
    """Attrition/Churn Early Warning - Balance flight & engagement drop detection"""

    sql = """
        WITH balance_trends AS (
            SELECT p.CLIENT_ID, p.PORTFOLIO_ID,
                   SUM(CASE WHEN ph.TIMESTAMP >= DATEADD(DAY, -30, CURRENT_DATE) THEN ph.MARKET_VALUE ELSE 0 END) AS RECENT_BALANCE,
                   SUM(CASE WHEN ph.TIMESTAMP >= DATEADD(DAY, -90, CURRENT_DATE) AND ph.TIMESTAMP < DATEADD(DAY, -30, CURRENT_DATE) THEN ph.MARKET_VALUE ELSE 0 END) AS PRIOR_BALANCE
            FROM PORTFOLIOS p
            JOIN POSITION_HISTORY ph ON p.PORTFOLIO_ID = ph.PORTFOLIO_ID
            WHERE ph.TICKER <> 'CASH'
            GROUP BY 1, 2
        ),
        engagement_drop AS (
            SELECT CLIENT_ID,
                   COUNT(CASE WHEN TIMESTAMP >= DATEADD(DAY, -30, CURRENT_DATE) THEN 1 END) AS RECENT_INTERACTIONS,
                   COUNT(CASE WHEN TIMESTAMP >= DATEADD(DAY, -90, CURRENT_DATE) AND TIMESTAMP < DATEADD(DAY, -30, CURRENT_DATE) THEN 1 END) AS PRIOR_INTERACTIONS
            FROM INTERACTIONS
            GROUP BY 1
        )
        SELECT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME,
               SUM(bt.RECENT_BALANCE) AS RECENT_BALANCE,
               SUM(bt.PRIOR_BALANCE) AS PRIOR_BALANCE,
               CASE
                   WHEN SUM(bt.PRIOR_BALANCE) > 0
                   THEN ROUND((SUM(bt.RECENT_BALANCE) - SUM(bt.PRIOR_BALANCE)) / SUM(bt.PRIOR_BALANCE) * 100, 2)
                   ELSE 0
               END AS BALANCE_CHANGE_PCT,
               ed.RECENT_INTERACTIONS,
               ed.PRIOR_INTERACTIONS,
               CASE
                   WHEN SUM(bt.RECENT_BALANCE) < SUM(bt.PRIOR_BALANCE) * 0.8 AND ed.RECENT_INTERACTIONS < ed.PRIOR_INTERACTIONS * 0.5 THEN 'High Risk'
                   WHEN SUM(bt.RECENT_BALANCE) < SUM(bt.PRIOR_BALANCE) * 0.9 OR ed.RECENT_INTERACTIONS < ed.PRIOR_INTERACTIONS * 0.7 THEN 'Medium Risk'
                   ELSE 'Low Risk'
               END AS CHURN_RISK
        FROM CLIENTS c
        LEFT JOIN balance_trends bt ON c.CLIENT_ID = bt.CLIENT_ID
        LEFT JOIN engagement_drop ed ON c.CLIENT_ID = ed.CLIENT_ID
        WHERE SUM(bt.PRIOR_BALANCE) > 0
        GROUP BY 1, 2, 3, ed.RECENT_INTERACTIONS, ed.PRIOR_INTERACTIONS
        HAVING CHURN_RISK IN ('High Risk', 'Medium Risk')
        ORDER BY BALANCE_CHANGE_PCT ASC
    """
    return run_query(sql)


def get_portfolio_drift_analysis() -> pd.DataFrame:
    """Portfolio Drift & Rebalance - Asset-class drift vs strategy analysis"""

    sql = """
        WITH latest_positions AS (
            SELECT PORTFOLIO_ID, MAX(TIMESTAMP) AS MAX_TS
            FROM POSITION_HISTORY
            GROUP BY 1
        ),
        current_allocation AS (
            SELECT p.PORTFOLIO_ID, p.STRATEGY_TYPE,
                   ph.ASSET_CLASS,
                   SUM(ph.MARKET_VALUE) AS CURRENT_VALUE,
                   SUM(SUM(ph.MARKET_VALUE)) OVER (PARTITION BY p.PORTFOLIO_ID) AS TOTAL_PORTFOLIO_VALUE
            FROM PORTFOLIOS p
            JOIN latest_positions lp ON p.PORTFOLIO_ID = lp.PORTFOLIO_ID
            JOIN POSITION_HISTORY ph ON p.PORTFOLIO_ID = ph.PORTFOLIO_ID AND lp.MAX_TS = ph.TIMESTAMP
            WHERE ph.TICKER <> 'CASH'
            GROUP BY 1, 2, 3
        ),
        target_allocations AS (
            SELECT 'Conservative' AS STRATEGY_TYPE, 'Equities' AS ASSET_CLASS, 30 AS TARGET_PCT
            UNION ALL SELECT 'Conservative', 'Fixed Income', 60
            UNION ALL SELECT 'Conservative', 'Cash', 10
            UNION ALL SELECT 'Balanced', 'Equities', 50
            UNION ALL SELECT 'Balanced', 'Fixed Income', 40
            UNION ALL SELECT 'Balanced', 'Cash', 10
            UNION ALL SELECT 'Growth', 'Equities', 70
            UNION ALL SELECT 'Growth', 'Fixed Income', 25
            UNION ALL SELECT 'Growth', 'Cash', 5
            UNION ALL SELECT 'Aggressive Growth', 'Equities', 85
            UNION ALL SELECT 'Aggressive Growth', 'Fixed Income', 10
            UNION ALL SELECT 'Aggressive Growth', 'Cash', 5
        )
        SELECT ca.PORTFOLIO_ID, ca.STRATEGY_TYPE, ca.ASSET_CLASS,
               ROUND(ca.CURRENT_VALUE / ca.TOTAL_PORTFOLIO_VALUE * 100, 2) AS CURRENT_PCT,
               ta.TARGET_PCT,
               ROUND(ca.CURRENT_VALUE / ca.TOTAL_PORTFOLIO_VALUE * 100 - ta.TARGET_PCT, 2) AS DRIFT_PCT,
               CASE
                   WHEN ABS(ca.CURRENT_VALUE / ca.TOTAL_PORTFOLIO_VALUE * 100 - ta.TARGET_PCT) > 10 THEN 'High Drift'
                   WHEN ABS(ca.CURRENT_VALUE / ca.TOTAL_PORTFOLIO_VALUE * 100 - ta.TARGET_PCT) > 5 THEN 'Medium Drift'
                   ELSE 'Within Range'
               END AS DRIFT_STATUS,
               ca.TOTAL_PORTFOLIO_VALUE
        FROM current_allocation ca
        LEFT JOIN target_allocations ta ON ca.STRATEGY_TYPE = ta.STRATEGY_TYPE AND ca.ASSET_CLASS = ta.ASSET_CLASS
        WHERE ta.TARGET_PCT IS NOT NULL
        ORDER BY ABS(DRIFT_PCT) DESC
    """
    return run_query(sql)


def get_idle_cash_analysis() -> pd.DataFrame:
    """Idle Cash / Cash-Sweep - Identify opportunities to monetize idle balances"""

    sql = """
        WITH latest_positions AS (
            SELECT PORTFOLIO_ID, MAX(TIMESTAMP) AS MAX_TS
            FROM POSITION_HISTORY
            GROUP BY 1
        ),
        cash_analysis AS (
            SELECT p.PORTFOLIO_ID, p.CLIENT_ID, p.STRATEGY_TYPE,
                   SUM(CASE WHEN ph.TICKER = 'CASH' THEN ph.MARKET_VALUE ELSE 0 END) AS CASH_BALANCE,
                   SUM(ph.MARKET_VALUE) AS TOTAL_PORTFOLIO_VALUE
            FROM PORTFOLIOS p
            JOIN latest_positions lp ON p.PORTFOLIO_ID = lp.PORTFOLIO_ID
            JOIN POSITION_HISTORY ph ON p.PORTFOLIO_ID = ph.PORTFOLIO_ID AND lp.MAX_TS = ph.TIMESTAMP
            GROUP BY 1, 2, 3
        )
        SELECT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME,
               ca.PORTFOLIO_ID, ca.STRATEGY_TYPE,
               ca.CASH_BALANCE,
               ca.TOTAL_PORTFOLIO_VALUE,
               ROUND(ca.CASH_BALANCE / NULLIF(ca.TOTAL_PORTFOLIO_VALUE, 0) * 100, 2) AS CASH_PCT,
               CASE
                   WHEN ca.CASH_BALANCE / NULLIF(ca.TOTAL_PORTFOLIO_VALUE, 0) > 0.15 THEN 'High Cash (>15%)'
                   WHEN ca.CASH_BALANCE / NULLIF(ca.TOTAL_PORTFOLIO_VALUE, 0) > 0.10 THEN 'Moderate Cash (10-15%)'
                   WHEN ca.CASH_BALANCE / NULLIF(ca.TOTAL_PORTFOLIO_VALUE, 0) > 0.05 THEN 'Normal Cash (5-10%)'
                   ELSE 'Low Cash (<5%)'
               END AS CASH_STATUS,
               ROUND(ca.CASH_BALANCE * 0.03, 0) AS POTENTIAL_ANNUAL_NII,
               CASE
                   WHEN ca.CASH_BALANCE > 100000 AND ca.CASH_BALANCE / NULLIF(ca.TOTAL_PORTFOLIO_VALUE, 0) > 0.10 THEN 'Investment Opportunity'
                   WHEN ca.CASH_BALANCE > 50000 AND ca.CASH_BALANCE / NULLIF(ca.TOTAL_PORTFOLIO_VALUE, 0) > 0.15 THEN 'Sweep Recommendation'
                   ELSE 'Monitor'
               END AS RECOMMENDATION
        FROM cash_analysis ca
        JOIN CLIENTS c ON ca.CLIENT_ID = c.CLIENT_ID
        WHERE ca.CASH_BALANCE > 0
        ORDER BY ca.CASH_BALANCE DESC
    """
    return run_query(sql)


def get_trade_fee_anomalies() -> pd.DataFrame:
    """Trade & Fee Anomaly Detection - Catch leakage, waivers, outliers"""

    sql = """
        WITH fee_stats AS (
            SELECT TRANSACTION_TYPE,
                   AVG(FEE_AMOUNT) AS AVG_FEE,
                   STDDEV(FEE_AMOUNT) AS STDDEV_FEE,
                   COUNT(*) AS TRANSACTION_COUNT
            FROM TRANSACTIONS
            WHERE FEE_AMOUNT IS NOT NULL AND FEE_AMOUNT > 0
            GROUP BY 1
        ),
        anomalies AS (
            SELECT t.TRANSACTION_ID, t.CLIENT_ID, t.PORTFOLIO_ID,
                   t.TRANSACTION_TYPE, t.TRANSACTION_AMOUNT, t.FEE_AMOUNT,
                   t.TIMESTAMP,
                   fs.AVG_FEE, fs.STDDEV_FEE,
                   CASE
                       WHEN t.FEE_AMOUNT = 0 AND t.TRANSACTION_AMOUNT > 10000 THEN 'Zero Fee on Large Trade'
                       WHEN t.FEE_AMOUNT > fs.AVG_FEE + 3 * fs.STDDEV_FEE THEN 'Unusually High Fee'
                       WHEN t.FEE_AMOUNT < fs.AVG_FEE - 2 * fs.STDDEV_FEE AND t.FEE_AMOUNT > 0 THEN 'Unusually Low Fee'
                       WHEN t.TRANSACTION_AMOUNT > 1000000 AND t.FEE_AMOUNT / t.TRANSACTION_AMOUNT < 0.001 THEN 'Large Trade Low Fee Rate'
                       ELSE 'Normal'
                   END AS ANOMALY_TYPE
            FROM TRANSACTIONS t
            LEFT JOIN fee_stats fs ON t.TRANSACTION_TYPE = fs.TRANSACTION_TYPE
            WHERE t.TIMESTAMP >= DATEADD(DAY, -90, CURRENT_DATE)
        )
        SELECT a.*, c.FIRST_NAME, c.LAST_NAME,
               ROUND(a.FEE_AMOUNT / NULLIF(a.TRANSACTION_AMOUNT, 0) * 100, 4) AS FEE_RATE_PCT,
               ROUND(a.AVG_FEE - a.FEE_AMOUNT, 2) AS FEE_DIFFERENCE
        FROM anomalies a
        JOIN CLIENTS c ON a.CLIENT_ID = c.CLIENT_ID
        WHERE a.ANOMALY_TYPE <> 'Normal'
        ORDER BY a.TIMESTAMP DESC
    """
    return run_query(sql)


def get_event_driven_opportunities() -> pd.DataFrame:
    """Event-Driven Outreach - Life/market events for timely client engagement"""

    sql = """
        WITH recent_market_events AS (
            SELECT DISTINCT EVENT_ID, EVENT_NAME, IMPACT_TYPE, DESCRIPTION, START_DATE, END_DATE
            FROM MARKET_EVENTS
            WHERE START_DATE >= DATEADD(DAY, -90, CURRENT_DATE)
               OR END_DATE >= DATEADD(DAY, -90, CURRENT_DATE)
        ),
        client_impact AS (
            SELECT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME,
                   c.LIFE_EVENT, c.LAST_UPDATE_TIMESTAMP,
                   MAX(i.TIMESTAMP) AS LAST_CONTACT,
                   DATEDIFF(DAY, MAX(i.TIMESTAMP), CURRENT_DATE) AS DAYS_SINCE_CONTACT
            FROM CLIENTS c
            LEFT JOIN INTERACTIONS i ON c.CLIENT_ID = i.CLIENT_ID
            GROUP BY 1, 2, 3, 4, 5
        )
        SELECT ci.CLIENT_ID, ci.FIRST_NAME, ci.LAST_NAME,
               CASE
                   WHEN ci.LIFE_EVENT IS NOT NULL AND ci.LAST_UPDATE_TIMESTAMP >= DATEADD(DAY, -60, CURRENT_DATE) THEN 'Recent Life Event'
                   WHEN ci.DAYS_SINCE_CONTACT > 90 THEN 'Long-term Re-engagement'
                   WHEN EXISTS (SELECT 1 FROM recent_market_events) THEN 'Market Event Follow-up'
                   ELSE 'Regular Check-in'
               END AS OUTREACH_TYPE,
               ci.LIFE_EVENT,
               ci.LAST_UPDATE_TIMESTAMP AS LIFE_EVENT_DATE,
               ci.LAST_CONTACT,
               ci.DAYS_SINCE_CONTACT,
               CASE
                   WHEN ci.LIFE_EVENT IN ('Marriage', 'Birth of Child', 'Retirement') THEN 'High'
                   WHEN ci.DAYS_SINCE_CONTACT > 180 THEN 'High'
                   WHEN ci.DAYS_SINCE_CONTACT > 90 THEN 'Medium'
                   ELSE 'Low'
               END AS PRIORITY,
               CASE
                   WHEN ci.LIFE_EVENT = 'Marriage' THEN 'Joint account setup, beneficiary updates'
                   WHEN ci.LIFE_EVENT = 'Birth of Child' THEN 'Education savings, life insurance review'
                   WHEN ci.LIFE_EVENT = 'Retirement' THEN 'Income planning, asset allocation review'
                   WHEN ci.DAYS_SINCE_CONTACT > 180 THEN 'Relationship health check, portfolio review'
                   ELSE 'Market update, investment opportunities'
               END AS SUGGESTED_DISCUSSION_TOPICS
        FROM client_impact ci
        WHERE ci.LIFE_EVENT IS NOT NULL OR ci.DAYS_SINCE_CONTACT > 60
        ORDER BY
            CASE PRIORITY WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
            ci.DAYS_SINCE_CONTACT DESC
    """
    return run_query(sql)


def get_sentiment_analysis() -> Dict[str, pd.DataFrame]:
    """Complaint/Sentiment Intelligence - Mine interaction notes for issues & sentiment"""

    # Complaints trend
    complaints_sql = """
        SELECT DATE_TRUNC('MONTH', TIMESTAMP) AS MONTH,
               COUNT(*) AS TOTAL_COMPLAINTS,
               COUNT(CASE WHEN OUTCOME_NOTES LIKE '%resolved%' THEN 1 END) AS RESOLVED,
               COUNT(CASE WHEN OUTCOME_NOTES LIKE '%escalated%' THEN 1 END) AS ESCALATED,
               AVG(DATEDIFF(DAY, TIMESTAMP, CURRENT_DATE)) AS AVG_RESOLUTION_DAYS
        FROM INTERACTIONS
        WHERE INTERACTION_TYPE = 'Complaint'
          AND TIMESTAMP >= DATEADD(MONTH, -12, CURRENT_DATE)
        GROUP BY 1
        ORDER BY 1
    """

    # Recent sentiment indicators
    sentiment_sql = """
        SELECT CLIENT_ID, INTERACTION_ID, TIMESTAMP, CHANNEL,
               OUTCOME_NOTES,
               CASE
                   WHEN OUTCOME_NOTES LIKE ANY ('%satisfied%', '%happy%', '%pleased%', '%excellent%') THEN 'Positive'
                   WHEN OUTCOME_NOTES LIKE ANY ('%dissatisfied%', '%unhappy%', '%frustrated%', '%angry%', '%complaint%') THEN 'Negative'
                   WHEN OUTCOME_NOTES LIKE ANY ('%concerned%', '%worried%', '%question%', '%clarification%') THEN 'Neutral/Concerned'
                   ELSE 'Neutral'
               END AS SENTIMENT_INDICATOR,
               CASE
                   WHEN OUTCOME_NOTES LIKE '%fee%' THEN 'Fees'
                   WHEN OUTCOME_NOTES LIKE ANY ('%performance%', '%return%', '%loss%') THEN 'Performance'
                   WHEN OUTCOME_NOTES LIKE ANY ('%service%', '%response%', '%wait%') THEN 'Service Quality'
                   WHEN OUTCOME_NOTES LIKE ANY ('%advisor%', '%relationship%') THEN 'Advisor Relationship'
                   ELSE 'General'
               END AS ISSUE_CATEGORY
        FROM INTERACTIONS
        WHERE OUTCOME_NOTES IS NOT NULL
          AND TIMESTAMP >= DATEADD(DAY, -90, CURRENT_DATE)
        ORDER BY TIMESTAMP DESC
        LIMIT 100
    """

    return {
        "complaints_trend": run_query(complaints_sql),
        "sentiment_analysis": run_query(sentiment_sql),
    }


def generate_wealth_narrative(client_id: str) -> Dict[str, Any]:
    """Wealth Narrative & Client Briefing - Auto-generate client summaries"""

    # Client overview
    overview_sql = f"""
        SELECT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME, c.RISK_TOLERANCE,
               c.NET_WORTH_ESTIMATE, c.LIFE_EVENT, c.LAST_UPDATE_TIMESTAMP AS LIFE_EVENT_DATE,
               COUNT(DISTINCT p.PORTFOLIO_ID) AS NUM_PORTFOLIOS,
               COUNT(DISTINCT acr.ADVISOR_ID) AS NUM_ADVISORS
        FROM CLIENTS c
        LEFT JOIN PORTFOLIOS p ON c.CLIENT_ID = p.CLIENT_ID
        LEFT JOIN ADVISOR_CLIENT_RELATIONSHIPS acr ON c.CLIENT_ID = acr.CLIENT_ID
        WHERE c.CLIENT_ID = '{client_id}'
        GROUP BY 1, 2, 3, 4, 5, 6, 7
    """

    # Portfolio summary
    portfolio_sql = f"""
        WITH latest_positions AS (
            SELECT PORTFOLIO_ID, MAX(TIMESTAMP) AS MAX_TS
            FROM POSITION_HISTORY
            GROUP BY 1
        )
        SELECT p.PORTFOLIO_ID, p.STRATEGY_TYPE,
               SUM(ph.MARKET_VALUE) AS TOTAL_VALUE,
               COUNT(DISTINCT ph.TICKER) AS NUM_HOLDINGS
        FROM PORTFOLIOS p
        JOIN latest_positions lp ON p.PORTFOLIO_ID = lp.PORTFOLIO_ID
        JOIN POSITION_HISTORY ph ON p.PORTFOLIO_ID = ph.PORTFOLIO_ID AND lp.MAX_TS = ph.TIMESTAMP
        WHERE p.CLIENT_ID = '{client_id}' AND ph.TICKER <> 'CASH'
        GROUP BY 1, 2
        ORDER BY TOTAL_VALUE DESC
    """

    # Recent interactions
    interactions_sql = f"""
        SELECT TIMESTAMP, INTERACTION_TYPE, CHANNEL, OUTCOME_NOTES
        FROM INTERACTIONS
        WHERE CLIENT_ID = '{client_id}'
        ORDER BY TIMESTAMP DESC
        LIMIT 10
    """

    return {
        "overview": run_query(overview_sql),
        "portfolios": run_query(portfolio_sql),
        "interactions": run_query(interactions_sql),
    }


def get_kyc_insights() -> pd.DataFrame:
    """KYB/KYC Ops Copilot - Client documentation and compliance insights"""

    sql = """
        WITH client_doc_status AS (
            SELECT c.CLIENT_ID, c.FIRST_NAME, c.LAST_NAME,
                   c.NET_WORTH_ESTIMATE, c.RISK_TOLERANCE,
                   COUNT(DISTINCT p.PORTFOLIO_ID) AS NUM_PORTFOLIOS,
                   MAX(i.TIMESTAMP) AS LAST_VERIFICATION_CHECK,
                   DATEDIFF(DAY, MAX(i.TIMESTAMP), CURRENT_DATE) AS DAYS_SINCE_VERIFICATION,
                   CASE
                       WHEN c.NET_WORTH_ESTIMATE > 5000000 THEN 'Enhanced Due Diligence Required'
                       WHEN DATEDIFF(DAY, MAX(i.TIMESTAMP), CURRENT_DATE) > 365 THEN 'Annual Review Due'
                       WHEN COUNT(DISTINCT p.PORTFOLIO_ID) > 3 THEN 'Complex Structure Review'
                       ELSE 'Standard Monitoring'
                   END AS KYC_STATUS,
                   CASE
                       WHEN c.NET_WORTH_ESTIMATE > 10000000 THEN 'High'
                       WHEN c.NET_WORTH_ESTIMATE > 5000000 OR COUNT(DISTINCT p.PORTFOLIO_ID) > 3 THEN 'Medium'
                       ELSE 'Low'
                   END AS RISK_RATING
            FROM CLIENTS c
            LEFT JOIN PORTFOLIOS p ON c.CLIENT_ID = p.CLIENT_ID
            LEFT JOIN INTERACTIONS i ON c.CLIENT_ID = i.CLIENT_ID
            GROUP BY 1, 2, 3, 4, 5
        )
        SELECT CLIENT_ID, FIRST_NAME, LAST_NAME, NET_WORTH_ESTIMATE,
               RISK_TOLERANCE, NUM_PORTFOLIOS, LAST_VERIFICATION_CHECK,
               DAYS_SINCE_VERIFICATION, KYC_STATUS, RISK_RATING,
               CASE
                   WHEN KYC_STATUS = 'Enhanced Due Diligence Required' THEN 'Wealth source verification, PEP screening'
                   WHEN KYC_STATUS = 'Annual Review Due' THEN 'Update personal info, refresh risk assessment'
                   WHEN KYC_STATUS = 'Complex Structure Review' THEN 'Entity structure validation, beneficial ownership'
                   ELSE 'Standard documentation refresh'
               END AS RECOMMENDED_ACTIONS
        FROM client_doc_status
        WHERE KYC_STATUS <> 'Standard Monitoring' OR DAYS_SINCE_VERIFICATION > 180
        ORDER BY
            CASE RISK_RATING WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 ELSE 3 END,
            DAYS_SINCE_VERIFICATION DESC
    """
    return run_query(sql)


# -----------------------------
# UI Layout
# -----------------------------

st.set_page_config(
    page_title="BFSI Wealth 360 – Analytics",
    page_icon="💹",
    layout="wide",
)

st.title("🏦 BFSI Wealth 360 – Advanced Analytics Platform")
st.caption(
    "🚀 Powered by Snowflake | Schema: FSI_DEMOS.WEALTH_360 | 12 Advanced Use Cases"
)

# Use Case Overview
with st.expander(
    "📋 **Use Case Catalog** - Click to see all 12 advanced capabilities",
    expanded=False,
):
    st.markdown(
        """
    | Use Case | Why It Matters | Key Tables | KPIs | Complexity/TTV |
    |----------|----------------|------------|------|----------------|
    | 🎯 **Customer 360 & Segmentation** | Single view across balances, portfolios, behavior | CLIENTS, ACCOUNTS, ACCOUNT_HISTORY, TRANSACTIONS, PORTFOLIOS | AUM/NTB growth, segment coverage, data freshness | Low / 1–2 wks |
    | 🎁 **Next Best Action (cross/upsell)** | Recommend card/loan/insurance/portfolio actions | CLIENTS, TRANSACTIONS, INTERACTIONS, PORTFOLIOS | Offer CTR, conversion, AUM lift | Med / 2–4 wks |
    | ⚠️ **Attrition/Churn Early Warning** | Catch balance flight & engagement drop | ACCOUNT_HISTORY, INTERACTIONS, ADVISOR_CLIENT_RELATIONSHIPS | Churn rate, save rate, time-to-contact | Med / 2–4 wks |
    | ⚖️ **Suitability & Risk Drift Alerts** | Ensure portfolio aligns to risk tolerance | CLIENTS (RISK_TOLERANCE), PORTFOLIOS, POSITION_HISTORY | Suitability breaches, time-to-remediate | Med / 3–5 wks |
    | 📊 **Portfolio Drift & Rebalance** | Alert on asset-class drift vs strategy | PORTFOLIOS, POSITION_HISTORY | Drift % over threshold, rebalance yield | Med / 3–5 wks |
    | 💰 **Idle Cash / Cash-Sweep** | Monetize idle balances | ACCOUNT_HISTORY, POSITION_HISTORY | Cash ratio, NII uplift | Low / 1–2 wks |
    | 🔍 **Trade & Fee Anomaly Detection** | Catch leakage/waivers/outliers | TRANSACTIONS | Fee recovery, false-positive rate | Med / 2–4 wks |
    | 👥 **Advisor Productivity & Coverage** | Improve book management & cadences | ADVISOR_CLIENT_RELATIONSHIPS, INTERACTIONS | Coverage %, last-contact SLA, meetings/client | Low / 1–2 wks |
    | 📅 **Event-Driven Outreach** | Timely, contextual nudge at life/market events | CLIENTS (LIFE_EVENT), MARKET_EVENTS, INTERACTIONS | Engagement rate, booked meetings | Low / 1–2 wks |
    | 💬 **Complaint/Sentiment Intelligence** | Mine notes for issues & intent | INTERACTIONS (OUTCOME_NOTES, LLM_GENERATED_CONTENT) | NPS proxy, time-to-resolution | Low / 1–2 wks |
    | 🤖 **Wealth Narrative & Client Briefing** | Auto-generate client summaries & talking points | CLIENTS, PORTFOLIOS, POSITION_HISTORY, INTERACTIONS | Prep time saved, call quality score | Low / 1–2 wks |
    | 📋 **KYB/KYC Ops Copilot** | Speed up checks & documentation Q&A | CLIENTS/ACCOUNTS + external docs | Cycle time, touchless rate | Med / 3–6 wks |
    """
    )
    st.info(
        "💡 **Navigate through the tabs below to explore each use case with live data and interactive analytics.**"
    )

# Sidebar – connection status and filters
with st.sidebar:
    st.header("Configuration")
    try:
        session = get_snowflake_session()
        st.success("✅ Connected to Snowflake")

        # Show session context info
        try:
            current_db = session.get_current_database()
            current_schema = session.get_current_schema()
            current_warehouse = session.get_current_warehouse()

            with st.expander("Session Context", expanded=False):
                st.info(f"**Database:** {current_db}")
                st.info(f"**Schema:** {current_schema}")
                st.info(f"**Warehouse:** {current_warehouse}")
        except Exception:
            # Context info not critical
            pass

    except Exception as e:
        st.error("❌ Snowflake connection failed")

        # Show helpful error message
        error_str = str(e)
        if "secrets" in error_str.lower() or "no configuration needed" in error_str:
            st.info(
                """
            **For Streamlit in Snowflake:**
            - No configuration needed! The app should work automatically.
            - If you see this error, try refreshing the page.

            **For local development:**
            - Configure `.streamlit/secrets.toml` with your Snowflake credentials.
            """
            )
        else:
            st.exception(e)
        st.stop()

    st.divider()
    st.subheader("Filters")
    hnw_threshold = st.number_input(
        "HNW Threshold (USD)", min_value=100000, value=1_000_000, step=100000
    )
    low_engagement_days = st.slider(
        "Low Engagement if last touch older than (days)",
        min_value=30,
        max_value=365,
        value=180,
        step=15,
    )
    advisor_window_days = st.slider(
        "Advisor activity window (days)", min_value=30, max_value=365, value=90, step=15
    )
    interactions_window_days = st.slider(
        "Engagement window (days)", min_value=30, max_value=1095, value=365, step=30
    )
    concentration_threshold = (
        st.slider(
            "Concentration threshold (%)", min_value=5, max_value=80, value=30, step=5
        )
        / 100.0
    )


tabs = st.tabs(
    [
        "🎯 Customer 360",
        "🎁 Next Best Action",
        "⚠️ Churn Warning",
        "⚖️ Suitability Risk",
        "📊 Portfolio Drift",
        "💰 Idle Cash",
        "🔍 Fee Anomalies",
        "👥 Advisor Coverage",
        "📅 Event Outreach",
        "💬 Sentiment",
        "🤖 AI Briefing",
        "📋 KYC Copilot",
    ]
)


# 🎯 Customer 360 & Segmentation
with tabs[0]:
    st.subheader("🎯 Customer 360 & Segmentation")
    st.caption(
        "Single view across balances, portfolios, behavior | KPIs: AUM/NTB growth, segment coverage, data freshness"
    )

    customer_data = get_customer_360_segments()

    # Segment distribution
    segments_df = customer_data["segments"]
    if not segments_df.empty:
        st.subheader("📊 Wealth Segment Distribution")
        segment_counts = segments_df["WEALTH_SEGMENT"].value_counts()
        fig = px.pie(
            values=segment_counts.values,
            names=segment_counts.index,
            title="Client Distribution by Wealth Segment",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("💰 Client Portfolio Summary")
        st.dataframe(segments_df.head(20), use_container_width=True)

    # Engagement patterns
    engagement_df = customer_data["engagement"]
    if not engagement_df.empty:
        st.subheader("📞 Engagement Patterns")
        fig2 = px.scatter(
            engagement_df.head(50),
            x="DAYS_SINCE_LAST_CONTACT",
            y="TOTAL_INTERACTIONS",
            hover_data=["FIRST_NAME", "LAST_NAME"],
            title="Client Engagement: Interactions vs Days Since Last Contact",
        )
        st.plotly_chart(fig2, use_container_width=True)


# 🎁 Next Best Action (Cross/Upsell)
with tabs[1]:
    st.subheader("🎁 Next Best Action - Cross/Upsell Recommendations")
    st.caption(
        "Recommend card/loan/insurance/portfolio actions | KPIs: Offer CTR, conversion, AUM lift"
    )

    nba_df = get_next_best_actions()
    if not nba_df.empty:
        # Priority distribution
        priority_counts = nba_df["PRIORITY"].value_counts()
        col1, col2, col3 = st.columns(3)
        col1.metric("High Priority", priority_counts.get("High", 0))
        col2.metric("Medium Priority", priority_counts.get("Medium", 0))
        col3.metric("Low Priority", priority_counts.get("Low", 0))

        st.subheader("🎯 Recommended Actions")
        st.dataframe(nba_df, use_container_width=True)

        # Revenue impact
        fig = px.bar(
            nba_df.head(15),
            x="RECOMMENDED_ACTION",
            y="ESTIMATED_REVENUE_IMPACT",
            color="PRIORITY",
            title="Estimated Revenue Impact by Recommendation",
        )
        fig.update_xaxes(tickangle=45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No recommendations available.")


# ⚠️ Attrition/Churn Early Warning
with tabs[2]:
    st.subheader("⚠️ Attrition/Churn Early Warning")
    st.caption(
        "Catch balance flight & engagement drop | KPIs: Churn rate, save rate, time-to-contact"
    )

    churn_df = get_churn_early_warning()
    if not churn_df.empty:
        # Risk distribution
        risk_counts = churn_df["CHURN_RISK"].value_counts()
        col1, col2 = st.columns(2)
        col1.metric("🔴 High Risk", risk_counts.get("High Risk", 0))
        col2.metric("🟡 Medium Risk", risk_counts.get("Medium Risk", 0))

        st.subheader("⚠️ At-Risk Clients")
        st.dataframe(churn_df, use_container_width=True)

        # Balance change visualization
        fig = px.scatter(
            churn_df,
            x="BALANCE_CHANGE_PCT",
            y="RECENT_INTERACTIONS",
            color="CHURN_RISK",
            size="PRIOR_BALANCE",
            hover_data=["FIRST_NAME", "LAST_NAME"],
            title="Churn Risk: Balance Change vs Recent Interactions",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No clients currently at high churn risk.")


# ⚖️ Suitability & Risk Drift Alerts
with tabs[3]:
    st.subheader("⚖️ Suitability & Risk Drift Alerts")
    st.caption(
        "Ensure portfolio aligns to risk tolerance | KPIs: Suitability breaches, time-to-remediate"
    )

    # Traditional suitability check
    mism = get_suitability_mismatches()
    if not mism.empty:
        st.subheader("🚨 Suitability Mismatches")
        st.dataframe(
            mism[
                [
                    "CLIENT_ID",
                    "FIRST_NAME",
                    "LAST_NAME",
                    "RISK_TOLERANCE",
                    "STRATEGY_TYPE",
                ]
            ],
            use_container_width=True,
        )
    else:
        st.success("✅ No suitability mismatches detected.")

    # Enhanced concentration analysis
    st.divider()
    conc = get_concentration_breaches(threshold_pct=concentration_threshold)
    if not conc.empty:
        st.subheader("⚠️ Concentration Risk Alerts")
        st.dataframe(conc, use_container_width=True)

        fig = px.bar(
            conc.head(15),
            x="TICKER",
            y="PCT_OF_PORTFOLIO",
            color="PORTFOLIO_ID",
            title="Portfolio Concentration Breaches",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.success("✅ No concentration breaches at selected threshold.")


# 📊 Portfolio Drift & Rebalance
with tabs[4]:
    st.subheader("📊 Portfolio Drift & Rebalance")
    st.caption(
        "Alert on asset-class drift vs strategy | KPIs: Drift % over threshold, rebalance yield"
    )

    drift_df = get_portfolio_drift_analysis()
    if not drift_df.empty:
        # Drift status summary
        drift_counts = drift_df["DRIFT_STATUS"].value_counts()
        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 High Drift", drift_counts.get("High Drift", 0))
        col2.metric("🟡 Medium Drift", drift_counts.get("Medium Drift", 0))
        col3.metric("✅ Within Range", drift_counts.get("Within Range", 0))

        st.subheader("📊 Asset Allocation Drift Analysis")
        st.dataframe(drift_df, use_container_width=True)

        # Drift visualization
        fig = px.scatter(
            drift_df,
            x="TARGET_PCT",
            y="CURRENT_PCT",
            color="DRIFT_STATUS",
            size="TOTAL_PORTFOLIO_VALUE",
            facet_col="ASSET_CLASS",
            facet_col_wrap=3,
            title="Target vs Current Allocation by Asset Class",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No portfolio drift data available.")


# 💰 Idle Cash / Cash-Sweep
with tabs[5]:
    st.subheader("💰 Idle Cash / Cash-Sweep Opportunities")
    st.caption("Monetize idle balances | KPIs: Cash ratio, NII uplift")

    cash_df = get_idle_cash_analysis()
    if not cash_df.empty:
        # Cash opportunity summary
        high_cash = cash_df[cash_df["CASH_STATUS"].str.contains("High")].shape[0]
        investment_opps = cash_df[
            cash_df["RECOMMENDATION"] == "Investment Opportunity"
        ].shape[0]
        total_idle_cash = cash_df["CASH_BALANCE"].sum()
        potential_nii = cash_df["POTENTIAL_ANNUAL_NII"].sum()

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("High Cash Portfolios", high_cash)
        col2.metric("Investment Opportunities", investment_opps)
        col3.metric("Total Idle Cash", f"${total_idle_cash:,.0f}")
        col4.metric("Potential Annual NII", f"${potential_nii:,.0f}")

        st.subheader("💰 Cash Analysis by Portfolio")
        st.dataframe(cash_df, use_container_width=True)

        # Cash percentage distribution
        fig = px.histogram(
            cash_df,
            x="CASH_PCT",
            color="CASH_STATUS",
            title="Distribution of Cash Percentages",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No cash sweep opportunities identified.")


# 🔍 Trade & Fee Anomaly Detection
with tabs[6]:
    st.subheader("🔍 Trade & Fee Anomaly Detection")
    st.caption(
        "Catch leakage/waivers/outliers | KPIs: Fee recovery, false-positive rate"
    )

    anomalies_df = get_trade_fee_anomalies()
    if not anomalies_df.empty:
        # Anomaly type distribution
        anomaly_counts = anomalies_df["ANOMALY_TYPE"].value_counts()
        st.subheader("🚨 Anomaly Type Distribution")
        fig = px.pie(
            values=anomaly_counts.values,
            names=anomaly_counts.index,
            title="Fee Anomaly Types (Last 90 Days)",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("⚠️ Recent Fee Anomalies")
        st.dataframe(anomalies_df, use_container_width=True)

        # Fee analysis
        fig2 = px.scatter(
            anomalies_df,
            x="TRANSACTION_AMOUNT",
            y="FEE_AMOUNT",
            color="ANOMALY_TYPE",
            title="Transaction Amount vs Fee Amount (Anomalies Only)",
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.success("✅ No fee anomalies detected in the last 90 days.")


# 👥 Advisor Productivity & Coverage
with tabs[7]:
    st.subheader("👥 Advisor Productivity & Coverage")
    st.caption(
        "Improve book management & cadences | KPIs: Coverage %, last-contact SLA, meetings/client"
    )

    adv_df = get_advisor_productivity(window_days=advisor_window_days)
    if not adv_df.empty:
        st.subheader("📊 Advisor Performance Metrics")
        st.dataframe(adv_df, use_container_width=True)

        # AUM by advisor
        fig = px.bar(
            adv_df,
            x="ADVISOR_NAME",
            y="TOTAL_AUM",
            title="Assets Under Management by Advisor",
            text_auto=True,
        )
        fig.update_layout(xaxis_title="Advisor", yaxis_title="Total AUM (USD)")
        st.plotly_chart(fig, use_container_width=True)

        # Interactions vs AUM efficiency
        fig2 = px.scatter(
            adv_df,
            x="INTERACTIONS_90D",
            y="TOTAL_AUM",
            size="NUM_CLIENTS",
            hover_data=["ADVISOR_NAME"],
            title="Advisor Efficiency: Interactions vs AUM",
        )
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No advisor productivity data available.")


# 📅 Event-Driven Outreach
with tabs[8]:
    st.subheader("📅 Event-Driven Outreach (Life/Market)")
    st.caption(
        "Timely, contextual nudge at life/market events | KPIs: Engagement rate, booked meetings"
    )

    events_df = get_event_driven_opportunities()
    if not events_df.empty:
        # Outreach priority summary
        priority_counts = events_df["PRIORITY"].value_counts()
        col1, col2, col3 = st.columns(3)
        col1.metric("🔴 High Priority", priority_counts.get("High", 0))
        col2.metric("🟡 Medium Priority", priority_counts.get("Medium", 0))
        col3.metric("🟢 Low Priority", priority_counts.get("Low", 0))

        st.subheader("📅 Outreach Opportunities")
        st.dataframe(events_df, use_container_width=True)

        # Outreach type distribution
        outreach_counts = events_df["OUTREACH_TYPE"].value_counts()
        fig = px.bar(
            x=outreach_counts.index,
            y=outreach_counts.values,
            title="Outreach Opportunities by Type",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No immediate outreach opportunities identified.")


# 💬 Complaint/Sentiment Intelligence
with tabs[9]:
    st.subheader("💬 Complaint/Sentiment Intelligence")
    st.caption("Mine notes for issues & intent | KPIs: NPS proxy, time-to-resolution")

    sentiment_data = get_sentiment_analysis()

    # Complaints trend
    complaints_df = sentiment_data["complaints_trend"]
    if not complaints_df.empty:
        st.subheader("📈 Complaints Trend (12 Months)")
        fig = px.line(
            complaints_df,
            x="MONTH",
            y="TOTAL_COMPLAINTS",
            title="Monthly Complaints Volume",
        )
        st.plotly_chart(fig, use_container_width=True)

        # Resolution analysis
        fig2 = px.bar(
            complaints_df,
            x="MONTH",
            y=["RESOLVED", "ESCALATED"],
            title="Complaint Resolution Status by Month",
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Sentiment analysis
    sentiment_df = sentiment_data["sentiment_analysis"]
    if not sentiment_df.empty:
        st.subheader("😊 Recent Sentiment Analysis")
        sentiment_counts = sentiment_df["SENTIMENT_INDICATOR"].value_counts()
        fig3 = px.pie(
            values=sentiment_counts.values,
            names=sentiment_counts.index,
            title="Sentiment Distribution (Last 90 Days)",
        )
        st.plotly_chart(fig3, use_container_width=True)

        st.dataframe(sentiment_df.head(20), use_container_width=True)


# 🤖 Wealth Narrative & Client Briefing (GenAI)
with tabs[10]:
    st.subheader("🤖 Wealth Narrative & Client Briefing (GenAI)")
    st.caption(
        "Auto-generate client summaries & talking points | KPIs: Prep time saved, call quality score"
    )

    # Client selector
    all_clients = run_query(
        "SELECT CLIENT_ID, FIRST_NAME, LAST_NAME FROM CLIENTS ORDER BY LAST_NAME"
    )
    if not all_clients.empty:
        selected_client = st.selectbox(
            "Select Client for AI-Generated Briefing:",
            options=all_clients["CLIENT_ID"].tolist(),
            format_func=lambda x: f"{all_clients[all_clients['CLIENT_ID']==x]['FIRST_NAME'].iloc[0]} {all_clients[all_clients['CLIENT_ID']==x]['LAST_NAME'].iloc[0]} ({x})",
        )

        if selected_client:
            narrative_data = generate_wealth_narrative(selected_client)

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

            # Portfolio summary
            portfolios_df = narrative_data["portfolios"]
            if not portfolios_df.empty:
                st.subheader("💼 Portfolio Summary")
                st.dataframe(portfolios_df, use_container_width=True)

            # Recent interactions
            interactions_df = narrative_data["interactions"]
            if not interactions_df.empty:
                st.subheader("📞 Recent Interactions")
                st.dataframe(interactions_df, use_container_width=True)


# 📋 KYB/KYC Ops Copilot (GenAI)
with tabs[11]:
    st.subheader("📋 KYB/KYC Ops Copilot (GenAI)")
    st.caption("Speed up checks & documentation Q&A | KPIs: Cycle time, touchless rate")

    kyc_df = get_kyc_insights()
    if not kyc_df.empty:
        # KYC status summary
        kyc_counts = kyc_df["KYC_STATUS"].value_counts()
        risk_counts = kyc_df["RISK_RATING"].value_counts()

        col1, col2 = st.columns(2)
        with col1:
            st.subheader("📋 KYC Status Distribution")
            fig = px.pie(
                values=kyc_counts.values,
                names=kyc_counts.index,
                title="KYC Review Status",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.subheader("⚖️ Risk Rating Distribution")
            fig2 = px.pie(
                values=risk_counts.values,
                names=risk_counts.index,
                title="Client Risk Ratings",
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📋 KYC Action Items")
        st.dataframe(kyc_df, use_container_width=True)

        # Days since verification analysis
        fig3 = px.histogram(
            kyc_df,
            x="DAYS_SINCE_VERIFICATION",
            color="RISK_RATING",
            title="Days Since Last Verification by Risk Rating",
        )
        st.plotly_chart(fig3, use_container_width=True)

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
    else:
        st.success("✅ All clients are up to date with KYC requirements.")
