import sys
from pathlib import Path

# Add project root to Python path so src modules can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Import reusable shared logic
from src.index_calc import calculate_guns_butter_index

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Guns vs. Butter: 90 Years of Global Budget Priorities",
    page_icon="🌎",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished styling
st.markdown("""
    <style>
    .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .stMetric { background-color: #f8f9fa; padding: 12px; border-radius: 8px; border: 1px solid #e9ecef; }
    </style>
""", unsafe_allow_html=True)

# --- DATA LOADING (CACHED) ---
@st.cache_data
def load_data():
    clustered_path = PROJECT_ROOT / "data" / "processed" / "global_budgets_clustered.parquet"
    analyzed_path = PROJECT_ROOT / "data" / "processed" / "global_budgets_analyzed.parquet"
    breaks_path = PROJECT_ROOT / "data" / "processed" / "detected_structural_breaks.csv"
    
    # Load primary dataset
    if clustered_path.exists():
        df = pd.read_parquet(clustered_path)
    elif analyzed_path.exists():
        df = pd.read_parquet(analyzed_path)
    else:
        st.error("❌ Processed dataset not found! Please run Notebook 01 and 03 first.")
        st.stop()
        
    # Ensure Guns-Butter calculation is active
    if 'Guns_Butter_Ratio' not in df.columns:
        df = calculate_guns_butter_index(df)
        
    # Load structural breaks metadata if available
    breaks_df = pd.read_csv(breaks_path) if breaks_path.exists() else pd.DataFrame()
    
    return df, breaks_df

df_master, df_breaks = load_data()

# --- SIDEBAR CONTROLS ---
st.sidebar.title("🌎 Navigation & Filters")
st.sidebar.markdown("---")

# Global Year Slider
min_year = int(df_master['Year'].min())
max_year = int(df_master['Year'].max())
selected_year = st.sidebar.slider("Select Year for Cross-Section / Map", min_year, max_year, 2020)

# Country Selector (Multi-select)
available_countries = sorted(df_master['Country'].dropna().unique())
default_countries = [c for c in ['USA', 'Germany', 'UK', 'India'] if c in available_countries]
if not default_countries and len(available_countries) >= 2:
    default_countries = available_countries[:2]

selected_countries = st.sidebar.multiselect(
    "Select Countries for Time Series Comparison",
    options=available_countries,
    default=default_countries
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Project Context:** Policy Research & Data Journalism Portfolio. "
    "Analyzing sovereign trade-offs between defense spending ('Guns') and domestic welfare ('Butter') across 1936–2026."
)

# --- DASHBOARD HEADER ---
st.title("🌎 Guns vs. Butter: 90 Years of Sovereign Budget Priorities")
st.markdown("An interactive investigation into how national defense, health, education, and social welfare priorities evolve over time.")

# --- TABS LAYOUT ---
tab1, tab2, tab3, tab4 = st.tabs([
    "🗺️ Global Choropleth Map", 
    "📈 Country Trajectories & Regime Shifts", 
    "🏷️ Fiscal Personality Clusters", 
    "📊 Budget Breakdown & Data Table"
])

# ==========================================
# TAB 1: CHOROPLETH MAP
# ==========================================
with tab1:
    st.subheader(f"Global Snapshot: {selected_year}")
    
    df_year = df_master[df_master['Year'] == selected_year].copy()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Countries Tracked", len(df_year))
    col2.metric("Median Defense Allocation", f"{df_year['Defense_Percentage'].median():.1f}%")
    col3.metric("Median Social Allocation", f"{df_year['Social_Total_Percentage'].median():.1f}%")
    col4.metric("Median Guns-Butter Ratio", f"{df_year['Guns_Butter_Ratio'].median():.2f}")
    
    map_metric = st.selectbox(
        "Select Metric to Map:",
        options=['Guns_Butter_Ratio', 'Defense_Percentage', 'Social_Total_Percentage', 'Interest_Payments_Percentage'],
        format_func=lambda x: x.replace('_', ' ')
    )
    
    fig_map = px.choropleth(
        df_year,
        locations="Country",
        locationmode="country names",
        color=map_metric,
        hover_name="Country",
        hover_data=['Total_Budget_Billions_USD', 'Defense_Percentage', 'Social_Total_Percentage'],
        color_continuous_scale="RdBu_r" if map_metric == 'Guns_Butter_Ratio' else "Viridis",
        title=f"Global {map_metric.replace('_', ' ')} in {selected_year}"
    )
    fig_map.update_layout(height=520, margin=dict(l=0, r=0, t=40, b=0))
    st.plotly_chart(fig_map, use_container_width=True)

