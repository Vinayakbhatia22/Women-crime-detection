"""Distributional analysis, inequality metrics, and descriptive statistics."""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any, List
from ..config import CRIME_COLS, CRIME_LABELS

class CrimeDistributionProfiler:
    """Profiles crime distribution shapes, inequality, and growth rates."""

    @staticmethod
    def gini_coefficient(values: np.ndarray) -> float:
        """
        Calculate Gini coefficient measuring geographic concentration inequality of crime.
        0 = completely uniform distribution, 1 = total concentration in a single state.
        """
        arr = np.sort(values.astype(float))
        n = len(arr)
        if n == 0 or np.sum(arr) == 0:
            return 0.0
        index = np.arange(1, n + 1)
        return float(((2 * np.sum(index * arr)) / (n * np.sum(arr))) - ((n + 1) / n))

    @staticmethod
    def calculate_cagr(start_val: float, end_val: float, num_periods: int) -> float:
        """Calculate Compound Annual Growth Rate (CAGR) in percent."""
        if start_val <= 0 or num_periods <= 0:
            return 0.0
        return float(((end_val / start_val) ** (1.0 / num_periods) - 1.0) * 100)

    def profile_categories(self, yearly_df: pd.DataFrame) -> Dict[str, Any]:
        """Compute skewness, kurtosis, CAGR, and total volume shares across categories."""
        grand_total = yearly_df['Total'].sum()
        num_years = len(yearly_df)

        profiles = {}
        for col in CRIME_COLS:
            vals = yearly_df[col].values
            col_total = np.sum(vals)
            cagr = self.calculate_cagr(vals[0], vals[-1], num_years - 1)

            profiles[col] = {
                'label': CRIME_LABELS.get(col, col),
                'total_volume': int(col_total),
                'volume_share_pct': round(float((col_total / grand_total) * 100), 2),
                'mean': round(float(np.mean(vals)), 1),
                'std_dev': round(float(np.std(vals, ddof=1)), 1),
                'skewness': round(float(stats.skew(vals)), 3),
                'kurtosis': round(float(stats.kurtosis(vals)), 3),
                'cagr_2001_2021': round(cagr, 2)
            }

        return profiles

    def profile_state_inequality(self, baseline_df: pd.DataFrame) -> Dict[str, float]:
        """Compute state-level Gini inequality coefficients for each crime type."""
        state_totals = baseline_df.groupby('State')[CRIME_COLS + ['Total']].sum()
        gini_dict = {}
        for col in CRIME_COLS + ['Total']:
            vals = state_totals[col].values
            gini_dict[col] = round(self.gini_coefficient(vals), 3)

        return gini_dict
