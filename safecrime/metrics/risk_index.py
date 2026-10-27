"""Women Safety Risk Index (WSRI) computation."""

import pandas as pd
from typing import Dict, Optional, Tuple, List
from ..config import CRIME_COLS, DEFAULT_SEVERITY_WEIGHTS

class RiskIndexCalculator:
    """
    Computes the Women Safety Risk Index (WSRI) (scale: 5 to 98) using min-max scaled
    offense rates weighted by legal severity (IPC bodily harm / trauma level).
    """

    def __init__(self, weights: Optional[Dict[str, float]] = None):
        self.weights = weights or DEFAULT_SEVERITY_WEIGHTS

    def compute(self, df_baseline: pd.DataFrame) -> Tuple[pd.Series, pd.DataFrame]:
        """
        Calculates WSRI score for each State / Union Territory based on baseline data.
        Returns:
            - wsri_series: Series of WSRI scores indexed by State
            - state_avg_df: DataFrame of average annual volumes per category
        """
        state_avg = df_baseline.groupby('State')[CRIME_COLS].mean()

        weighted_scores = pd.Series(0.0, index=state_avg.index)
        for col, weight in self.weights.items():
            if col in state_avg.columns:
                c_min = state_avg[col].min()
                c_max = state_avg[col].max()
                scaled = (state_avg[col] - c_min) / (c_max - c_min + 1e-9)
                weighted_scores += scaled * weight

        # Rescale between 5.0 and 98.0 for intuitive human readability
        s_min = weighted_scores.min()
        s_max = weighted_scores.max()
        wsri = 5.0 + (weighted_scores - s_min) / (s_max - s_min + 1e-9) * 93.0
        wsri = wsri.round(1)

        return wsri, state_avg

    def get_leaderboard(self, wsri_series: pd.Series) -> List[Dict[str, float]]:
        """Return sorted leaderboard list of dictionaries for export or visualization."""
        records = [{'state': state, 'wsri': float(score)} for state, score in wsri_series.items()]
        return sorted(records, key=lambda x: x['wsri'], reverse=True)
