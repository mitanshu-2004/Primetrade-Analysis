# PrimeTrade Analysis Project

## Overview

This project analyzes trader behavior to find profitable strategies. It processes raw trading logs, groups traders into behavioral profiles (like "Whales" or "Skilled Contrarians"), and identifies when to follow them based on market sentiment.

The project consists of two parts:

*   **The Strategy Dashboard (Success):** A tool that identifies trader groups and tells us when to copy them based on market sentiment.
*   **The Predictive Engine (Discontinued):** An experiment to predict future daily profits, which I have shut down due to the randomness of daily price action.

## Project Structure

*   `data/`: `historical_data.csv`, `fear_greed_index.csv`.
*   `src/`: Contains the processing scripts.
    *   `data_preparation.py`: Cleans data and calculates daily stats.
    *   `analysis_script.py`: Creates charts for the report.
    *   `trader_clustering.py`: Groups traders using machine learning.
*   `output/`: Where the results go (processed files and charts).
*   `dashboard.py`: The interactive app to view results.

## Setup & How to Run

### 1. Install Requirements

You need Python installed. Open your terminal and install the required libraries:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn streamlit altair
```

### 2. Run the Processing command

```bash
python run_all.py
```

### 3. Launch the Dashboard

To see the analysis, strategies and clustering run:

```bash
streamlit run dashboard.py
```

## 📄 Detailed Project Report — [View Documentation](project_report.md)
