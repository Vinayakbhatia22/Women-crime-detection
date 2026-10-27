"""Data cleaning, state normalization, and baseline isolation."""

import pandas as pd
from typing import Tuple, List, Optional
from ..config import CRIME_COLS, STATE_NORMALIZATION_MAP

class DataCleaner:
    """Normalizes state naming variations, casts numeric types, and partitions clean baselines."""

    @staticmethod
    def clean_state_name(raw_state: str) -> str:
        """Standardize state names across multiple census and NCRB conventions."""
        st = str(raw_state).strip()
        st_title = st.title().replace('&', 'and').replace('  ', ' ')
        
        for key, val in STATE_NORMALIZATION_MAP.items():
            if key.lower() in st.lower() or key.lower() in st_title.lower():
                return val
        return st_title

    def clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """Perform comprehensive data cleaning, type casting, and compute total crime sums."""
        cleaned_df = df.copy()

        # Clean state names
        cleaned_df['State'] = cleaned_df['State'].apply(self.clean_state_name)

        # Cast crime categories to numeric and fill missing with 0
        for col in CRIME_COLS:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce').fillna(0).astype(int)

        # Cast Year to integer
        cleaned_df['Year'] = pd.to_numeric(cleaned_df['Year'], errors='coerce').astype(int)

        # Compute aggregate total per row
        cleaned_df['Total'] = cleaned_df[CRIME_COLS].sum(axis=1)

        return cleaned_df

    def get_clean_baseline(self, df: pd.DataFrame, max_year: int = 2019) -> pd.DataFrame:
        """
        Isolate clean pre-shift baseline (2001-2019) to prevent post-2019 UT restructuring
        off-by-one misalignment from skewing state-level geographic averages.
        """
        return df[df['Year'] <= max_year].copy()
