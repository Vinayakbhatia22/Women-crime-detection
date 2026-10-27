#!/usr/bin/env python3
"""
SafeVision Analytics: Data Science & Machine Learning Pipeline
--------------------------------------------------------------
Backward-compatible wrapper utilizing the modular 'safecrime' library.
"""

from safecrime.pipeline import SafeCrimePipeline

def run_ds_pipeline():
    print("=" * 60)
    print(">>> SAFEVISION DATA SCIENCE & MACHINE LEARNING PIPELINE")
    print("=" * 60)
    
    pipeline = SafeCrimePipeline('crime_data.csv')
    results = pipeline.run()
    
    meta = results['metadata']
    print(f"Loaded {meta['total_records_processed']} records across {meta['unique_states']} States/UTs")
    print("\n[OK] Engineered Metric: Women Safety Risk Index (WSRI) computed for 36 States/UTs")
    print(f"[OK] Unsupervised K-Means Clustering complete: 4 Tiers identified (Silhouette Score: {meta['silhouette_score']:.3f}, PCA Variance: {sum(meta['pca_variance_ratio'])*100:.1f}%)")
    print(f"[OK] Predictive Model Trained (Ridge Poly-2) | R2 Score: {meta['r2_score']:.3f} | RMSE: {meta['rmse']:,.0f} cases")
    print(f"[OK] Isolation Forest Anomaly Detection identified {len(results['anomalies'])} key national anomalies")
    
    pipeline.export_dashboard_json('ml_data.js')
    print("\n[SUCCESS] ml_data.js written with complete ML models, forecasts, and cluster profiles.")
    print("=" * 60)

if __name__ == '__main__':
    run_ds_pipeline()
