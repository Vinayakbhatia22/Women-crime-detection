import os
import csv
from collections import defaultdict
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Setup paths
artifact_dir = r"C:\Users\User\.gemini\antigravity-ide\brain\91ee457f-d1d4-48ae-8bc1-85bdf6e32dfd"
os.makedirs(artifact_dir, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Segoe UI', 'DejaVu Sans', 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = True

rows = []
with open('crime_data.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for r in reader:
        rows.append(r)

crime_cols = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
col_labels = {
    'Rape': 'Rape',
    'K&A': 'Kidnapping & Abduction',
    'DD': 'Dowry Deaths',
    'AoW': 'Assault on Women (Molestation)',
    'AoM': 'Insult to Modesty (Eve Teasing)',
    'DV': 'Domestic Violence (Sec 498A)',
    'WT': 'Women Trafficking'
}

for r in rows:
    r['Year'] = int(r['Year'])
    for c in crime_cols:
        r[c] = float(r[c])
    r['Total'] = sum(r[c] for c in crime_cols)

# 1. Yearly aggregation
year_data = defaultdict(lambda: defaultdict(float))
for r in rows:
    y = r['Year']
    for c in crime_cols:
        year_data[y][c] += r[c]
    year_data[y]['Total'] += r['Total']

years = sorted(year_data.keys())
total_crimes = [year_data[y]['Total'] for y in years]

# --- CHART 1: Overall National Crime Trend (2001-2021) with Milestones ---
fig, ax = plt.subplots(figsize=(12, 6), dpi=200)
line = ax.plot(years, total_crimes, color='#4F46E5', linewidth=3, marker='o', markersize=6, label='Total Reported Crimes against Women')
ax.fill_between(years, total_crimes, color='#4F46E5', alpha=0.12)

# Annotate 2013 Nirbhaya Law Impact
y2013 = year_data[2013]['Total']
ax.annotate('2013 Post-Nirbhaya Surge\n(+63,419 / +27.0% YoY)', 
            xy=(2013, y2013), xytext=(2008, 290000),
            arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1.5, headwidth=7),
            fontsize=10, fontweight='bold', color='#991B1B',
            bbox=dict(boxstyle="round,pad=0.4", fc="#FEE2E2", ec="#EF4444", lw=1))

# Annotate 2020 COVID Lockdowns
y2020 = year_data[2020]['Total']
ax.annotate('2020 COVID Dip\n(-31,531 / -9.5% YoY)', 
            xy=(2020, y2020), xytext=(2016, 250000),
            arrowprops=dict(facecolor='#0284C7', shrink=0.08, width=1.5, headwidth=7),
            fontsize=10, fontweight='bold', color='#0369A1',
            bbox=dict(boxstyle="round,pad=0.4", fc="#E0F2FE", ec="#38BDF8", lw=1))

# Annotate 2021 Rebound
y2021 = year_data[2021]['Total']
ax.annotate('2021 Rebound\n(+45,906 / +15.2% YoY)', 
            xy=(2021, y2021), xytext=(2016, 360000),
            arrowprops=dict(facecolor='#059669', shrink=0.08, width=1.5, headwidth=7),
            fontsize=10, fontweight='bold', color='#047857',
            bbox=dict(boxstyle="round,pad=0.4", fc="#D1FAE5", ec="#34D399", lw=1))

ax.set_title('National Trend: Crimes Against Women in India (2001 - 2021)', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=12, labelpad=10)
ax.set_ylabel('Number of Cases Reported', fontsize=12, labelpad=10)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
ax.set_xticks(years)
ax.set_xticklabels(years, rotation=45)
ax.grid(True, linestyle='--', alpha=0.5)

chart1_path = os.path.join(artifact_dir, 'national_crime_trend.png')
plt.savefig(chart1_path, bbox_inches='tight')
plt.close()

# --- CHART 2: Crime Categories Trajectory Stacked Area / Multiline ---
fig, ax = plt.subplots(figsize=(13, 7), dpi=200)
colors = ['#EF4444', '#F59E0B', '#10B981', '#3B82F6', '#8B5CF6', '#EC4899', '#6366F1']

for i, c in enumerate(['DV', 'AoW', 'K&A', 'Rape', 'AoM', 'DD']):
    y_vals = [year_data[y][c] for y in years]
    ax.plot(years, y_vals, label=col_labels[c], linewidth=2.4, marker='s', markersize=4, color=colors[i])

ax.set_title('Evolution of Individual Crime Categories (2001 - 2021)', fontsize=15, fontweight='bold', pad=15)
ax.set_xlabel('Year', fontsize=12, labelpad=10)
ax.set_ylabel('Annual Reported Cases', fontsize=12, labelpad=10)
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
ax.set_xticks(years)
ax.set_xticklabels(years, rotation=45)
ax.legend(frameon=True, facecolor='white', framealpha=0.9, loc='upper left', fontsize=10)
ax.grid(True, linestyle='--', alpha=0.5)

chart2_path = os.path.join(artifact_dir, 'crime_categories_trajectory.png')
plt.savefig(chart2_path, bbox_inches='tight')
plt.close()

# --- CHART 3: Percentage Growth Rates (2001 to 2019 / 2021) ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5.5), dpi=200)

crimes_no_wt = ['K&A', 'DV', 'AoW', 'Rape', 'DD', 'AoM']
growth_19 = [((year_data[2019][c] - year_data[2001][c]) / year_data[2001][c]) * 100 for c in crimes_no_wt]
growth_labels = [col_labels[c] for c in crimes_no_wt]
bar_colors_19 = ['#10B981' if g > 0 else '#EF4444' for g in growth_19]

bars1 = ax1.barh(growth_labels, growth_19, color=bar_colors_19, height=0.6)
ax1.set_title('Growth Rate: 2001 to 2019 (%)', fontsize=13, fontweight='bold')
ax1.set_xlabel('Percentage Change (%)', fontsize=11)
ax1.axvline(0, color='black', linewidth=0.8, linestyle='--')
for b in bars1:
    w = b.get_width()
    ax1.text(w + (10 if w >= 0 else -40), b.get_y() + b.get_height()/2, f"{w:+.1f}%", 
             va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

# Absolute Growth in Cases (2001 to 2019)
abs_growth_19 = [(year_data[2019][c] - year_data[2001][c]) for c in crimes_no_wt]
bars2 = ax2.barh(growth_labels, abs_growth_19, color='#6366F1', height=0.6)
ax2.set_title('Absolute Net Case Increase (2001 to 2019)', fontsize=13, fontweight='bold')
ax2.set_xlabel('Net Additional Cases per Year', fontsize=11)
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
ax2.axvline(0, color='black', linewidth=0.8, linestyle='--')
for b in bars2:
    w = b.get_width()
    ax2.text(w + (1000 if w >= 0 else -8000), b.get_y() + b.get_height()/2, f"{int(w):+,}", 
             va='center', fontsize=9.5, fontweight='bold', color='#1E293B')

plt.suptitle('Fastest Increasing vs Decreasing Crimes Analysis', fontsize=15, fontweight='bold', y=1.02)
chart3_path = os.path.join(artifact_dir, 'crime_growth_comparison.png')
plt.savefig(chart3_path, bbox_inches='tight')
plt.close()

# --- CHART 4: Top 10 State Hotspots (2001-2019 Clean Baseline) ---
state_totals = defaultdict(float)
for r in rows:
    if r['Year'] <= 2019:
        st = r['State'].strip().upper()
        state_totals[st] += r['Total']

sorted_states = sorted(state_totals.items(), key=lambda x: x[1], reverse=True)[:10]
s_names = [x[0].title() for x in sorted_states][::-1]
s_counts = [x[1] for x in sorted_states][::-1]

fig, ax = plt.subplots(figsize=(11, 6), dpi=200)
hotspot_bars = ax.barh(s_names, s_counts, color='#F43F5E', height=0.65)
ax.set_title('Top 10 Crime Hotspot States (Cumulative Reported Cases: 2001 - 2019)', fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel('Total Number of Reported Crimes', fontsize=12, labelpad=10)
ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))

for b in hotspot_bars:
    w = b.get_width()
    ax.text(w + 6000, b.get_y() + b.get_height()/2, f"{int(w):,} ({w/sum(state_totals.values())*100:.1f}%)", 
             va='center', fontsize=9.5, fontweight='bold', color='#881337')

ax.grid(True, linestyle='--', alpha=0.5, axis='x')
chart4_path = os.path.join(artifact_dir, 'top_state_hotspots.png')
plt.savefig(chart4_path, bbox_inches='tight')
plt.close()

print("Charts successfully saved to:", artifact_dir)
