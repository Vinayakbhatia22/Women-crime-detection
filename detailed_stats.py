import csv
from collections import defaultdict

with open('crime_data.csv', 'r') as f:
    rows = list(csv.DictReader(f))

crime_cols = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
crime_names = {
    'Rape': 'Rape (Sec. 376 IPC)',
    'K&A': 'Kidnapping & Abduction (Sec. 363-373 IPC)',
    'DD': 'Dowry Deaths (Sec. 304B IPC)',
    'AoW': 'Assault on Women / Molestation (Sec. 354 IPC)',
    'AoM': 'Insult to Modesty / Eve Teasing (Sec. 509 IPC)',
    'DV': 'Domestic Violence / Cruelty by Husband/Relatives (Sec. 498A IPC)',
    'WT': 'Women Trafficking / Immoral Traffic'
}

for r in rows:
    r['Year'] = int(r['Year'])
    for c in crime_cols:
        r[c] = float(r[c])
    r['Total'] = sum(r[c] for c in crime_cols)

# Yearly totals
year_totals = defaultdict(lambda: defaultdict(float))
for r in rows:
    y = r['Year']
    for c in crime_cols:
        year_totals[y][c] += r[c]
    year_totals[y]['Total'] += r['Total']

years = sorted(year_totals.keys())

print("--- CRIME SUMMARY 2001 vs 2012 vs 2013 vs 2019 vs 2021 ---")
for c in crime_cols:
    v01 = year_totals[2001][c]
    v12 = year_totals[2012][c]
    v13 = year_totals[2013][c]
    v19 = year_totals[2019][c]
    v21 = year_totals[2021][c]
    pct_12_13 = ((v13 - v12) / v12 * 100) if v12 else 0
    pct_01_19 = ((v19 - v01) / v01 * 100) if v01 else 0
    pct_01_21 = ((v21 - v01) / v01 * 100) if v01 else 0
    print(f"{c:<5} | 2001: {v01:8,.0f} | 2012: {v12:8,.0f} | 2013: {v13:8,.0f} (+{pct_12_13:5.1f}%) | 2019: {v19:8,.0f} (+{pct_01_19:6.1f}%) | 2021: {v21:8,.0f} (+{pct_01_21:6.1f}%)")

print("\n--- TOTAL CRIME BY YEAR ---")
for y in years:
    t = year_totals[y]['Total']
    print(f"{y}: {t:,.0f}")

# State cumulative totals (2001-2019 clean period to avoid shift)
state_totals_clean = defaultdict(lambda: defaultdict(float))
for r in rows:
    if r['Year'] <= 2019:
        st = r['State'].strip().upper()
        for c in crime_cols:
            state_totals_clean[st][c] += r[c]
        state_totals_clean[st]['Total'] += r['Total']

sorted_st_clean = sorted(state_totals_clean.items(), key=lambda x: x[1]['Total'], reverse=True)
grand_clean = sum(x[1]['Total'] for x in sorted_st_clean)

print("\n--- TOP 10 STATES (2001-2019 CLEAN BASELINE) ---")
for idx, (st, d) in enumerate(sorted_st_clean[:10], 1):
    share = d['Total'] / grand_clean * 100
    print(f"{idx:2d}. {st:<22}: {d['Total']:10,.0f} ({share:5.2f}%) | DV: {d['DV']:8,.0f} | AoW: {d['AoW']:8,.0f} | K&A: {d['K&A']:8,.0f} | Rape: {d['Rape']:7,.0f}")

