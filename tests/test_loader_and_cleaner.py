import unittest
import os
import pandas as pd
from safecrime.data.loader import CrimeDataLoader
from safecrime.data.cleaner import DataCleaner
from safecrime.config import CRIME_COLS

class TestLoaderAndCleaner(unittest.TestCase):

    def setUp(self):
        self.csv_path = 'crime_data.csv'
        self.loader = CrimeDataLoader(self.csv_path)
        self.cleaner = DataCleaner()

    def test_load_dataset_exists(self):
        df = self.loader.load()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 500)
        self.assertIn('State', df.columns)
        self.assertIn('Year', df.columns)
        for col in CRIME_COLS:
            self.assertIn(col, df.columns)

    def test_clean_state_normalization(self):
        df_raw = self.loader.load()
        df_clean = self.cleaner.clean(df_raw)
        
        # Verify no trailing whitespace or lowercase anomalies
        unique_states = df_clean['State'].unique()
        self.assertIn('Andaman & Nicobar', unique_states)
        self.assertIn('Kerala', unique_states)
        self.assertNotIn('KERALAL', unique_states)
        self.assertIn('Total', df_clean.columns)

    def test_baseline_filtering(self):
        df_raw = self.loader.load()
        df_clean = self.cleaner.clean(df_raw)
        baseline = self.cleaner.get_clean_baseline(df_clean, max_year=2019)
        
        self.assertEqual(baseline['Year'].max(), 2019)
        self.assertEqual(baseline['Year'].min(), 2001)

if __name__ == '__main__':
    unittest.main()
