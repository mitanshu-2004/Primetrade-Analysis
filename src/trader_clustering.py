import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from math import pi

def cluster_traders(processed_data_path):
    """
    Segments traders into behavioral groups using K-Means clustering.
    """
    print("Clustering traders...")
    df = pd.read_csv(processed_data_path)
    
    # Filter for active days to capture true behavior
    df = df[df['Number of Trades'] > 0].copy()
    
    # Aggregate data per trader
    trader_features = df.groupby('Account').agg({
        'Daily PnL': ['mean', 'std'],
        'Win Rate': 'mean',
        'Number of Trades': 'mean',
        'Average Trade Size USD': 'mean',
        'Long/Short Ratio': 'mean'
    })
    
    trader_features.columns = ['avg_daily_pnl', 'std_daily_pnl', 'avg_win_rate', 'avg_num_trades', 'avg_trade_size_usd', 'avg_long_short_ratio']
    trader_features.fillna(0, inplace=True) 
    
    # Normalize features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(trader_features)
    
    # K-Means
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(scaled_features)
    
    print(f"Silhouette Score: {silhouette_score(scaled_features, clusters):.3f}")
    
    # Label the clusters dynamically
    temp_df = trader_features.copy()
    temp_df['Cluster_ID'] = clusters
    stats = temp_df.groupby('Cluster_ID').mean()
    
    # Logic: High Size = High Roller, High Win Rate = Skilled, Remainder = Typical
    high_roller_id = stats['avg_trade_size_usd'].idxmax()
    remaining = [c for c in [0,1,2] if c != high_roller_id]
    skilled_id = stats.loc[remaining, 'avg_win_rate'].idxmax()
    typical_id = [c for c in [0,1,2] if c not in [high_roller_id, skilled_id]][0]
    
    mapping = {high_roller_id: "High_Roller", skilled_id: "Skilled_Contrarian", typical_id: "Typical_Trader"}
    trader_features['Cluster'] = clusters
    trader_features['Archetype'] = trader_features['Cluster'].map(mapping)
    
    # Save results
    output_path = 'output/processed_data/clustered_traders.csv'
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    trader_features.to_csv(output_path)
    
    # Generate Visualization Charts
    charts_dir = 'output/charts'
    os.makedirs(charts_dir, exist_ok=True)
    
    # 1. PCA Scatter Plot
    pca = PCA(n_components=2, random_state=42)
    pca_result = pca.fit_transform(scaled_features)
    
    plt.figure(figsize=(10, 7))
    colors = {"Typical_Trader": "blue", "High_Roller": "orange", "Skilled_Contrarian": "green"}
    for archetype, color in colors.items():
        mask = trader_features['Archetype'] == archetype
        plt.scatter(pca_result[mask, 0], pca_result[mask, 1], c=color, label=archetype, alpha=0.7, edgecolors='w', s=100)
    plt.title('Trader Segments (PCA Projection)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(os.path.join(charts_dir, 'pca_clusters.png'))
    plt.close()

    # 2. Radar Chart
    from sklearn.preprocessing import MinMaxScaler
    categories = list(trader_features.columns[:-2]) # Exclude Cluster/Archetype
    scaler = MinMaxScaler()
    
    plt.figure(figsize=(8, 8))
    ax = plt.subplot(111, polar=True)
    angles = [n / float(len(categories)) * 2 * pi for n in range(len(categories))]
    angles += angles[:1]
    
    plt.xticks(angles[:-1], categories, size=8)
    ax.set_rlabel_position(0)
    plt.yticks([0.25, 0.5, 0.75], ["25%","50%","75%"], color="grey", size=7)
    plt.ylim(0, 1)
    
    archetype_means = trader_features.groupby('Archetype')[categories].mean()
    means_scaled = pd.DataFrame(scaler.fit_transform(archetype_means), columns=categories, index=archetype_means.index)
    
    for arch, color in colors.items():
        if arch in means_scaled.index:
            vals = means_scaled.loc[arch].values.flatten().tolist()
            vals += vals[:1]
            ax.plot(angles, vals, linewidth=2, label=arch, color=color)
            ax.fill(angles, vals, color=color, alpha=0.1)
            
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.savefig(os.path.join(charts_dir, 'cluster_archetype_radar_chart.png'))
    plt.close()
    
    print("Clustering complete.")

if __name__ == "__main__":
    cluster_traders('output/processed_data/daily_trader_metrics_with_sentiment.csv')