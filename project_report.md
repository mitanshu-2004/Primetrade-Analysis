# Project Report

## Methodology

I built a data pipeline to turn raw trade logs into clear actions.

*   **Data Processing:** I combined the trading logs with the Fear & Greed Index. I calculated daily stats for every trader, including their Profit/Loss (PnL), Win Rate, Trade Size, and how much they went Long vs. Short.
*   **Grouping Traders:** I used a machine learning tool (K-Means) to sort traders based on how they act, not just how much money they make. This found three specific types of traders.
*   **Strategy Check:** I looked at how each group performed during "Fear" and "Greed" to see which actions worked best.

## Note on Predictive Modeling

I initially attempted to build a machine learning model to predict daily trader profits. However, the daily price action proved too random to generate reliable predictions. You can find the details of this experiment, including why it failed, in the `failed_prediction/` folder.

## Insights

*   **The Crowd Follows Trends:** Most traders react to the market instead of planning ahead. They sell heavily during Fear and buy heavily during Greed.
*   **Whales Buy the Dip:** The "High Roller" group makes the most money during Fear. They use their large cash reserves to buy when everyone else is panic selling.
*   **Greed is Dangerous:** During "Extreme Greed," the High Rollers get careless. Their win rate drops to around 11%, and they often lose money even though the market is going up.

## Strategy Recommendations

Based on the data, I suggest a "Rotation Strategy" to reduce risk.

*   **Strategy A: The "Dip Buyer"**
    *   **Condition:** When the market is in Fear.
    *   **Action:** Copy the trades of the High Rollers.
    *   **Why:** They have a proven history of buying at the bottom and making large profits when the market turns back up.
*   **Strategy B: The "Defensive Switch"**
    *   **Condition:** When the market is in Extreme Greed (Index > 75).
    *   **Action:** Stop following High Rollers and switch to Skilled Contrarians.
    *   **Why:** High Rollers tend to crash during euphoria. Skilled Contrarians are the only group that keeps a steady win rate (~39%) and makes money when the market gets too hot.