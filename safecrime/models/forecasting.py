"""Time-series predictive forecasting using polynomial Ridge regression."""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from sklearn.linear_model import Ridge
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from ..config import CRIME_COLS

class CrimeForecaster:
    """
    Polynomial Ridge Regression forecaster for longitudinal crime trajectories.
    Models non-linear historical inflection points while regularizing against explosive growth.
    """

    def __init__(self, degree: int = 2, alpha: float = 1.0):
        self.degree = degree
        self.alpha = alpha
        self.poly = PolynomialFeatures(degree=degree)
        self.model_total = Ridge(alpha=alpha)
        self.cat_models: Dict[str, Ridge] = {}
        self.metrics_: Dict[str, float] = {}

    def fit_predict(
        self,
        yearly_df: pd.DataFrame,
        future_years: Optional[List[int]] = None
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, float]]:
        """
        Fit polynomial models across total crimes and individual crime categories.
        Returns:
            - forecast_records: Predictions for future years with 95% confidence intervals
            - historical_fit: In-sample fitted values versus actuals
            - metrics: Dict containing r2, mae, rmse
        """
        if future_years is None:
            future_years = [2022, 2023, 2024, 2025, 2026]

        X_years = yearly_df['Year'].values.reshape(-1, 1)
        future_arr = np.array(future_years).reshape(-1, 1)

        X_poly = self.poly.fit_transform(X_years)
        X_future_poly = self.poly.transform(future_arr)

        # 1. Total Crimes Model
        y_total = yearly_df['Total'].values
        self.model_total.fit(X_poly, y_total)
        y_pred_hist = self.model_total.predict(X_poly)
        y_future_pred = self.model_total.predict(X_future_poly)

        r2 = float(r2_score(y_total, y_pred_hist))
        mae = float(mean_absolute_error(y_total, y_pred_hist))
        rmse = float(np.sqrt(mean_squared_error(y_total, y_pred_hist)))

        self.metrics_ = {
            'r2_score': round(r2, 4),
            'mae': round(mae, 1),
            'rmse': round(rmse, 1)
        }

        # 2. Individual Category Models
        cat_forecasts = {}
        for col in CRIME_COLS:
            cat_model = Ridge(alpha=self.alpha)
            y_col = yearly_df[col].values
            cat_model.fit(X_poly, y_col)
            self.cat_models[col] = cat_model
            preds = cat_model.predict(X_future_poly)
            cat_forecasts[col] = [max(0, int(round(p))) for p in preds]

        # 3. Format Future Forecast Records with 95% Confidence Bounds
        forecast_records = []
        for idx, (yr, pred_tot) in enumerate(zip(future_years, y_future_pred)):
            f_rec = {
                'year': int(yr),
                'is_forecast': True,
                'predicted_total': int(round(pred_tot)),
                'lower_bound_95': int(round(pred_tot - 1.96 * rmse)),
                'upper_bound_95': int(round(pred_tot + 1.96 * rmse))
            }
            for col in CRIME_COLS:
                f_rec[col] = cat_forecasts[col][idx]
            forecast_records.append(f_rec)

        # 4. Format Historical In-Sample Fit Records
        historical_fit = [
            {'year': int(yr), 'actual': int(actual), 'fitted': int(round(fitted))}
            for yr, actual, fitted in zip(yearly_df['Year'].values, y_total, y_pred_hist)
        ]

        return forecast_records, historical_fit, self.metrics_
