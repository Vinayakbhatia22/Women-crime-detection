"""Statistical hypothesis testing for legal & policy intervention analysis."""

import numpy as np
import pandas as pd
from scipy import stats
from typing import Dict, Any, List, Optional
from ..config import CRIME_COLS, CRIME_LABELS

class PolicyImpactAnalyzer:
    """
    Evaluates whether legislative or external shocks (e.g., 2013 Criminal Law Amendment,
    2020 COVID Lockdown) induced statistically significant shifts in reporting patterns.
    """

    @staticmethod
    def cohens_d(group1: np.ndarray, group2: np.ndarray) -> float:
        """Compute Cohen's d effect size between two distributions."""
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        pooled_se = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        if pooled_se == 0:
            return 0.0
        return float((np.mean(group2) - np.mean(group1)) / pooled_se)

    def analyze_nirbhaya_law_impact(self, df_clean: pd.DataFrame) -> Dict[str, Any]:
        """
        Compare crime incidence pre-2013 (2001-2012) vs post-2013 (2013-2019)
        using parametric t-tests, non-parametric Mann-Whitney U tests, and effect sizes.
        """
        pre_df = df_clean[df_clean['Year'] < 2013]
        post_df = df_clean[(df_clean['Year'] >= 2013) & (df_clean['Year'] <= 2019)]

        pre_yearly = pre_df.groupby('Year')[CRIME_COLS + ['Total']].sum()
        post_yearly = post_df.groupby('Year')[CRIME_COLS + ['Total']].sum()

        results = {}
        for col in CRIME_COLS + ['Total']:
            s_pre = pre_yearly[col].values
            s_post = post_yearly[col].values

            # Two-sample t-test
            t_stat, p_val_t = stats.ttest_ind(s_post, s_pre, equal_var=False)

            # Non-parametric Mann-Whitney U test (robust to non-normality)
            u_stat, p_val_u = stats.mannwhitneyu(s_post, s_pre, alternative='greater')

            # Effect size
            d_val = self.cohens_d(s_pre, s_post)

            mean_pre = float(np.mean(s_pre))
            mean_post = float(np.mean(s_post))
            pct_change = ((mean_post - mean_pre) / mean_pre) * 100 if mean_pre > 0 else 0.0

            results[col] = {
                'label': CRIME_LABELS.get(col, 'Total Crimes'),
                'mean_pre_2013': round(mean_pre, 1),
                'mean_post_2013': round(mean_post, 1),
                'percentage_change': round(pct_change, 2),
                't_statistic': round(float(t_stat), 4),
                't_test_p_value': round(float(p_val_t), 6),
                'mann_whitney_u': round(float(u_stat), 2),
                'mann_whitney_p_value': round(float(p_val_u), 6),
                'cohens_d': round(float(d_val), 3),
                'statistically_significant': bool(p_val_u < 0.05)
            }

        return results
