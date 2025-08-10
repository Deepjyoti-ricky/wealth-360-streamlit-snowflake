# Wealth 360 Streamlit Analytics

[![CI/CD Pipeline](https://github.com/Deepjyoti-ricky/wealth-360-streamlit-snowflake/actions/workflows/ci.yml/badge.svg)](https://github.com/Deepjyoti-ricky/wealth-360-streamlit-snowflake/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)

Professional Streamlit application for BFSI analytics, built to run natively in **Streamlit in Snowflake** using Snowpark. Provides comprehensive dashboards for wealth management use cases using the `FSI_DEMOS.WEALTH_360` dataset.

## 🎯 Key Features

- **Snowpark-First Architecture**: Uses `get_active_session()` when running in Snowflake; seamless fallback to credentials locally
- **Production-Ready Dashboards**: 7 comprehensive analytics tabs covering all major BFSI use cases
- **Advanced SQL Patterns**: Implements verified patterns like ASOF JOIN with MATCH_CONDITION for time-series analysis
- **Professional Code Quality**: Full linting, type checking, security scanning, and automated CI/CD

## 📊 Analytics Modules

| Module | Description | Key Metrics |
|--------|-------------|-------------|
| **Overview** | Firm-level KPIs and asset allocation | AUM, Client Count, YTD Growth |
| **HNW Retention** | High net worth clients with low engagement | Net Worth vs. Last Contact |
| **Advisor Productivity** | Performance metrics by advisor | AUM per Advisor, Client Coverage |
| **Portfolio Performance** | Investment performance analytics | YTD Returns, Asset Allocation |
| **Compliance & Risk** | Regulatory monitoring | Suitability Mismatches, Concentration |
| **Market Events Impact** | Performance during market conditions | AUM Change by Event Period |
| **Digital Engagement** | Customer interaction analytics | Channel Usage, Complaint Trends |

## 🏗️ Data Architecture

The application expects the following tables in `FSI_DEMOS.WEALTH_360`:

```
CLIENTS                      # Demographics, risk profiles, financial goals
├── ADVISORS                 # Staff information and specializations
├── ADVISOR_CLIENT_RELATIONSHIPS  # Active relationship mappings
├── ACCOUNTS & ACCOUNT_HISTORY    # Banking account balances over time
├── PORTFOLIOS               # Investment strategy definitions
├── POSITION_HISTORY         # Holdings snapshots (TICKER, MARKET_VALUE)
├── TRANSACTIONS             # Portfolio activity (buys, sells, deposits)
└── MARKET_EVENTS           # Predefined market periods for context
```

## 🚀 Quick Start

### Streamlit in Snowflake (Recommended)

1. Upload `streamlit_app.py` to Snowflake
2. Optionally set context overrides in Snowsight secrets:
   ```toml
   [SNOWFLAKE]
   DATABASE = "FSI_DEMOS"
   SCHEMA = "WEALTH_360"
   WAREHOUSE = "COMPUTE_WH"
   ROLE = "ACCOUNTADMIN"
   ```
3. Run the app - no credentials required!

### Local Development

1. **Environment Setup**
   ```bash
   git clone https://github.com/Deepjyoti-ricky/wealth-360-streamlit-snowflake.git
   cd wealth-360-streamlit-snowflake
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Configure Secrets**
   ```bash
   cp .streamlit/secrets.example.toml .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml with your Snowflake credentials
   ```

3. **Run Application**
   ```bash
   streamlit run streamlit_app.py
   ```

## 🛠️ Development

### Code Quality Standards

This project maintains enterprise-grade code quality:

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Set up pre-commit hooks
pre-commit install

# Run quality checks
black .                    # Code formatting
flake8 .                  # Linting
mypy streamlit_app.py         # Type checking
bandit -r .               # Security scanning
```

### Testing

```bash
# Validate core imports
python -c "import streamlit, pandas, plotly; print('✅ Success')"

# Manual testing checklist:
# □ Streamlit in Snowflake deployment
# □ Local development environment
# □ All 7 dashboard tabs functional
# □ Error handling scenarios
# □ Performance with large datasets
```

## 🏢 Production Deployment

### Snowflake Requirements
- Snowflake account with Streamlit in Snowflake enabled
- Access to `FSI_DEMOS.WEALTH_360` schema
- Appropriate warehouse for query execution

### Performance Considerations
- Queries are cached for 10 minutes using `@st.cache_data`
- ASOF JOINs optimize time-series lookups
- Position history uses latest snapshots to minimize data transfer

## 📋 API Documentation

### Core Functions

```python
# streamlit_app.py - Main application functions
get_snowflake_session() -> Session
    """Get authenticated Snowpark session"""

get_global_kpis() -> Dict[str, Any]
    """Calculate firm-level KPIs"""

get_hnw_low_engagement(threshold_days: int, net_worth_threshold: int) -> pd.DataFrame
    """Identify at-risk high-value clients"""

run_query(sql: str) -> pd.DataFrame
    """Execute SQL with error handling and logging"""
```

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Development guidelines
- Code style requirements
- Pull request process
- Issue templates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 [Documentation](README.md)
- 🐛 [Report Issues](https://github.com/Deepjyoti-ricky/wealth-360-streamlit-snowflake/issues)
- 💡 [Feature Requests](https://github.com/Deepjyoti-ricky/wealth-360-streamlit-snowflake/issues/new?template=feature_request.md)
- 🤝 [Contributing Guidelines](CONTRIBUTING.md)

## 👤 Author

**Deepjyoti Dev**
Senior Data Cloud Architect, Snowflake GXC Team
📧 deepjyoti.dev@snowflake.com
📱 +917205672310

---

**Built with ❤️ for the BFSI community using Snowflake and Streamlit**
