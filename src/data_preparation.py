import pandas as pd
import os
import numpy as np

def load_and_prepare_data(fear_greed_path, historical_data_path):
    """
    Loads raw trading data and market sentiment, cleans it, and calculates 
    daily performance metrics for each account.
    """
    print("Loading datasets...")
    fear_greed_df = pd.read_csv(fear_greed_path)
    historical_df = pd.read_csv(historical_data_path) 

    # standardized date formatting
    historical_df['date'] = pd.to_datetime(historical_df['Timestamp IST'], dayfirst=True, errors='coerce').dt.date
    fear_greed_df['date'] = pd.to_datetime(fear_greed_df['date'], errors='coerce').dt.date

    historical_df.dropna(subset=['date'], inplace=True)
    fear_greed_df.dropna(subset=['date'], inplace=True)

    print("Calculating daily metrics...")

    def calculate_ls_ratio(x):
        longs = x[x == 'BUY'].count()
        shorts = x[x == 'SELL'].count()
        return longs / shorts if shorts > 0 else (longs if longs > 0 else 0)

    # Aggregate daily stats per trader
    daily_metrics = historical_df.groupby(['Account', 'date']).agg({
        'Closed PnL': ['sum', 'std'], 
        'Size USD': 'mean',           
        'Trade ID': 'count',          
        'Side': calculate_ls_ratio    
    }).reset_index()

    daily_metrics.columns = ['Account', 'date', 'Daily PnL', 'PnL Volatility', 'Average Trade Size USD', 'Number of Trades', 'Long/Short Ratio']
    
    # Calculate Win Rate separately to avoid aggregation errors
    win_rates = historical_df.groupby(['Account', 'date'])['Closed PnL'].apply(lambda x: (x > 0).sum() / x.count() if x.count() > 0 else 0).reset_index(name='Win Rate')
    
    daily_metrics = pd.merge(daily_metrics, win_rates, on=['Account', 'date'])
    daily_metrics['PnL Volatility'] = daily_metrics['PnL Volatility'].fillna(0) 

    # Merge with Market Sentiment
    merged_df = pd.merge(daily_metrics, fear_greed_df[['date', 'value', 'classification']], on='date', how='inner')
    
    output_path = 'output/processed_data/daily_trader_metrics_with_sentiment.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged_df.to_csv(output_path, index=False)
    
    print(f"Data preparation complete. Saved to {output_path}")
    return merged_df

if __name__ == "__main__":
    load_and_prepare_data('data/fear_greed_index.csv', 'data/historical_data.csv')