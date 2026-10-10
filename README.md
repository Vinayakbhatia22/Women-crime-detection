# SafeVision Analytics — Crimes Against Women Detection & Analysis (2001–2021)

[![Python 3.11+](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![NCRB Dataset](https://img.shields.io/badge/Data-NCRB%20(2001--2021)-orange)](https://ncrb.gov.in/)
[![Status: Active](https://img.shields.io/badge/Status-Complete-emerald)](#)

SafeVision Analytics is a data science and interactive intelligence platform analyzing 21 years of reported crime against women across 36 Indian States and Union Territories (2001 – 2021) using National Crime Records Bureau (NCRB) datasets.

---

## 🚀 Live Interactive Dashboard

The repository includes a modern glassmorphic web dashboard providing real-time data exploration, dynamic filtering by state, year, and crime category, and analytical visualizations.

To launch the dashboard locally:
```bash
python -m http.server 3000
```
Open your browser at: **`http://localhost:3000`**

---

## 📊 Core Analytical Findings

| Dimension | Primary Insight | Metric / Percentage Change |
| :--- | :--- | :--- |
| **Fastest Increasing Crime (Relative %)** | **Kidnapping & Abduction (`K&A`)** | **+432.0%** (13.6k in 2001 &rarr; 72.8k in 2019 / 75.4k in 2021) |
| **Fastest Increasing Crime (Absolute Volume)** | **Domestic Violence (`DV` - Sec 498A)** | **+76,266** net cases/yr (+155.5%) by 2019 / **+87,202** by 2021 |
| **Crime Decreasing the Most** | **Insult to Modesty / Eve Teasing (`AoM`)** | **-28.14%** drop (9.6k in 2001 &rarr; 6.9k in 2019 / -19.4% in 2021) |
| **Historical Peak Surge Year** | **2013** | **+63,419 cases (+27.0% YoY)** post-Nirbhaya Criminal Law reforms |
| **Year of Largest Crime Decrease** | **2020** | **-31,531 cases (-9.45% YoY)** during national COVID-19 lockdowns |
| **#1 Crime Hotspot State** | **Uttar Pradesh** | **525,428 cases (12.46% of all crimes nationwide)** |
| **Top 6 Hotspots Concentration** | **UP, West Bengal, Rajasthan, Maharashtra, AP, MP** | Account for **56.8%** of all reported crimes across India |

---

## 🏛️ State Hotspots by Crime Category

* **Rape (Sec. 376 IPC)**: Madhya Pradesh (68,251), Uttar Pradesh (44,673), Rajasthan (43,779).
* **Kidnapping & Abduction (Sec. 363-373 IPC)**: Uttar Pradesh (133,105), Bihar (62,355), Assam (60,359).
* **Dowry Deaths (Sec. 304B IPC)**: Uttar Pradesh (40,615), Bihar (24,428), Madhya Pradesh (13,316).
* **Assault on Women / Molestation (Sec. 354 IPC)**: Madhya Pradesh (131,467), Maharashtra (107,366), Uttar Pradesh (98,521).
* **Domestic Violence / Cruelty (Sec. 498A IPC)**: West Bengal (262,229), Rajasthan (201,484), Andhra Pradesh (174,873).
* **Women Trafficking**: Tamil Nadu (4,041), Karnataka (2,799), Andhra Pradesh (2,548).

---

## 🔍 Data Quality & Normalization Insights

1. **2011 AoW Missing Value**: In the 2011 records, Assault on Women was recorded as 0 across all states in the raw scrape, creating an artificial dip in 2011.
2. **2020–2021 State Off-By-One Scraping Shift**: When Jammu & Kashmir was reorganized into a Union Territory in late 2019, NCRB moved J&K to the UTs table. In this raw scraped dataset, rows from index 9 to 35 shifted by one position. Our analytics isolate the clean 2001–2019 baseline to maintain rigorous statistical integrity.

---

## 📁 Repository Structure

```
├── crime_data.csv              # Full normalized 21-year NCRB dataset
├── index.html                  # Glassmorphism Analytics Dashboard
├── index.css                   # Custom CSS styling & responsive design tokens
├── app.js                      # Interactive Chart.js and state filter logic
├── data.js                     # Pre-processed clean dataset for 0ms dashboard load
├── analyze_crime.py            # CLI script for trend & surge statistics
├── detailed_stats.py           # Deep statistical breakdown script
├── generate_visualizations.py  # High-res chart generator using Matplotlib
└── README.md                   # Project documentation
```

---

## 🛠️ Requirements & Setup

To run Python analytical scripts:
```bash
python analyze_crime.py
python detailed_stats.py
```

To run the interactive local dashboard:
```bash
python -m http.server 3000
```
Open `http://localhost:3000` in any modern web browser.