"""Dataset loader with validation and schema enforcement."""

import os
import pandas as pd
from typing import Optional, List
from ..config import CRIME_COLS

class CrimeDataLoader:
    """Loads and validates National Crime Records Bureau (NCRB) crime datasets."""

    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> pd.DataFrame:
        """Load CSV data, remove auto-generated index columns, and validate schema."""
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"Dataset not found at: {self.filepath}")

        df = pd.read_csv(self.filepath)

        # Drop unnamed index columns from pandas export/raw scrape
        if 'Unnamed: 0' in df.columns:
            df = df.drop(columns=['Unnamed: 0'])
        elif len(df.columns) > 0 and (df.columns[0] == '' or 'Unnamed' in df.columns[0]):
            df = df.drop(columns=[df.columns[0]])

        # Validate required columns
        required_cols = ['State', 'Year'] + CRIME_COLS
        missing_cols = [c for c in required_cols if c not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns in dataset: {missing_cols}")

        return df
