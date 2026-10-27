#!/usr/bin/env python3
"""
SafeCrime: End-to-End Data Science & Machine Learning Pipeline
---------------------------------------------------------------
This standalone script executes the complete data science analysis
on reported crimes against women across 36 Indian States and Union Territories.

Data Science Modules Leveraged:
- pandas & numpy: Vectorized wrangling, aggregations, and array transformations
- scipy.stats: Hypothesis testing (Mann-Whitney U, t-test, Cohen's d), Gini coefficient
- scikit-learn: KMeans clustering, PCA, Polynomial Ridge Regressor, Isolation Forest
- seaborn & matplotlib: Diagnostic figures and publication charts
"""

import os
import sys
import pandas as pd
import numpy as np

# Ensure safecrime library package is on path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from safecrime import (
    CRIME_COLS,
    CRIME_LABELS,
    CrimeDataLoader,
    DataCleaner,
    RiskIndexCalculator,
    CrimeClusterModel,
    CrimeForecaster,
    CrimeAnomalyDetector,
    PolicyImpactAnalyzer,
    CrimeDistributionProfiler,
    CrimeVisualizer,
    SafeCrimePipeline
)

def run_data_science_study(data_path: str = 'crime_data.csv', export_dashboard: bool = True):
    print("=" * 80)
    print("    SAFECRIME DATA SCIENCE & STATISTICAL INTELLIGENCE STUDY")
    print("    Analyzing 21 Years of Reported Crimes Against Women in India (2001-2021)")
    print("=" * 80)

    # -------------------------------------------------------------------------
    # STAGE 1: DATA INGESTION & QUALITY SANITIZATION
    # -------------------------------------------------------------------------
    print("\n[STAGE 1/7] Ingesting and Sanitizing Dataset...")
    loader = CrimeDataLoader(data_path)
    cleaner = DataCleaner()

    raw_df = loader.load()
    df = cleaner.clean(raw_df)
    baseline_df = cleaner.get_clean_baseline(df, max_year=2019)

    print(f"  -> Raw records: {len(raw_df)} | Clean records: {len(df)}")
    print(f"  -> Clean baseline (2001-2019): {len(baseline_df)} records across {df['State'].nunique()} States/UTs")
    print(f"  -> Total Crimes Recorded (2001-2021): {df['Total'].sum():,}")

    # -------------------------------------------------------------------------
    # STAGE 2: STATISTICAL DISTRIBUTION & REGIONAL INEQUALITY
    # -------------------------------------------------------------------------
    print("\n[STAGE 2/7] Computing Distribution Metrics & Gini Inequality Indices...")
    profiler = CrimeDistributionProfiler()
    yearly_df = df.groupby('Year')[CRIME_COLS].sum().reset_index()
    yearly_df['Total'] = yearly_df[CRIME_COLS].sum(axis=1)

    cat_profiles = profiler.profile_categories(yearly_df)
    gini_scores = profiler.profile_state_inequality(baseline_df)

    print(f"  {'Category':<6} | {'Total Cases':<12} | {'Share %':<8} | {'CAGR (01-21)':<12} | {'Skewness':<9} | {'State Gini':<10}")
    print("  " + "-" * 75)
    for col in CRIME_COLS:
        prof = cat_profiles[col]
        gini = gini_scores.get(col, 0.0)
        print(f"  {col:<6} | {prof['total_volume']:<12,d} | {prof['volume_share_pct']:<7.2f}% | {prof['cagr_2001_2021']:>+10.2f}% | {prof['skewness']:>+8.2f} | {gini:>9.3f}")

    print(f"\n  National Overall Crime Geographic Gini Coefficient: {gini_scores.get('Total', 0.0):.3f}")

    # -------------------------------------------------------------------------
    # STAGE 3: POLICY IMPACT HYPOTHESIS TESTING (2013 NIRBHAYA REFORMS)
    # -------------------------------------------------------------------------
    print("\n[STAGE 3/7] Hypothesis Testing: Impact of 2013 Criminal Law Amendment Act...")
    policy_analyzer = PolicyImpactAnalyzer()
    hypothesis_results = policy_analyzer.analyze_nirbhaya_law_impact(baseline_df)

    print(f"  {'Crime':<6} | {'Pre-2013 Mean':<14} | {'Post-2013 Mean':<14} | {'Change %':<9} | {'p-value (U)':<12} | {'Cohen d':<8} | {'Sig (p<0.05)'}")
    print("  " + "-" * 85)
    for col in CRIME_COLS:
        res = hypothesis_results[col]
        sig_str = "YES (***)" if res['statistically_significant'] else "NO"
        print(f"  {col:<6} | {res['mean_pre_2013']:<14,.0f} | {res['mean_post_2013']:<14,.0f} | {res['percentage_change']:>+7.1f}% | {res['mann_whitney_p_value']:<12.5f} | {res['cohens_d']:>+7.2f} | {sig_str}")

    # -------------------------------------------------------------------------
    # STAGE 4: FEATURE ENGINEERING - WOMEN SAFETY RISK INDEX (WSRI)
    # -------------------------------------------------------------------------
    print("\n[STAGE 4/7] Engineering Women Safety Risk Index (WSRI, scale 5-98)...")
    risk_calc = RiskIndexCalculator()
    wsri_series, state_avg = risk_calc.compute(baseline_df)
    state_total_avg = baseline_df.groupby('State')['Total'].mean()
    leaderboard = risk_calc.get_leaderboard(wsri_series)

    print("  Top 5 High-Risk States (WSRI):")
    for rank, entry in enumerate(leaderboard[:5], 1):
        print(f"    {rank}. {entry['state']:<22} | WSRI Score: {entry['wsri']:>5.1f}/100")

    print("\n  Top 5 Low-Risk States / Safe Havens (WSRI):")
    for rank, entry in enumerate(leaderboard[-5:], 1):
        print(f"    {rank}. {entry['state']:<22} | WSRI Score: {entry['wsri']:>5.1f}/100")

    # -------------------------------------------------------------------------
    # STAGE 5: UNSUPERVISED LEARNING - K-MEANS & PCA DIMENSIONALITY REDUCTION
    # -------------------------------------------------------------------------
    print("\n[STAGE 5/7] Fitting K-Means Clustering & 2D PCA Dimensionality Reduction...")
    cluster_model = CrimeClusterModel(n_clusters=4, random_state=42)
    state_clusters = cluster_model.fit_predict(state_avg, wsri_series, state_total_avg)

    var_ratio = cluster_model.pca_variance_ratio_
    print(f"  -> Silhouette Score: {cluster_model.silhouette_score_:.4f}")
    print(f"  -> PCA Explained Variance: PC1={var_ratio[0]*100:.1f}%, PC2={var_ratio[1]*100:.1f}% (Cumulative: {var_ratio.sum()*100:.1f}%)")
    
    tier_counts = {}
    for sc in state_clusters:
        tier_counts[sc['tier']] = tier_counts.get(sc['tier'], 0) + 1
    for tier, count in tier_counts.items():
        print(f"    - {tier}: {count} States/UTs")

    # -------------------------------------------------------------------------
    # STAGE 6: TIME-SERIES PREDICTIVE FORECASTING (2022-2026)
    # -------------------------------------------------------------------------
    print("\n[STAGE 6/7] Training Polynomial Ridge Regressors (2022-2026 Forecasts)...")
    forecaster = CrimeForecaster(degree=2, alpha=1.0)
    forecasts, historical_fit, metrics = forecaster.fit_predict(yearly_df)

    print(f"  -> Model Performance: R2 Score: {metrics['r2_score']:.4f} | MAE: {metrics['mae']:,.0f} | RMSE: {metrics['rmse']:,.0f}")
    print("  National Crime Projections (with 95% Confidence Intervals):")
    for f in forecasts:
        print(f"    Year {f['year']}: Projected {f['predicted_total']:,} cases (95% CI: [{f['lower_bound_95']:,} - {f['upper_bound_95']:,}])")

    # -------------------------------------------------------------------------
    # STAGE 7: MULTIVARIATE ANOMALY DETECTION (ISOLATION FOREST)
    # -------------------------------------------------------------------------
    print("\n[STAGE 7/7] Multivariate Anomaly Detection via Isolation Forest...")
    anomaly_detector = CrimeAnomalyDetector(contamination=0.15, random_state=42)
    anomalies = anomaly_detector.detect(yearly_df)

    print(f"  Identified {len(anomalies)} structural shock years:")
    for anom in anomalies:
        print(f"    - Year {anom['year']} [{anom['severity']}]: {anom['description']}")

    # -------------------------------------------------------------------------
    # EXPORTING ASSETS & VISUALIZATIONS
    # -------------------------------------------------------------------------
    if export_dashboard:
        print("\n[EXPORT] Updating Browser Analytics Assets (ml_data.js)...")
        pipeline = SafeCrimePipeline(data_path)
        pipeline.run()
        pipeline.export_dashboard_json('ml_data.js')
        print("  -> ml_data.js synchronized successfully.")

    print("\n" + "=" * 80)
    print("  [COMPLETE] SafeCrime Data Science Pipeline executed successfully.")
    print("=" * 80)

if __name__ == '__main__':
    run_data_science_study()
