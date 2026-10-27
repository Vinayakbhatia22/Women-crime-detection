import unittest
import numpy as np
import pandas as pd
from safecrime.data.loader import CrimeDataLoader
from safecrime.data.cleaner import DataCleaner
from safecrime.metrics.risk_index import RiskIndexCalculator
from safecrime.stats.hypothesis import PolicyImpactAnalyzer
from safecrime.stats.distribution import CrimeDistributionProfiler
from safecrime.config import CRIME_COLS

class TestMetricsAndStats(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        loader = CrimeDataLoader('crime_data.csv')
        cleaner = DataCleaner()
        cls.df = cleaner.clean(loader.load())
        cls.baseline_df = cleaner.get_clean_baseline(cls.df, max_year=2019)

    def test_wsri_computation(self):
        calculator = RiskIndexCalculator()
        wsri, state_avg = calculator.compute(self.baseline_df)
        
        self.assertIsInstance(wsri, pd.Series)
        # Check scale boundaries [5, 98]
        self.assertGreaterEqual(wsri.min(), 5.0)
        self.assertLessEqual(wsri.max(), 98.0)
        
        # Check leaderboard
        leaderboard = calculator.get_leaderboard(wsri)
        self.assertEqual(len(leaderboard), len(wsri))
        self.assertEqual(leaderboard[0]['state'], 'Uttar Pradesh')

    def test_hypothesis_testing(self):
        analyzer = PolicyImpactAnalyzer()
        results = analyzer.analyze_nirbhaya_law_impact(self.baseline_df)
        
        self.assertIn('Rape', results)
        self.assertIn('Total', results)
        self.assertTrue(results['Rape']['statistically_significant'])
        self.assertGreater(results['Rape']['cohens_d'], 1.0)

    def test_gini_and_cagr(self):
        profiler = CrimeDistributionProfiler()
        yearly = self.df.groupby('Year')[CRIME_COLS].sum().reset_index()
        yearly['Total'] = yearly[CRIME_COLS].sum(axis=1)
        
        cat_prof = profiler.profile_categories(yearly)
        gini_dict = profiler.profile_state_inequality(self.baseline_df)
        
        self.assertIn('Total', gini_dict)
        self.assertGreaterEqual(gini_dict['Total'], 0.0)
        self.assertLessEqual(gini_dict['Total'], 1.0)
        self.assertIn('Rape', cat_prof)

if __name__ == '__main__':
    unittest.main()
