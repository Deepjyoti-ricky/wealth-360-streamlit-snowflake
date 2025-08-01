#!/usr/bin/env python3
"""
Stock Analysis Demo using Semantic Model
Demonstrates how to use the semantic YAML model with stock price data
"""

import pandas as pd
import numpy as np
import yaml
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

class StockAnalyzer:
    """
    Stock analyzer using semantic model definitions
    """
    
    def __init__(self, semantic_model_path, data_path):
        """Initialize with semantic model and data"""
        self.load_semantic_model(semantic_model_path)
        self.load_data(data_path)
        self.validate_data()
        
    def load_semantic_model(self, path):
        """Load semantic model from YAML file"""
        with open(path, 'r') as file:
            self.model = yaml.safe_load(file)
        print(f"✅ Loaded semantic model: {self.model['model_name']}")
        print(f"   Description: {self.model['description']}")
        
    def load_data(self, path):
        """Load stock data from CSV file"""
        self.df = pd.read_csv(path)
        self.df['date'] = pd.to_datetime(self.df['date'])
        print(f"✅ Loaded data: {len(self.df)} records")
        print(f"   Date range: {self.df['date'].min()} to {self.df['date'].max()}")
        
    def validate_data(self):
        """Validate data against semantic model rules"""
        print("\n📋 Data Quality Validation:")
        
        # Check completeness rules
        completeness_rules = self.model['data_quality']['completeness']
        for rule in completeness_rules:
            field = rule['field']
            if field in self.df.columns:
                null_count = self.df[field].isnull().sum()
                if null_count == 0:
                    print(f"   ✅ {field}: No null values")
                else:
                    print(f"   ❌ {field}: {null_count} null values found")
                    
        # Check for duplicate ticker-date-variable combinations
        duplicates = self.df.groupby(['ticker', 'date', 'variable_name']).size()
        duplicate_count = (duplicates > 1).sum()
        if duplicate_count == 0:
            print(f"   ✅ Uniqueness: No duplicate ticker-date-variable combinations")
        else:
            print(f"   ❌ Uniqueness: {duplicate_count} duplicate combinations found")
            
    def get_dimension_values(self, dimension):
        """Get unique values for a dimension"""
        return self.df[dimension].unique().tolist()
        
    def calculate_measures(self):
        """Calculate derived measures from the semantic model"""
        print("\n📊 Calculating Derived Measures:")
        
        # Create pivot table for easier calculations
        pivot_df = self.df.pivot_table(
            index=['ticker', 'date'], 
            columns='variable_name', 
            values='value', 
            fill_value=np.nan
        ).reset_index()
        
        # Calculate day-over-day change for closing prices
        if 'Close' in pivot_df.columns:
            pivot_df = pivot_df.sort_values(['ticker', 'date'])
            pivot_df['day_over_day_change'] = (
                pivot_df.groupby('ticker')['Close']
                .pct_change()
                .fillna(0)
            )
            print("   ✅ Calculated day-over-day price change")
            
        # Add market cap categories
        large_cap = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
        medium_cap = ['TSLA', 'META', 'NVDA']
        
        pivot_df['market_cap_category'] = pivot_df['ticker'].apply(
            lambda x: 'Large Cap' if x in large_cap 
                     else 'Medium Cap' if x in medium_cap 
                     else 'Small Cap'
        )
        print("   ✅ Assigned market cap categories")
        
        self.processed_df = pivot_df
        return pivot_df
        
    def analyze_performance(self):
        """Analyze stock performance using semantic model patterns"""
        print("\n📈 Stock Performance Analysis:")
        
        if not hasattr(self, 'processed_df'):
            self.calculate_measures()
            
        df = self.processed_df
        
        # Daily performance summary
        if 'day_over_day_change' in df.columns:
            performance_stats = df.groupby('ticker')['day_over_day_change'].agg([
                'mean', 'std', 'min', 'max'
            ]).round(4)
            
            print("\n   Daily Performance Summary (% change):")
            print(performance_stats)
            
        # Volume analysis
        if 'Nasdaq Volume' in df.columns:
            volume_stats = df.groupby('ticker')['Nasdaq Volume'].agg([
                'mean', 'sum'
            ]).round(0)
            
            print("\n   Volume Analysis:")
            print(volume_stats)
            
        # Market cap category analysis
        if 'market_cap_category' in df.columns and 'Close' in df.columns:
            category_stats = df.groupby('market_cap_category')['Close'].agg([
                'mean', 'count'
            ]).round(2)
            
            print("\n   Average Price by Market Cap Category:")
            print(category_stats)
            
    def create_visualizations(self):
        """Create visualizations based on semantic model recommendations"""
        print("\n📊 Creating Visualizations:")
        
        if not hasattr(self, 'processed_df'):
            self.calculate_measures()
            
        df = self.processed_df
        
        # Set up the plotting style
        plt.style.use('default')
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Stock Analysis Dashboard', fontsize=16, fontweight='bold')
        
        # 1. Time series of closing prices
        if 'Close' in df.columns:
            for ticker in df['ticker'].unique():
                ticker_data = df[df['ticker'] == ticker]
                axes[0, 0].plot(ticker_data['date'], ticker_data['Close'], 
                               label=ticker, marker='o', markersize=4)
            
            axes[0, 0].set_title('Daily Closing Prices')
            axes[0, 0].set_xlabel('Date')
            axes[0, 0].set_ylabel('Price ($)')
            axes[0, 0].legend()
            axes[0, 0].grid(True, alpha=0.3)
        
        # 2. Day-over-day change
        if 'day_over_day_change' in df.columns:
            change_data = df.groupby('ticker')['day_over_day_change'].mean() * 100
            bars = axes[0, 1].bar(change_data.index, change_data.values)
            axes[0, 1].set_title('Average Daily Change (%)')
            axes[0, 1].set_xlabel('Ticker')
            axes[0, 1].set_ylabel('Change (%)')
            axes[0, 1].tick_params(axis='x', rotation=45)
            
            # Color bars based on positive/negative
            for i, bar in enumerate(bars):
                if change_data.values[i] >= 0:
                    bar.set_color('green')
                else:
                    bar.set_color('red')
        
        # 3. Volume comparison
        if 'Nasdaq Volume' in df.columns:
            volume_data = df.groupby('ticker')['Nasdaq Volume'].mean() / 1_000_000
            axes[1, 0].bar(volume_data.index, volume_data.values, color='steelblue')
            axes[1, 0].set_title('Average Daily Volume (Millions)')
            axes[1, 0].set_xlabel('Ticker')
            axes[1, 0].set_ylabel('Volume (M shares)')
            axes[1, 0].tick_params(axis='x', rotation=45)
        
        # 4. Market cap category distribution
        if 'market_cap_category' in df.columns:
            category_counts = df['market_cap_category'].value_counts()
            axes[1, 1].pie(category_counts.values, labels=category_counts.index, 
                          autopct='%1.1f%%', startangle=90)
            axes[1, 1].set_title('Market Cap Category Distribution')
        
        plt.tight_layout()
        plt.savefig('stock_analysis_dashboard.png', dpi=300, bbox_inches='tight')
        print("   ✅ Saved dashboard as 'stock_analysis_dashboard.png'")
        plt.show()
        
    def generate_insights(self):
        """Generate insights based on semantic model common queries"""
        print("\n🔍 Key Insights:")
        
        if not hasattr(self, 'processed_df'):
            self.calculate_measures()
            
        df = self.processed_df
        
        # Best and worst performers
        if 'day_over_day_change' in df.columns:
            avg_change = df.groupby('ticker')['day_over_day_change'].mean() * 100
            best_performer = avg_change.idxmax()
            worst_performer = avg_change.idxmin()
            
            print(f"   📈 Best performer: {best_performer} (+{avg_change[best_performer]:.2f}%)")
            print(f"   📉 Worst performer: {worst_performer} ({avg_change[worst_performer]:.2f}%)")
            
        # Highest volume stock
        if 'Nasdaq Volume' in df.columns:
            avg_volume = df.groupby('ticker')['Nasdaq Volume'].mean()
            highest_volume = avg_volume.idxmax()
            print(f"   📊 Highest volume: {highest_volume} ({avg_volume[highest_volume]:,.0f} shares)")
            
        # Price range analysis
        if 'Close' in df.columns:
            price_stats = df.groupby('ticker')['Close'].agg(['min', 'max'])
            price_stats['range'] = price_stats['max'] - price_stats['min']
            most_volatile = price_stats['range'].idxmax()
            print(f"   📈 Most volatile: {most_volatile} (${price_stats.loc[most_volatile, 'range']:.2f} range)")

def main():
    """Main execution function"""
    print("🚀 Stock Analysis Demo using Semantic Model")
    print("=" * 50)
    
    try:
        # Initialize analyzer
        analyzer = StockAnalyzer('semantic_model.yaml', 'sample_stock_data.csv')
        
        # Run analysis
        analyzer.calculate_measures()
        analyzer.analyze_performance()
        analyzer.generate_insights()
        analyzer.create_visualizations()
        
        print("\n✅ Analysis completed successfully!")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        return 1
        
    return 0

if __name__ == "__main__":
    exit(main())