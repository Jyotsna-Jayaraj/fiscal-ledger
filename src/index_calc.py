import pandas as pd

def calculate_guns_butter_index(df: pd.DataFrame, epsilon: float = 1e-5) -> pd.DataFrame:
    """
    Computes the Guns-vs-Butter ratio and relative metrics.
    Adds 'Social_Total_Percentage' and 'Guns_Butter_Ratio'.
    """
    df = df.copy()
    
    # Combined social spending
    df['Social_Total_Percentage'] = (
        df['Health_Percentage'].fillna(0) + 
        df['Education_Percentage'].fillna(0) + 
        df['Social_Welfare_Percentage'].fillna(0)
    )
    
    # Guns to Butter Ratio (Defense % / Social %)
    df['Guns_Butter_Ratio'] = df['Defense_Percentage'] / (df['Social_Total_Percentage'] + epsilon)
    
    # Normalized Guns-Butter Score (-1 to 1 scale for easy mapping)
    # +1 = Purely Defense Focus, -1 = Purely Social Focus
    total_defense_social = df['Defense_Percentage'] + df['Social_Total_Percentage'] + epsilon
    df['Guns_Butter_Index_Normalized'] = (df['Defense_Percentage'] - df['Social_Total_Percentage']) / total_defense_social
    
    return df