"""SafeCrime end-to-end data science pipeline orchestrator."""

import json
from typing import Dict, Any, Optional, List
import pandas as pd

from .config import CRIME_COLS, CRIME_LABELS
from .data.loader import CrimeDataLoader
from .data.cleaner import DataCleaner
from .metrics.risk_index import RiskIndexCalculator
from .models.clustering import CrimeClusterModel
from .models.forecasting import CrimeForecaster
from .models.anomaly import CrimeAnomalyDetector

class SafeCrimePipeline:
    """
    End-to-end pipeline facade encapsulating data ingestion, cleaning,
    feature engineering, unsupervised clustering, predictive time-series modeling,
    and anomaly detection.
    """

    def __init__(self, filepath: str = 'crime_data.csv'):
        self.filepath = filepath
        self.loader = CrimeDataLoader(filepath)
        self.cleaner = DataCleaner()
        self.risk_calc = RiskIndexCalculator()
        self.cluster_model = CrimeClusterModel()
        self.forecaster = CrimeForecaster()
        self.anomaly_detector = CrimeAnomalyDetector()

        # State storage
        self.raw_df: Optional[pd.DataFrame] = None
        self.clean_df: Optional[pd.DataFrame] = None
        self.baseline_df: Optional[pd.DataFrame] = None
        self.yearly_df: Optional[pd.DataFrame] = None
        self.results: Dict[str, Any] = {}

    def run(self) -> Dict[str, Any]:
        """Execute complete analytical and machine learning workflow."""
        # 1. Ingestion & Preprocessing
        self.raw_df = self.loader.load()
        self.clean_df = self.cleaner.clean(self.raw_df)
        self.baseline_df = self.cleaner.get_clean_baseline(self.clean_df, max_year=2019)

        # 2. Risk Metrics (WSRI)
        wsri_series, state_avg = self.risk_calc.compute(self.baseline_df)
        state_total_avg = self.baseline_df.groupby('State')['Total'].mean()
        wsri_leaderboard = self.risk_calc.get_leaderboard(wsri_series)

        # 3. Clustering & Archetyping
        state_clusters = self.cluster_model.fit_predict(state_avg, wsri_series, state_total_avg)

        # 4. Aggregations & Longitudinal Modeling
        self.yearly_df = self.clean_df.groupby('Year')[CRIME_COLS].sum().reset_index()
        self.yearly_df['Total'] = self.yearly_df[CRIME_COLS].sum(axis=1)

        forecasts, historical_fit, forecast_metrics = self.forecaster.fit_predict(self.yearly_df)

        # 5. Anomaly Detection
        anomalies = self.anomaly_detector.detect(self.yearly_df)

        # 6. Correlation Analysis
        corr_matrix = self.baseline_df[CRIME_COLS].corr().round(3).to_dict()

        # 7. Synthesize Results
        self.results = {
            "metadata": {
                "model_version": "SafeCrime v2.5",
                "algorithms": [
                    "K-Means (k=4)",
                    "PCA (2D)",
                    "Ridge Polynomial-2 Regressor",
                    "Isolation Forest"
                ],
                "r2_score": forecast_metrics['r2_score'],
                "mae": forecast_metrics['mae'],
                "rmse": forecast_metrics['rmse'],
                "silhouette_score": round(self.cluster_model.silhouette_score_, 4),
                "pca_variance_ratio": [round(float(v), 4) for v in self.cluster_model.pca_variance_ratio_],
                "forecast_horizon": "2022 - 2026",
                "total_records_processed": len(self.clean_df),
                "unique_states": int(self.clean_df['State'].nunique())
            },
            "state_clusters": state_clusters,
            "wsri_leaderboard": wsri_leaderboard,
            "forecasts": forecasts,
            "anomalies": anomalies,
            "correlations": corr_matrix,
            "historical_fit": historical_fit
        }

        return self.results

    def export_dashboard_json(self, output_path: str = 'ml_data.js') -> None:
        """Export computed machine learning assets as a browser-ready JS bundle."""
        if not self.results:
            self.run()

        js_content = (
            "// SafeVision Machine Learning & Data Science Intelligence Pipeline Asset\n"
            f"window.ML_DATA = {json.dumps(self.results, indent=2)};\n"
        )
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(js_content)

    def export_data_js(self, output_path: str = 'data.js') -> None:
        """Export raw and preprocessed historical records as a browser-ready JS bundle."""
        if self.clean_df is None:
            self.raw_df = self.loader.load()
            self.clean_df = self.cleaner.clean(self.raw_df)

        records = []
        for _, row in self.clean_df.iterrows():
            rec = {
                'state': row['State'],
                'year': int(row['Year']),
                'total': int(row['Total'])
            }
            for col in CRIME_COLS:
                rec[col] = int(row[col])
            records.append(rec)

        js_content = (
            "// Generated Crime Data for Analytics Dashboard\n"
            f"window.CRIME_DATA = {json.dumps(records, indent=2)};\n"
            f"window.CRIME_COLS = {json.dumps(CRIME_COLS)};\n"
            f"window.CRIME_LABELS = {json.dumps(CRIME_LABELS)};\n"
        )
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(js_content)
