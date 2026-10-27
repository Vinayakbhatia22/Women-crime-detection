"""
SafeCrime: Advanced Data Science & Machine Learning Library for Crimes Against Women Analytics.

This library provides domain-specific modeling for NCRB crime datasets, including:
- Data ingestion, validation, and state normalization.
- Statistical hypothesis testing (Nirbhaya 2013 legal reform impact, Mann-Whitney U, Cohen's d).
- Distribution profiling (Skewness, Kurtosis, CAGR, Gini inequality coefficient).
- Women Safety Risk Index (WSRI) calculation.
- Unsupervised clustering (K-Means & PCA) for state risk tiers.
- Polynomial Ridge regression time-series forecasting with 95% confidence bounds.
- Multivariate anomaly detection using Isolation Forests.
- High-level automated pipelines and visual analytics.
"""

from .config import (
    CRIME_COLS,
    CRIME_LABELS,
    DEFAULT_SEVERITY_WEIGHTS,
    HISTORICAL_ANOMALIES,
    CLUSTER_TIER_META
)
from .data.loader import CrimeDataLoader
from .data.cleaner import DataCleaner
from .stats.hypothesis import PolicyImpactAnalyzer
from .stats.distribution import CrimeDistributionProfiler
from .metrics.risk_index import RiskIndexCalculator
from .models.clustering import CrimeClusterModel
from .models.forecasting import CrimeForecaster
from .models.anomaly import CrimeAnomalyDetector
from .visualization.charts import CrimeVisualizer
from .pipeline import SafeCrimePipeline

__version__ = "1.0.0"
__author__ = "SafeVision Analytics Team"

__all__ = [
    "CRIME_COLS",
    "CRIME_LABELS",
    "DEFAULT_SEVERITY_WEIGHTS",
    "HISTORICAL_ANOMALIES",
    "CLUSTER_TIER_META",
    "CrimeDataLoader",
    "DataCleaner",
    "PolicyImpactAnalyzer",
    "CrimeDistributionProfiler",
    "RiskIndexCalculator",
    "CrimeClusterModel",
    "CrimeForecaster",
    "CrimeAnomalyDetector",
    "CrimeVisualizer",
    "SafeCrimePipeline",
]
