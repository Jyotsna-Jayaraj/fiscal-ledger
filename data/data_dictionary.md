# Data Dictionary: Fiscal Ledger Dataset

## Overview
This dataset contains panel data on national fiscal budgets across various countries and years (1936–2026). It includes raw percentage allocations, nominal budget amounts, validation flags, recalculated metrics, and comparative policy ratios (e.g., Guns vs. Butter).

* **Primary Key / Index:** `['Country', 'Year']`
* **Data Completeness:** 100% complete across available country-year records (no missing values).

---

## Variable Definitions

### 1. Identifiers & Temporal Coordinates
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`Country`** | `String` | Name of the nation/entity (e.g., `India Real Budget 1947 2026`). |
| **`Year`** | `Integer` | Observation year, ranging from 1936 to 2026. |

---

### 2. Budget Allocation Percentages (Raw Data)
*Note: All percentage fields represent share of total national budget (0–100%).*

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`Defense_Percentage`** | `Float` | Share allocated to national defense and military expenditures. |
| **`Education_Percentage`** | `Float` | Share allocated to primary, secondary, and higher education. |
| **`Health_Percentage`** | `Float` | Share allocated to public healthcare and medical services. |
| **`Interest_Payments_Percentage`** | `Float` | Share spent servicing government public debt. |
| **`Infrastructure_Percentage`** | `Float` | Share allocated to public works, transport, and infrastructure. |
| **`Agriculture_Percentage`** | `Float` | Share allocated to agricultural subsidies and development. |
| **`State_Transfers_Percentage`** | `Float` | Share transferred to regional, state, or municipal governments. |
| **`Social_Welfare_Percentage`** | `Float` | Share spent on pensions, social security, and welfare programs. |
| **`Administration_and_Others_Percentage`** | `Float` | Share spent on civil administration and miscellaneous operations. |

---

### 3. Financial Totals & Raw Nominal Values
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`Total_Budget_Billions_USD`** | `Float` | Total annual government expenditure (in billions of USD). |
| **`Defense_Amount_Billions_USD`** | `Float` | Nominal defense spending (Billions USD). |
| **`Education_Amount_Billions_USD`** | `Float` | Nominal education spending (Billions USD). |
| **`Health_Amount_Billions_USD`** | `Float` | Nominal health spending (Billions USD). |
| **`Interest_Payments_Amount_Billions_USD`** | `Float` | Nominal interest payment spending (Billions USD). |
| **`Infrastructure_Amount_Billions_USD`** | `Float` | Nominal infrastructure spending (Billions USD). |
| **`Agriculture_Amount_Billions_USD`** | `Float` | Nominal agricultural spending (Billions USD). |
| **`State_Transfers_Amount_Billions_USD`** | `Float` | Nominal state transfer spending (Billions USD). |
| **`Social_Welfare_Amount_Billions_USD`** | `Float` | Nominal social welfare spending (Billions USD). |
| **`Administration_and_Others_Amount_Billions_USD`** | `Float` | Nominal civil administration spending (Billions USD). |

---

### 4. Data Quality & Audit Flags
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`Total_Percentage_Sum`** | `Float` | Sum of all sector allocation percentages (Target ≈ 100.00%). Captures minor floating-point rounding errors (e.g., 99.98%–100.02%). |
| **`Pct_Discrepancy_Flag`** | `Boolean` / `Int` | Binary flag (`1` / `0`) indicating whether `Total_Percentage_Sum` deviates significantly from 100.0%. |

---

### 5. Verified / Calculated Nominal Amounts
*Calculated using: Calculated Amount = Total_Budget_Billions_USD * (Sector_Percentage / 100)*

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`Defense_Amount_Billions_USD_Calculated`** | `Float` | Recalculated defense budget in Billions USD. |
| **`Education_Amount_Billions_USD_Calculated`** | `Float` | Recalculated education budget in Billions USD. |
| **`Health_Amount_Billions_USD_Calculated`** | `Float` | Recalculated health budget in Billions USD. |
| **`Interest_Payments_Amount_Billions_USD_Calculated`** | `Float` | Recalculated interest payment budget in Billions USD. |
| **`Infrastructure_Amount_Billions_USD_Calculated`** | `Float` | Recalculated infrastructure budget in Billions USD. |
| **`Agriculture_Amount_Billions_USD_Calculated`** | `Float` | Recalculated agriculture budget in Billions USD. |
| **`State_Transfers_Amount_Billions_USD_Calculated`** | `Float` | Recalculated state transfer budget in Billions USD. |
| **`Social_Welfare_Amount_Billions_USD_Calculated`** | `Float` | Recalculated social welfare budget in Billions USD. |
| **`Administration_and_Others_Amount_Billions_USD_Calculated`** | `Float` | Recalculated administration budget in Billions USD. |

---

### 6. Derived Policy Indicators
| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| **`Social_Total_Percentage`** | `Float` | Aggregated percentage spent on social well-being (Education + Health + Social Welfare). |
| **`Guns_Butter_Ratio`** | `Float` | Ratio of defense/military spending to social spending (Defense_Percentage / Social_Total_Percentage). |
| **`Guns_Butter_Index_Normalized`** | `Float` | Standardized or Min-Max scaled index of `Guns_Butter_Ratio` for cross-country comparison. |