# ==========================================
# TAB 2: TIME SERIES & REGIME SHIFTS
# ==========================================
with tab2:
    st.subheader("Historical Allocation Trajectories (1936–2026)")
    
    if not selected_countries:
        st.warning("Please select at least one country from the sidebar.")
    else:
        df_selected = df_master[df_master['Country'].isin(selected_countries)].sort_values(['Country', 'Year'])
        
        show_breaks = st.checkbox("Overlay Auto-Detected Structural Breakpoints", value=True)
        
        # Plotting Defense vs Social Over Time
        fig_ts = go.Figure()
        
        for country in selected_countries:
            c_df = df_selected[df_selected['Country'] == country]
            
            # Defense Trace
            fig_ts.add_trace(go.Scatter(
                x=c_df['Year'], y=c_df['Defense_Percentage'],
                mode='lines', name=f"{country} - Defense %",
                line=dict(width=2.5)
            ))
            # Social Trace
            fig_ts.add_trace(go.Scatter(
                x=c_df['Year'], y=c_df['Social_Total_Percentage'],
                mode='lines', name=f"{country} - Social %",
                line=dict(dash='dash', width=2)
            ))
            
            # Overlay Structural Breaks if requested
            if show_breaks and not df_breaks.empty:
                c_breaks = df_breaks[df_breaks['Country'] == country]['Break_Year'].unique()
                for b_yr in c_breaks:
                    fig_ts.add_vline(
                        x=b_yr, line_width=1, line_dash="dot", line_color="red",
                        annotation_text=f"{country} Break: {b_yr}", annotation_position="top left"
                    )
        
        fig_ts.update_layout(
            title="Defense Allocation vs. Combined Social Allocations Over Time",
            xaxis_title="Year",
            yaxis_title="Budget Percentage (%)",
            height=550,
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_ts, use_container_width=True)

# ==========================================
# TAB 3: FISCAL PERSONALITY CLUSTERS
# ==========================================
with tab3:
    st.subheader("Fiscal Personality Types (Machine Learning Classification)")
    
    if 'Fiscal_Personality' in df_master.columns:
        st.markdown(
            "Countries are grouped into four macro fiscal profiles based on their 9 budget allocation signatures: "
            "**Security States**, **Welfare States**, **Debt-Constrained States**, and **Developmental States**."
        )
        
        df_clust_year = df_master[df_master['Year'] == selected_year].dropna(subset=['Fiscal_Personality'])
        
        col_c1, col_c2 = st.columns([1, 2])
        
        with col_c1:
            st.markdown(f"#### Personality Breakdown ({selected_year})")
            personality_counts = df_clust_year['Fiscal_Personality'].value_counts().reset_index()
            personality_counts.columns = ['Personality', 'Count']
            
            fig_pie = px.pie(
                personality_counts, values='Count', names='Personality',
                hole=0.4, color_discrete_sequence=px.colors.qualitative.Set2
            )
            fig_pie.update_layout(height=380, margin=dict(l=0, r=0, t=20, b=0))
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with col_c2:
            st.markdown(f"#### Country Assignments in {selected_year}")
            st.dataframe(
                df_clust_year[['Country', 'Fiscal_Personality', 'Defense_Percentage', 'Social_Total_Percentage', 'Interest_Payments_Percentage']],
                use_container_width=True,
                height=350
            )
    else:
        st.info("💡 Run `notebooks/03_clustering.ipynb` to populate the Fiscal Personality cluster definitions.")

# ==========================================
# TAB 4: RAW DATA & EXPORT
# ==========================================
with tab4:
    st.subheader("Explore & Export Filtered Panel Data")
    
    if selected_countries:
        df_table = df_master[df_master['Country'].isin(selected_countries)].sort_values(['Country', 'Year'])
    else:
        df_table = df_master[df_master['Year'] == selected_year]
        
    st.dataframe(df_table, use_container_width=True)
    
    csv_data = df_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv_data,
        file_name=f"guns_vs_butter_filtered_{selected_year}.csv",
        mime="text/csv"
    )