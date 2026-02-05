import streamlit as st
import pandas as pd
import os
import altair as alt

st.set_page_config(page_title="Trader Analysis", layout="wide")
st.title("Trader Performance & Strategy Analysis")

@st.cache_data
def load_data():
    try:
        clusters = pd.read_csv('output/processed_data/clustered_traders.csv')
        daily = pd.read_csv('output/processed_data/daily_trader_metrics_with_sentiment.csv')
        daily['date'] = pd.to_datetime(daily['date'])
        
        merged = pd.merge(daily, clusters[['Account', 'Archetype']], on='Account', how='left')
        merged.dropna(subset=['Archetype'], inplace=True)
        return clusters, merged
    except FileNotFoundError:
        return None, None

clusters, data = load_data()

tab1, tab2, tab3 = st.tabs(["Analysis", "Strategies", "Trader Groups"])

with tab1:
    st.header("Executive Summary of Findings")
    
    st.subheader("Q1: Does performance differ between Fear vs Greed?")
    st.write("**Yes.** I found that market sentiment is the primary driver of volatility, but not necessarily win rate.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**PnL Volatility (Drawdown Risk)**")
        st.caption("Insight: 'Extreme' sentiment creates massive variance. While 'Fear' offers the highest upside (buying the dip), 'Extreme Greed' often leads to the largest drawdowns for aggressive traders.")
        if os.path.exists('output/charts/pnl_by_fgi_classification.png'):
            st.image('output/charts/pnl_by_fgi_classification.png', use_container_width=True)
            
    with col2:
        st.markdown("**Win Rates**")
        st.caption("Insight: Win rates remain surprisingly stable across conditions (~45-55%). This implies that profitability is determined by **when** they trade and **how much** they bet, not just how often they are right.")
        if os.path.exists('output/charts/win_rate_by_fgi_classification.png'):
            st.image('output/charts/win_rate_by_fgi_classification.png', use_container_width=True)
            
    st.divider()
    
    st.subheader("Q2: Do traders change behavior based on sentiment?")
    st.write("**Yes.** The data reveals strong 'Herd Behavior' and emotional position sizing.")
    
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("**Long/Short Bias**")
        st.caption("Insight: Traders are reactive. They aggressively Short during Fear (<1.0 ratio) and go All-In Long during Greed (>1.2), often entering trends late.")
        if os.path.exists('output/charts/long_short_by_fgi_classification.png'):
            st.image('output/charts/long_short_by_fgi_classification.png', use_container_width=True)
            
    with col4:
        st.markdown("**Position Sizing (Risk Appetite)**")
        st.caption("Insight: Confidence correlates with Price. Traders significantly increase their position sizes during Greed, which exposes them to 'Fat Tail' crash risks.")
        if os.path.exists('output/charts/trade_size_by_fgi_classification.png'):
            st.image('output/charts/trade_size_by_fgi_classification.png', use_container_width=True)
            
    st.divider()

    st.subheader("Q3: Can we identify distinct trader segments?")
    st.write("I applied K-Means clustering to the dataset and identified **3 distinct behavioral profiles**:")
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("**1. The High Rollers (Whales)**\n\n* **Defining Trait:** Massive Trade Size (>$30k).\n* **Behavior:** They are risk-takers who provide liquidity during Fear but suffer heavy losses during Euphoria.")
    with c2:
        st.info("**2. The Skilled Contrarians**\n\n* **Defining Trait:** Balanced Long/Short Ratio.\n* **Behavior:** The 'Smart Money'. They manage risk best and survive extreme volatility with positive expectancy.")
    with c3:
        st.info("**3. The Aggressive Bulls**\n\n* **Defining Trait:** Ratio > 40.0 (Never Short).\n* **Behavior:** 'Permabulls'. They perform well only in straight-up bull markets but lack versatility.")

    st.markdown("👉 *For a deep dive into these segments and to see individual accounts, navigate to the **'Trader Groups'** tab.*")

