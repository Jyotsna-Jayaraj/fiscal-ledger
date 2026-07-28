from pathlib import Path
import pandas as pd
import numpy as np
import re

def clean_country_name(filename_stem: str) -> str:
    """
    Extracts the clean country name from messy filenames.
    Example: 'Argentina_Real_Budget_1946_2026' -> 'Argentina'
    """
    # Replace underscores with spaces
    name = filename_stem.replace("_", " ")
    
    # Strip common metadata artifacts like 'Real Budget 1946 2026' or trailing years
    name = re.sub(r'(?i)\b(real|budget|nominal|\d{4})\b', '', name)
    
    # Clean up excess spaces
    return name.strip()

def merge_country_files(raw_dir: Path) -> pd.DataFrame:
    """
    Scans CSVs, extracts clean country names, and concatenates them.
    """
    country_files = list(raw_dir.glob("*.csv"))
    
    if not country_files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir}")

    df_list = []
    
    for file_path in country_files:
        country_name = clean_country_name(file_path.stem)
        
        df_country = pd.read_csv(file_path)
        df_country.columns = df_country.columns.str.strip()
        
        # Override or insert Country column with clean name
        df_country['Country'] = country_name
            
        df_list.append(df_country)
        
    merged_df = pd.concat(df_list, ignore_index=True)
    merged_df = merged_df.sort_values(by=['Country', 'Year']).reset_index(drop=True)
    return merged_df

def clean_panel_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Performs data hygiene, percentage sum validations, and calculates missing amounts.
    """
    df = df.copy()
    
    # 1. Percentage Integrity Check
    pct_cols = [c for c in df.columns if c.endswith('_Percentage')]
    df['Total_Percentage_Sum'] = df[pct_cols].sum(axis=1)
    
    # Flag rows where sum of percentages deviates significantly from 100%
    df['Pct_Discrepancy_Flag'] = np.abs(df['Total_Percentage_Sum'] - 100.0) > 1.0
    
    # 2. Impute missing or zero dollar amounts from percentages
    for col in pct_cols:
        base_name = col.replace('_Percentage', '')
        amt_col = f"{base_name}_Amount_Billions_USD"
        if amt_col in df.columns and 'Total_Budget_Billions_USD' in df.columns:
            # Re-compute exact amounts based on percentage * total budget
            df[f"{amt_col}_Calculated"] = (df[col] / 100.0) * df['Total_Budget_Billions_USD']
            
    return df

def process_and_save_pipeline(raw_country_dir: Path, output_parquet_path: Path) -> pd.DataFrame:
    """
    Full pipeline wrapper: Merge -> Clean -> Save to Parquet.
    """
    raw_df = merge_country_files(raw_country_dir)
    clean_df = clean_panel_dataset(raw_df)
    
    output_parquet_path.parent.mkdir(parents=True, exist_ok=True)
    clean_df.to_parquet(output_parquet_path, index=False)
    
    print(f"Successfully merged {clean_df['Country'].nunique()} countries ({len(clean_df)} rows) into {output_parquet_path}")
    return clean_df