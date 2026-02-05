import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_analysis_charts(processed_data_path):
    """
    Generates visual evidence for performance and behavioral analysis.
    """
    df = pd.read_csv(processed_data_path)
    output_dir = 'output/charts'
    os.makedirs(output_dir, exist_ok=True)
    
    sns.set(style="whitegrid")
    sentiment_order = ['Extreme Fear', 'Fear', 'Neutral', 'Greed', 'Extreme Greed']

    # Chart 1: Volatility Risk
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='classification', y='Daily PnL', data=df, hue='classification', legend=False, palette="coolwarm", order=sentiment_order, showfliers=False)
    plt.title('Daily PnL Volatility by Sentiment')
    plt.ylabel('Daily PnL ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'pnl_by_fgi_classification.png'))
    plt.close()

    # Chart 2: Win Rate
    plt.figure(figsize=(10, 6))
    sns.barplot(x='classification', y='Win Rate', data=df, hue='classification', legend=False, palette="Greens", order=sentiment_order, errorbar=None)
    plt.title('Average Win Rate by Sentiment')
    plt.ylabel('Win Rate')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'win_rate_by_fgi_classification.png'))
    plt.close()

    # Chart 3: Trading Volume
    plt.figure(figsize=(10, 6))
    sns.barplot(x='classification', y='Number of Trades', data=df, estimator=sum, hue='classification', legend=False, palette="viridis", order=sentiment_order, errorbar=None)
    plt.title('Total Trading Volume')
    plt.ylabel('Number of Trades')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'trades_by_fgi_classification.png'))
    plt.close()

    # Chart 4: Long/Short Bias
    plt.figure(figsize=(10, 6))
    sns.barplot(x='classification', y='Long/Short Ratio', data=df, hue='classification', legend=False, palette="magma", order=sentiment_order, errorbar=None)
    plt.title('Long/Short Ratio (Sentiment Tracking)')
    plt.ylabel('Ratio (>1 is Bullish)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'long_short_by_fgi_classification.png'))
    plt.close()

    # Chart 5: Trade Sizing
    plt.figure(figsize=(10, 6))
    sns.barplot(x='classification', y='Average Trade Size USD', data=df, hue='classification', legend=False, palette="Blues", order=sentiment_order, errorbar=None)
    plt.title('Average Position Size ($)')
    plt.ylabel('Size ($)')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'trade_size_by_fgi_classification.png'))
    plt.close()

    print("Analysis charts generated.")

if __name__ == "__main__":
    generate_analysis_charts('output/processed_data/daily_trader_metrics_with_sentiment.csv')