with tab2:
    st.header("Proposed Strategies")
    st.write("Based on the data analysis, I developed two actionable rules to outperform the market.")

    st.subheader("1. Buy the Panic (The 'Whale' Strategy)")
    st.success("**Recommendation:** When the market is in **FEAR**, follow the 'High Rollers'.")
    
    with st.expander("See the Logic", expanded=True):
        st.write("""
        **My Findings:**
        The 'High Roller' group essentially acts as a liquidity provider. When the public panics (Fear), these traders step in with massive size.
        * **Performance:** In Fear conditions, this group generates the highest daily returns (approx +$222k/day in our sample).
        * **Action:** If Sentiment is Fear/Extreme Fear, copy the Long trades of the 'High Roller' segment.
        """)

    if data is not None:
        subset = data[(data['classification'].isin(['Fear', 'Extreme Fear'])) & (data['Archetype'] == 'High_Roller')]
        if not subset.empty:
            st.dataframe(subset[['date', 'Account', 'Daily PnL', 'Average Trade Size USD']].sort_values('Daily PnL', ascending=False).style.format({'Daily PnL': "${:,.2f}", 'Average Trade Size USD': "${:,.0f}"}), use_container_width=True)

    st.divider()

    st.subheader("2. Avoid the Crash (The Rotation)")
    st.warning("**Recommendation:** When the market is in **EXTREME GREED**, switch to 'Skilled Contrarians'.")
    
    with st.expander("See the Logic", expanded=True):
        st.write("""
        **My Findings:**
        During Extreme Greed, the 'High Rollers' get reckless. They chase prices and often end up with a negative PnL despite the bull run.
        * **The Pivot:** The 'Skilled Contrarian' group manages risk much better in these conditions, maintaining a positive win rate (~39%) while Whales crash (~11%).
        * **Action:** When FGI > 75, stop following High Rollers. Rotate capital to the Skilled Contrarian group.
        """)
        
    if data is not None:
        subset = data[(data['classification'] == 'Extreme Greed')]
        if not subset.empty:
            comparison = subset.groupby('Archetype')[['Daily PnL', 'Win Rate']].mean()
            st.table(comparison.style.format({'Daily PnL': "${:,.2f}", 'Win Rate': "{:.1%}"}))

with tab3:
    st.header("Who are these traders?")
    st.write("I used machine learning (PCA & K-Means) to group the traders based on their habits.")
    
    col1, col2 = st.columns(2)
    with col1:
        if os.path.exists('output/charts/pca_clusters.png'):
            st.image('output/charts/pca_clusters.png', caption="Visualizing the Segments", use_container_width=True)
    with col2:
        if os.path.exists('output/charts/cluster_archetype_radar_chart.png'):
            st.image('output/charts/cluster_archetype_radar_chart.png', caption="Behavioral Profiles", use_container_width=True)
            
    st.divider()
    
    st.subheader("Inspect the Groups")
    
    option = st.selectbox("Select a Group to explore:", ["High_Roller", "Skilled_Contrarian", "Typical_Trader"])
    
    descriptions = {
        "High_Roller": "These are the 'Whales'. They trade with massive size ($30k+) and high volatility. They are risk-takers who drive the market.",
        "Skilled_Contrarian": "These are the 'Safety Nets'. They trade smaller sizes but maintain balanced books. They survive volatility better than anyone else.",
        "Typical_Trader": "These are the 'Aggressive Bulls'. They almost never short the market (Ratio > 40). They do well in bull runs but lack versatility."
    }
    
    st.info(descriptions.get(option, ""))
    
    if clusters is not None:
        view = clusters[clusters['Archetype'] == option].copy()
        st.dataframe(view[['Account', 'avg_daily_pnl', 'avg_win_rate', 'avg_trade_size_usd']].style.format({'avg_daily_pnl': "${:,.2f}", 'avg_win_rate': "{:.1%}", 'avg_trade_size_usd': "${:,.0f}"}), use_container_width=True)