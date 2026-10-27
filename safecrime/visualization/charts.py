"""Publication-quality visualization utilities for crime analysis."""

import os
from typing import Optional, List, Dict, Any
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
import pandas as pd
import numpy as np
from ..config import CRIME_COLS, CRIME_LABELS

class CrimeVisualizer:
    """Generates analytical charts and visual diagnostics using Matplotlib and Seaborn."""

    def __init__(self, style: str = 'whitegrid'):
        sns.set_theme(style=style)
        plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
        plt.rcParams['font.family'] = 'sans-serif'

    def plot_national_trend(
        self,
        yearly_df: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot longitudinal national crime volume trend with milestone annotations."""
        fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
        years = yearly_df['Year'].values
        totals = yearly_df['Total'].values

        ax.plot(years, totals, color='#4F46E5', linewidth=3, marker='o', markersize=6, label='Reported Crimes Against Women')
        ax.fill_between(years, totals, color='#4F46E5', alpha=0.12)

        # Annotations for key inflection points if present
        if 2013 in years:
            val_2013 = yearly_df.loc[yearly_df['Year'] == 2013, 'Total'].values[0]
            ax.annotate('2013 Nirbhaya Law Reform\n(+27.0% YoY Surge)',
                        xy=(2013, val_2013), xytext=(2008, val_2013 + 30000),
                        arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1.5, headwidth=6),
                        fontsize=9, fontweight='bold', color='#991B1B',
                        bbox=dict(boxstyle="round,pad=0.4", fc="#FEE2E2", ec="#EF4444", lw=1))

        if 2020 in years:
            val_2020 = yearly_df.loc[yearly_df['Year'] == 2020, 'Total'].values[0]
            ax.annotate('2020 COVID Lockdowns\n(-9.5% Dip)',
                        xy=(2020, val_2020), xytext=(2016, val_2020 - 45000),
                        arrowprops=dict(facecolor='#0284C7', shrink=0.08, width=1.5, headwidth=6),
                        fontsize=9, fontweight='bold', color='#0369A1',
                        bbox=dict(boxstyle="round,pad=0.4", fc="#E0F2FE", ec="#38BDF8", lw=1))

        ax.set_title('National Trajectory: Reported Crimes Against Women (2001 - 2021)', fontsize=14, fontweight='bold', pad=14)
        ax.set_xlabel('Year', fontsize=11, labelpad=8)
        ax.set_ylabel('Total Annual Incidents', fontsize=11, labelpad=8)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
        ax.set_xticks(years)
        ax.set_xticklabels(years, rotation=45)
        ax.grid(True, linestyle='--', alpha=0.5)

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            fig.savefig(save_path, bbox_inches='tight')

        return fig

    def plot_clusters_pca(
        self,
        state_clusters: List[Dict[str, Any]],
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot 2D PCA state risk clusters with tier color coding."""
        fig, ax = plt.subplots(figsize=(11, 7), dpi=150)

        for sc in state_clusters:
            ax.scatter(sc['pca_x'], sc['pca_y'], color=sc['color'], s=sc['wsri'] * 2.5, alpha=0.8, edgecolors='none')
            ax.text(sc['pca_x'] + 0.08, sc['pca_y'], sc['state'], fontsize=8, alpha=0.85)

        ax.set_title('State Crime Archetypes: 2D PCA Projection & K-Means Clusters', fontsize=14, fontweight='bold', pad=14)
        ax.set_xlabel('Principal Component 1 (Crime Volume Scale)', fontsize=11)
        ax.set_ylabel('Principal Component 2 (Offense Distribution Shift)', fontsize=11)
        ax.grid(True, linestyle='--', alpha=0.4)

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            fig.savefig(save_path, bbox_inches='tight')

        return fig

    def plot_forecast(
        self,
        historical_fit: List[Dict[str, Any]],
        forecasts: List[Dict[str, Any]],
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot historical trends alongside Ridge polynomial projections and 95% confidence intervals."""
        fig, ax = plt.subplots(figsize=(12, 6), dpi=150)

        hist_years = [h['year'] for h in historical_fit]
        hist_actual = [h['actual'] for h in historical_fit]
        hist_fitted = [h['fitted'] for h in historical_fit]

        fore_years = [f['year'] for f in forecasts]
        fore_pred = [f['predicted_total'] for f in forecasts]
        lower_bound = [f['lower_bound_95'] for f in forecasts]
        upper_bound = [f['upper_bound_95'] for f in forecasts]

        # Historical actual & fitted
        ax.plot(hist_years, hist_actual, 'o-', color='#1E293B', label='Historical Reported Cases', linewidth=2.2, markersize=5)
        ax.plot(hist_years, hist_fitted, '--', color='#6366F1', label='Polynomial Regression Fit (In-Sample)', linewidth=2)

        # Forecast & Confidence Band
        bridge_years = [hist_years[-1]] + fore_years
        bridge_preds = [hist_actual[-1]] + fore_pred
        ax.plot(bridge_years, bridge_preds, 's--', color='#EF4444', label='Machine Learning Forecast (2022-2026)', linewidth=2.5, markersize=6)
        
        ax.fill_between(
            fore_years,
            lower_bound,
            upper_bound,
            color='#EF4444',
            alpha=0.15,
            label='95% Prediction Interval'
        )

        ax.set_title('Longitudinal Prediction & Trend Projections (2022 - 2026)', fontsize=14, fontweight='bold', pad=14)
        ax.set_xlabel('Year', fontsize=11)
        ax.set_ylabel('Incidents Reported', fontsize=11)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
        ax.set_xticks(hist_years + fore_years)
        ax.set_xticklabels(hist_years + fore_years, rotation=45)
        ax.grid(True, linestyle='--', alpha=0.4)
        ax.legend(loc='upper left', frameon=True)

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            fig.savefig(save_path, bbox_inches='tight')

        return fig

    def plot_correlation_heatmap(
        self,
        corr_matrix: pd.DataFrame,
        save_path: Optional[str] = None
    ) -> plt.Figure:
        """Plot a clean Seaborn heatmap of inter-crime category correlations."""
        fig, ax = plt.subplots(figsize=(8, 6), dpi=150)
        sns.heatmap(
            corr_matrix,
            annot=True,
            fmt=".2f",
            cmap="mako",
            cbar=True,
            square=True,
            linewidths=0.5,
            ax=ax
        )
        ax.set_title('Inter-Crime Correlation Matrix (Pearson)', fontsize=13, fontweight='bold', pad=12)

        if save_path:
            os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
            fig.savefig(save_path, bbox_inches='tight')

        return fig
