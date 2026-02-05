# Predictive Modeling

## What I Tried 
Goal was to create a model that could look at a trader's behavior today and predict exactly how much money they would make (or lose) tomorrow.

---

### Model 1: The "Win vs. Loss" Predictor
I tried to train a model to guess if a trader would finish the next day with a profit or a loss.

**The Result: It Failed to Spot Danger**
* **The Illusion:** On paper, the model looked okay with **63% accuracy**.
* **The Reality:** The model was cheating. Because most days in the market were profitable, it learned to just guess "Profit" almost every single time to get a high score.
* **The Critical Failure:** The most important job of this tool was to warn us about **Losing Days**. It failed completely.
    * There were **44** actual days where traders lost money.
    * My model only spotted **2** of them.
    * **Bottom Line:** It missed **95%** of the warning signals. A risk tool that stays silent during a crash is dangerous.

---

### Model 2: The "Volatility" Predictor
I tried to predict exactly how big the price swings (volatility) would be for the next day.

**The Result: Worse Than a Guess**
* **The Score:** The model got a score (R-Squared) of **-0.385**.
* **What that means:** A score of 0.0 means "just guessing the average." A *negative* score means my complicated model was actually less accurate than if I had just used a simple average.
* **The Error:** On average, the predictions were off by **$7,838 per day**.

---

## Why It Failed (The Root Cause)
It was a problem with the nature of daily trading data.

**1. The "Coin Flip" Problem**
I found that daily trading results are incredibly noisy. Just because a trader made money yesterday doesn't mean they will make money today.
* Some traders win big and take the next day off.
* Others win big, get overconfident, and lose it all the next day.
There was no consistent pattern for the computer to find. It was like trying to predict the outcome of a coin flip based on the previous flip—there is simply no connection.

**2. Personality vs. Price**
My data successfully identified a trader's *personality* (e.g., "This guy is a High Roller"), but it didn't tell me what the *market* was doing. Knowing a trader likes big risks doesn't tell me if Bitcoin is going to crash tomorrow morning. Without that market price data, the model was flying blind.

