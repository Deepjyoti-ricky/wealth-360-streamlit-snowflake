# Stock Price Analysis with Semantic Model

This project demonstrates how to create and use a semantic YAML model for stock price time series analysis, based on the Snowflake Labs pandas tutorial dataset structure.

## 📁 Project Structure

```
Stock Analysis/
├── semantic_model.yaml          # Semantic data model definition
├── sample_stock_data.csv        # Sample stock price dataset
├── stock_analysis_demo.py       # Python demo script
├── requirements.txt             # Python dependencies
├── README.md                    # This file
└── sfguide-getting-started-with-pandas-on-snowflake/  # Original Snowflake repo
```

## 🎯 What's Included

### 1. Semantic Model (`semantic_model.yaml`)
A comprehensive YAML-based semantic model that defines:

- **Dimensions**: ticker, date, exchange_code, variable_name, company_name
- **Measures**: value, volume, price changes, calculated metrics
- **Calculated Fields**: price volatility, market cap categories, rolling metrics
- **Data Quality Rules**: completeness, validity, consistency checks
- **Common Query Patterns**: performance analysis, volume analysis, volatility tracking
- **Visualization Recommendations**: time series, heatmaps, comparison charts

### 2. Sample Dataset (`sample_stock_data.csv`)
Real-world style stock data including:
- Popular stocks: AAPL, MSFT, GOOGL, AMZN, TSLA, META, NVDA, SNOW
- Multiple metrics per stock: Open, Close, High, Low, Volume, Pre/Post-Market
- Time series data across multiple trading days
- Different exchanges (NASDAQ, NYSE)

### 3. Analysis Demo (`stock_analysis_demo.py`)
A complete Python script that demonstrates:
- Loading and validating data against the semantic model
- Calculating derived measures (day-over-day changes, categories)
- Performing analysis using semantic model patterns
- Creating visualizations based on model recommendations
- Generating business insights

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Demo
```bash
python stock_analysis_demo.py
```

This will:
- ✅ Load and validate the semantic model
- 📊 Process the sample stock data
- 📈 Generate performance analytics
- 🎨 Create visualization dashboard
- 💡 Provide key insights

### 3. Expected Output
```
🚀 Stock Analysis Demo using Semantic Model
==================================================
✅ Loaded semantic model: stock_price_timeseries
   Description: Daily stock price and trading metrics for publicly traded companies
✅ Loaded data: 98 records
   Date range: 2024-01-15 00:00:00 to 2024-01-16 00:00:00

📋 Data Quality Validation:
   ✅ ticker: No null values
   ✅ date: No null values
   ✅ value: No null values
   ✅ Uniqueness: No duplicate ticker-date-variable combinations

📊 Calculating Derived Measures:
   ✅ Calculated day-over-day price change
   ✅ Assigned market cap categories

📈 Stock Performance Analysis:
   [Performance metrics and analysis results]

🔍 Key Insights:
   [Generated business insights]

📊 Creating Visualizations:
   ✅ Saved dashboard as 'stock_analysis_dashboard.png'
```

## 📊 Semantic Model Features

### Dimensions & Measures
- **Stock Identifiers**: ticker, company_name, exchange_code
- **Time Dimension**: date with time-series capabilities
- **Metrics**: price values, volume, calculated changes
- **Categories**: market cap classification, metric types

### Data Quality & Validation
- Completeness checks for required fields
- Validity rules for data ranges and formats
- Consistency validation for unique combinations
- Automated data quality reporting

### Analytics Patterns
- **Performance Analysis**: day-over-day changes, volatility metrics
- **Volume Analysis**: trading volume patterns and trends
- **Comparative Analysis**: cross-stock performance comparison
- **Time Series Analysis**: rolling calculations and trends

### Visualization Framework
- Pre-defined chart types and configurations
- Recommended visualizations for different use cases
- Interactive dashboard templates
- Export capabilities for reporting

## 🔄 Extending the Model

### Adding New Dimensions
```yaml
dimensions:
  sector:
    type: "string"
    description: "Industry sector classification"
    examples: ["Technology", "Healthcare", "Finance"]
```

### Adding New Measures
```yaml
measures:
  market_cap:
    type: "float"
    description: "Market capitalization in billions"
    unit: "USD billions"
    aggregations: ["sum", "avg"]
```

### Adding Calculated Fields
```yaml
calculated_fields:
  volatility_score:
    formula: "STDDEV(day_over_day_change) OVER (PARTITION BY ticker)"
    description: "30-day volatility score"
    type: "float"
```

## 🗄️ Using with Real Snowflake Data

To use with the actual Cybersyn Financial & Economic Essentials dataset:

1. **Set up Snowflake access** (follow the original repository setup)
2. **Update data source** in the semantic model:
   ```yaml
   data_source:
     type: "snowflake_table"
     database: "FINANCIAL__ECONOMIC_ESSENTIALS"
     schema: "CYBERSYN"
     table: "STOCK_PRICE_TIMESERIES"
   ```
3. **Install Snowflake connector**:
   ```bash
   pip install snowflake-snowpark-python[modin]
   ```

## 📚 Related Resources

- [Original Snowflake Labs Repository](https://github.com/Snowflake-Labs/sfguide-getting-started-with-pandas-on-snowflake)
- [Snowpark pandas Documentation](https://docs.snowflake.com/developer-guide/snowpark/python/snowpark-pandas)
- [Cybersyn Financial Dataset](https://app.snowflake.com/marketplace/listing/GZTSZAS2KF7/cybersyn-inc-financial-economic-essentials)

## 🤝 Contributing

Feel free to extend the semantic model with:
- Additional stock metrics and KPIs
- More sophisticated calculated fields
- Enhanced data quality rules
- New visualization patterns
- Integration with other data sources

## 📄 License

This project follows the same licensing as the original Snowflake Labs repository (Apache 2.0).