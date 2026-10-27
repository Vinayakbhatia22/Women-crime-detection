# SafeVision Analytics — Crimes Against Women Detection & Data Science Library

[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/CI%2FCD-Passing-brightgreen?logo=githubactions&logoColor=white)](.github/workflows/ci.yml)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![SciPy](https://img.shields.io/badge/SciPy-8CAAE6?logo=scipy&logoColor=white)](https://scipy.org/)
[![Pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![NCRB Dataset](https://img.shields.io/badge/Data-NCRB%20(2001--2021)-orange)](https://ncrb.gov.in/)

SafeVision is an open-source Python Data Science & Machine Learning library (`safecrime`) coupled with an interactive web intelligence platform for analyzing 21 years of longitudinal crime records against women across 36 Indian States and Union Territories (2001–2021) based on official National Crime Records Bureau (NCRB) data.

---

## 🏛️ Architecture & Project Structure

```
Women-crime-detection/
├── safecrime/                      # Production Python Data Science Library
│   ├── __init__.py                 # Public API exports
│   ├── config.py                   # Legal IPC mappings, weights & constants
│   ├── pipeline.py                 # SafeCrimePipeline facade orchestrator
│   ├── data/
│   │   ├── loader.py               # CSV schema validation & ingestion
│   │   └── cleaner.py              # State normalization & baseline isolation
│   ├── stats/
│   │   ├── hypothesis.py           # SciPy policy tests (Mann-Whitney U, Cohen's d)
│   │   └── distribution.py         # Skewness, Kurtosis, CAGR & Gini inequality
│   ├── metrics/
│   │   └── risk_index.py           # Women Safety Risk Index (WSRI, scale 5-98)
│   ├── models/
│   │   ├── clustering.py           # K-Means (k=4) & 2D PCA archetyping
│   │   ├── forecasting.py          # Polynomial Ridge Regressor (2022-2026)
│   │   └── anomaly.py              # Isolation Forest multivariate shock detection
│   └── visualization/
│       └── charts.py               # Matplotlib & Seaborn publication figures
├── notebooks/
│   └── crime_data_science_analysis.ipynb # Interactive Jupyter Data Science Notebook
├── tests/                          # Automated unit and integration test suite
│   ├── test_loader_and_cleaner.py
│   ├── test_metrics_and_stats.py
│   └── test_models_and_pipeline.py
├── examples/
│   └── quickstart.py               # 15-line quickstart demo
├── .github/workflows/
│   └── ci.yml                      # GitHub Actions automated test & lint CI/CD
├── crime_data_science.py           # Primary standalone Data Science CLI study
├── crime_data.csv                  # 21-year NCRB longitudinal dataset
├── index.html                      # Glassmorphism Web Analytics Dashboard
├── index.css                       # Modern responsive CSS design tokens
├── app.js                          # Dynamic Chart.js and state filtering logic
├── pyproject.toml                  # Modern PEP 517/518 build specification
├── setup.py                        # Pip installation configuration
├── requirements.txt                # Pinned production dependencies
├── LICENSE                         # MIT Open Source License
└── README.md                       # Documentation
```

---

## ⚡ Installation & Quickstart

### 1. Install as a Python Library
Clone the repository and install the `safecrime` library in editable mode:
```bash
git clone https://github.com/Vinayakbhatia22/Women-crime-detection.git
cd Women-crime-detection
pip install -r requirements.txt
pip install -e .
```

### 2. Run the Primary Data Science CLI Study
Execute the complete multi-stage data science study:
```bash
python crime_data_science.py
```

### 3. Quickstart Example
```python
from safecrime import SafeCrimePipeline, CrimeDataLoader, RiskIndexCalculator

# High-Level Unified Pipeline
pipeline = SafeCrimePipeline("crime_data.csv")
results = pipeline.run()

print(f"Model R2 Score: {results['metadata']['r2_score']:.4f}")
print("Top 3 High-Risk States:", [s['state'] for s in results['wsri_leaderboard'][:3]])
```

### 4. Interactive Jupyter Notebook
Launch the complete exploratory data science and statistical analysis:
```bash
jupyter notebook notebooks/crime_data_science_analysis.ipynb
```

### 5. Launch the Web Dashboard
```bash
python -m http.server 3000
```
Open **`http://localhost:3000`** in your browser to explore the dashboard.

---

## 🔬 Data Science & Statistical Methodology

| Component | Library & Method | Scientific Objective | Result / Performance |
| :--- | :--- | :--- | :--- |
| **Statistical Inequality** | `scipy.stats` / Gini Index | Spatial concentration of crime across 36 states | National Geographic Gini: **0.625** |
| **Policy Shock Testing** | `scipy.stats.mannwhitneyu` | Impact of 2013 Nirbhaya Criminal Law Amendment | Significant surge across Rape ($p < 0.0001, d = 5.09$) |
| **Feature Engineering** | Min-Max Severity Scaling | Women Safety Risk Index (**WSRI**, 5 - 98) | UP: **98.0**, MP: **77.2**, Nagaland: **5.2** |
| **Unsupervised Archetypes**| `sklearn.cluster.KMeans` + `PCA` | Group states into 4 actionable risk tiers | Silhouette Score: **0.532**, PCA Explained: **79.7%** |
| **Predictive Forecasting** | `sklearn.linear_model.Ridge` Poly-2 | 2022–2026 trajectory forecast with 95% CI | **$R^2 = 0.886$**, **RMSE = 27,785** cases |
| **Anomaly Detection** | `sklearn.ensemble.IsolationForest` | Multi-category structural shock identification | Detected 2013 reform spike & 2020 COVID lockdown dip |

---

## 🧪 Running Automated Tests

Run the full automated test suite across all library modules:
```bash
python -m unittest discover tests
```

---

## 📄 License
This project is open-source and distributed under the **[MIT License](LICENSE)**.