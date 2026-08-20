import pandas as pd

def fit_and_assign_clusters(df: pd.DataFrame, feature_cols: list, k: int = 4) -> pd.DataFrame:
    """
    Standardizes features, fits KMeans clustering, and appends cluster labels.
    """
    from sklearn.preprocessing import StandardScaler
    from sklearn.cluster import KMeans
    
    df_out = df.copy()
    valid_mask = df_out[feature_cols].notnull().all(axis=1)
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df_out.loc[valid_mask, feature_cols])
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    df_out.loc[valid_mask, 'Cluster'] = kmeans.fit_predict(X_scaled)
    
    return df_out