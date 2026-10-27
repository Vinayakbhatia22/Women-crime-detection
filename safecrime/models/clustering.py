"""Unsupervised learning: K-Means clustering and PCA archetyping."""

import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from ..config import CRIME_COLS, CLUSTER_TIER_META

class CrimeClusterModel:
    """
    Unsupervised segmentation of Indian states into 4 distinct risk archetypes
    based on multi-category crime incidence volumes and PCA dimensionality reduction.
    """

    def __init__(self, n_clusters: int = 4, random_state: int = 42):
        self.n_clusters = n_clusters
        self.random_state = random_state
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=15)
        self.pca = PCA(n_components=2, random_state=random_state)
        self.silhouette_score_: float = 0.0
        self.pca_variance_ratio_: np.ndarray = np.array([])
        self.cluster_centers_: pd.DataFrame = pd.DataFrame()
        self.tier_mapping_: Dict[int, Dict[str, Any]] = {}

    def fit_predict(
        self,
        state_avg: pd.DataFrame,
        wsri_series: pd.Series,
        state_total_avg: pd.Series
    ) -> List[Dict[str, Any]]:
        """
        Fit clustering and PCA pipeline on state average crime profiles.
        Returns a list of cluster profiles per state.
        """
        scaled_features = self.scaler.fit_transform(state_avg[CRIME_COLS])
        cluster_labels = self.kmeans.fit_predict(scaled_features)
        self.silhouette_score_ = float(silhouette_score(scaled_features, cluster_labels))

        pca_coords = self.pca.fit_transform(scaled_features)
        self.pca_variance_ratio_ = self.pca.explained_variance_ratio_

        # Determine Cluster Archetypes based on centroid crime volumes
        inv_centers = self.scaler.inverse_transform(self.kmeans.cluster_centers_)
        centers_df = pd.DataFrame(inv_centers, columns=CRIME_COLS)
        centers_df['SumTotal'] = centers_df.sum(axis=1)
        self.cluster_centers_ = centers_df

        # Rank clusters by total crime centroid volume
        sorted_indices = centers_df.sort_values(by='SumTotal', ascending=False).index.tolist()
        
        self.tier_mapping_ = {}
        for rank, cluster_id in enumerate(sorted_indices):
            self.tier_mapping_[cluster_id] = CLUSTER_TIER_META[rank]

        state_clusters = []
        for idx, (state, row) in enumerate(state_avg.iterrows()):
            c_id = int(cluster_labels[idx])
            meta = self.tier_mapping_[c_id]
            state_clusters.append({
                'state': state,
                'cluster_id': c_id,
                'tier': meta['tier'],
                'risk_level': meta['risk'],
                'color': meta['color'],
                'description': meta['desc'],
                'pca_x': round(float(pca_coords[idx, 0]), 3),
                'pca_y': round(float(pca_coords[idx, 1]), 3),
                'wsri': float(wsri_series.get(state, 50.0)),
                'avg_annual_crimes': round(float(state_total_avg.get(state, row.sum())), 1)
            })

        return state_clusters
