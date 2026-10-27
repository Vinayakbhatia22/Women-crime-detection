import unittest
import os
import pandas as pd
from safecrime.pipeline import SafeCrimePipeline
from safecrime.models.clustering import CrimeClusterModel
from safecrime.models.forecasting import CrimeForecaster
from safecrime.models.anomaly import CrimeAnomalyDetector
from safecrime.config import CRIME_COLS

class TestModelsAndPipeline(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pipeline = SafeCrimePipeline('crime_data.csv')
        cls.results = cls.pipeline.run()

    def test_pipeline_execution(self):
        self.assertIn('metadata', self.results)
        self.assertIn('state_clusters', self.results)
        self.assertIn('forecasts', self.results)
        self.assertIn('anomalies', self.results)
        self.assertIn('correlations', self.results)
        self.assertGreater(self.results['metadata']['r2_score'], 0.80)
        self.assertGreater(self.results['metadata']['silhouette_score'], 0.40)

    def test_forecast_confidence_intervals(self):
        forecasts = self.results['forecasts']
        self.assertEqual(len(forecasts), 5) # 2022 to 2026
        for f in forecasts:
            self.assertGreater(f['predicted_total'], 0)
            self.assertLess(f['lower_bound_95'], f['predicted_total'])
            self.assertGreater(f['upper_bound_95'], f['predicted_total'])

    def test_anomaly_detection(self):
        anomalies = self.results['anomalies']
        years = [a['year'] for a in anomalies]
        self.assertIn(2013, years)
        self.assertIn(2020, years)

    def test_export_dashboard_json(self):
        test_export = 'test_ml_data.js'
        self.pipeline.export_dashboard_json(test_export)
        self.assertTrue(os.path.exists(test_export))
        if os.path.exists(test_export):
            os.remove(test_export)

if __name__ == '__main__':
    unittest.main()
