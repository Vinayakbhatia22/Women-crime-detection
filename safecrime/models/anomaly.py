"""Multivariate anomaly detection using Isolation Forests."""

import numpy as np
import pandas as pd
from typing import Dict, List, Any, Optional
from sklearn.ensemble import IsolationForest
from ..config import CRIME_COLS, HISTORICAL_ANOMALIES

class CrimeAnomalyDetector:
    """
    Multivariate anomaly detection module using Isolation Forest to identify
    structural shocks, reporting shifts, or unprecedented spikes in crime time-series.
    """

    def __init__(self, contamination: float = 0.15, random_state: int = 42):
        self.contamination = contamination
        self.random_state = random_state
        self.iso_forest = IsolationForest(contamination=contamination, random_state=random_state)

    def detect(self, yearly_df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Detect anomalies across yearly national multi-category vectors and attach domain explanations.
        """
        features = yearly_df[CRIME_COLS].values
        preds = self.iso_forest.fit_predict(features)
        scores = self.iso_forest.decision_function(features)

        anomalies = []
        for idx, yr in enumerate(yearly_df['Year'].values):
            yr = int(yr)
            is_statistical_outlier = (preds[idx] == -1)
            has_domain_anomaly = (yr in HISTORICAL_ANOMALIES)

            if is_statistical_outlier or has_domain_anomaly:
                anomalies.append({
                    'year': yr,
                    'anomaly_score': round(float(scores[idx]), 3),
                    'total_crimes': int(yearly_df.loc[yearly_df['Year'] == yr, 'Total'].values[0]),
                    'severity': 'Critical' if yr in [2013, 2020] else 'Elevated',
                    'description': HISTORICAL_ANOMALIES.get(
                        yr,
                        f"Statistical distribution outlier detected by Isolation Forest (Decision score: {scores[idx]:.3f})"
                    )
                })

        anomalies.sort(key=lambda x: x['year'])
        return anomalies
