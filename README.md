# The Cost of Debt: How Sovereign Spending Shifted Over 90 Years

A comprehensive data journalism and econometric analysis studying how 45 sovereign nations allocated public expenditure across nine functional categories ("Guns vs. Butter") between 1936 and 2026.

---

## Project Overview

Over the past nine decades, sovereign nations have faced a fundamental trade-off: allocating public capital between national security (**"Guns"**) and socio-economic investment (**"Butter"**). Using a panel dataset of **3,654 country-year observations**, this repository examines long-run spending trends, fiscal response functions during geopolitical shocks, machine-learning-derived "fiscal personalities," and time-series forecasting.

Key focus areas include:
* **The Guns-vs-Butter Trade-Off:** Quantifying the shift from post-WWII defense priorities to modern social welfare states.
* **Geopolitical Shocks & Alliances:** Econometric modeling of NATO vs. Non-NATO expenditure adjustments following major global events (1991 USSR dissolution, 2008 Financial Crisis, 2022 regional conflicts).
* **Fiscal Personality Clustering:** Unsupervised $K$-Means clustering to identify sovereign spending archetypes.
* **Time-Series Analysis:** Structural break detection using `PELT` algorithms and short-term defense spending forecasts using ARIMA.

---

## Repository Structure

```text
.
├── app/
│   └── streamlit_app.py      # Interactive Streamlit dashboard
├── outputs/                  # Generated figures, heatmaps, and diagnostic plots
│   ├── 01_data_coverage_heatmap.jpg
│   ├── 01_pct_sum_distribution.png
│   ├── 02_global_spending_trends.png
│   ├── 02_divergent_country_paths.jpg
│   ├── 02_guns_butter_era_distribution.png
│   ├── 02_country_ratio_heatmap.png
│   ├── 03_defense_allocation_boxplot.png
│   ├── 03_guns_butter_trajectory.png
│   ├── 04_k_selection_diagnostics.png
│   ├── 04_fiscal_personality_profiles.jpg
│   ├── 04_transition_matrix.png
│   ├── 05_structural_breaks_detected.jpg
│   └── 05_defense_forecast.png
├── writeup/
│   └── the_cost_of_debt.html # Full analytical report in HTML format
├── README.md                 # Project documentation
└── requirements.txt          # Python dependencies

## Quick Start

1.  Clone the repository and install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2.  Run the interactive dashboard:
    ```bash
    streamlit run app/streamlit_app.py
    ```
3.  Read the full report by opening `writeup/the_cost_of_debt.html` in your web browser.