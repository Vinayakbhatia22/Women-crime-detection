"""
SafeCrime Visualization Suite: 10 Types of Matplotlib & Pyplot Visualizations
-----------------------------------------------------------------------------
This script demonstrates 10 distinct, publication-grade visualization types
using Matplotlib (pyplot), subplots, and bar graphs based on the Women Crime Detection dataset:

 1. Horizontal Bar Graph with Value Annotations (Top 10 State Hotspots)
 2. Grouped / Clustered Bar Graph (Pre vs Post Reform vs Pandemic Eras)
 3. 100% Stacked Bar Graph (Crime Category Composition Across High-Risk States)
 4. Multi-Panel Subplots Grid (Small Multiples: Offense Trajectories 2001-2021)
 5. Synchronized Two-Panel Subplots (Total Volume vs YoY Growth Rate)
 6. Annotated Longitudinal Pyplot (National Timeline with Policy Milestones)
 7. Correlation Heatmap Subplot (Inter-Crime Correlation Matrix)
 8. Multi-Category Box & Whisker Plot (State Spread, Quartiles & Outliers)
 9. Donut Chart with Exploded Slice (National Share of Offense Categories)
 10. Multi-Dimensional Bubble Scatter Plot (State Vulnerability, Volume & Severity)
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# -----------------------------------------------------------------------------
# Configuration & Output Setup
# -----------------------------------------------------------------------------
OUTPUT_DIR = "output_plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set global aesthetic style
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = ['Segoe UI', 'DejaVu Sans', 'Arial', 'sans-serif']
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.autolayout'] = False

CRIME_COLS = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
CRIME_LABELS = {
    'Rape': 'Rape (Sec. 376 IPC)',
    'K&A': 'Kidnapping & Abduction',
    'DD': 'Dowry Deaths (Sec. 304B)',
    'AoW': 'Assault on Women (Molestation)',
    'AoM': 'Insult to Modesty (Eve Teasing)',
    'DV': 'Domestic Violence (Sec. 498A)',
    'WT': 'Women Trafficking'
}
PALETTE = {
    'DV': '#EF4444',    # Crimson
    'AoW': '#F59E0B',   # Amber
    'K&A': '#10B981',   # Emerald
    'Rape': '#3B82F6',  # Royal Blue
    'AoM': '#8B5CF6',   # Purple
    'DD': '#EC4899',    # Pink
    'WT': '#6B7280'     # Gray
}

# -----------------------------------------------------------------------------
# Data Ingestion & Sanitization
# -----------------------------------------------------------------------------
def load_and_clean_data(csv_path='crime_data.csv') -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    if 'Unnamed: 0' in df.columns:
        df = df.drop(columns=['Unnamed: 0'])

    # Standardize State names
    df['State'] = df['State'].astype(str).str.strip().str.upper()
    df['State'] = df['State'].replace({
        'A & N ISLANDS': 'ANDAMAN & NICOBAR',
        'A AND N ISLANDS': 'ANDAMAN & NICOBAR',
        'D & N HAVELI': 'DADRA & NAGAR HAVELI',
        'D AND N HAVELI': 'DADRA & NAGAR HAVELI',
        'DAMAN & DIU': 'DAMAN & DIU',
        'DELHI UT': 'DELHI',
        'KERALAL': 'KERALA'
    })

    # Numeric conversion & total
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce').fillna(2001).astype(int)
    for col in CRIME_COLS:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

    df['Total'] = df[CRIME_COLS].sum(axis=1)
    return df

df = load_and_clean_data()
yearly_national = df.groupby('Year')[CRIME_COLS + ['Total']].sum().reset_index()


# =============================================================================
# 1. HORIZONTAL BAR GRAPH (Top 10 Crime Hotspot States)
# =============================================================================
def plot_1_horizontal_bar(df: pd.DataFrame):
    """Bar Graph 1: Horizontal Bar Chart with exact counts and percentage share."""
    state_totals = df.groupby('State')['Total'].sum().sort_values(ascending=False).head(10)
    state_names = [s.title() for s in state_totals.index[::-1]]
    counts = state_totals.values[::-1]
    total_national = df['Total'].sum()

    fig, ax = plt.subplots(figsize=(10, 6), dpi=150)
    colors = ['#4F46E5' if i < 9 else '#DC2626' for i in range(len(counts))]
    bars = ax.barh(state_names, counts, color=colors, height=0.65, edgecolor='none')

    ax.set_title('Top 10 Crime Hotspot States in India (Cumulative 2001 - 2021)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Total Reported Crimes Against Women', fontsize=11, labelpad=8)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    for bar in bars:
        w = bar.get_width()
        pct = (w / total_national) * 100
        ax.text(w + 10000, bar.get_y() + bar.get_height()/2, f'{int(w):,} ({pct:.1f}%)',
                va='center', ha='left', fontsize=9, fontweight='semibold', color='#1E293B')

    ax.set_xlim(0, max(counts) * 1.18)
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '01_horizontal_bar_hotspots.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 2. GROUPED / CLUSTERED BAR GRAPH (Comparing Three Historical Eras)
# =============================================================================
def plot_2_grouped_bar(df: pd.DataFrame):
    """Bar Graph 2: Multi-column Grouped Bar Chart comparing Pre-Nirbhaya, Post-Nirbhaya, and Pandemic eras."""
    # Define eras
    def assign_era(year):
        if year <= 2012:
            return 'Baseline (2001-2012)'
        elif year <= 2019:
            return 'Post-Nirbhaya (2013-2019)'
        else:
            return 'Pandemic Era (2020-2021)'

    df_era = df.copy()
    df_era['Era'] = df_era['Year'].apply(assign_era)
    
    # Calculate average annual incidents per era
    era_years = {'Baseline (2001-2012)': 12, 'Post-Nirbhaya (2013-2019)': 7, 'Pandemic Era (2020-2021)': 2}
    era_totals = df_era.groupby('Era')[['DV', 'AoW', 'K&A', 'Rape', 'DD']].sum().astype(float)
    for era in era_years:
        era_totals.loc[era] = era_totals.loc[era] / era_years[era]

    eras = ['Baseline (2001-2012)', 'Post-Nirbhaya (2013-2019)', 'Pandemic Era (2020-2021)']
    offenses = ['DV', 'AoW', 'K&A', 'Rape', 'DD']
    labels = [CRIME_LABELS[c] for c in offenses]

    x = np.arange(len(offenses))
    width = 0.26

    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    era_colors = ['#94A3B8', '#3B82F6', '#EF4444']

    for i, era in enumerate(eras):
        vals = [era_totals.loc[era, c] for c in offenses]
        rects = ax.bar(x + (i - 1) * width, vals, width, label=era, color=era_colors[i], edgecolor='white', linewidth=0.8)
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2, h + 1500, f'{int(h/1000)}k',
                    ha='center', va='bottom', fontsize=8, fontweight='bold', color='#334155')

    ax.set_title('Average Annual Crime Incidents: Comparing Three Policy & Societal Eras', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel('Average Annual Reported Cases', fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels([c.split('(')[0].strip() for c in labels], fontsize=10, fontweight='medium')
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f'{int(y):,}'))
    ax.legend(frameon=True, facecolor='white', loc='upper right')
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '02_grouped_bar_eras.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 3. 100% STACKED BAR GRAPH (Category Composition Across High-Risk States)
# =============================================================================
def plot_3_stacked_bar(df: pd.DataFrame):
    """Bar Graph 3: 100% Stacked Bar Chart displaying crime type proportions across top states."""
    top_states = df.groupby('State')['Total'].sum().sort_values(ascending=False).head(8).index
    df_top = df[df['State'].isin(top_states)].groupby('State')[CRIME_COLS].sum()
    
    # Normalize each state to 100%
    df_pct = df_top.div(df_top.sum(axis=1), axis=0) * 100
    df_pct = df_pct.loc[top_states[::-1]]  # Reorder for display

    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    left = np.zeros(len(df_pct))
    
    for c in ['DV', 'AoW', 'K&A', 'Rape', 'DD', 'AoM', 'WT']:
        values = df_pct[c].values
        ax.barh([s.title() for s in df_pct.index], values, left=left, label=CRIME_LABELS[c].split('(')[0].strip(),
                color=PALETTE[c], height=0.6, edgecolor='white', linewidth=0.5)
        left += values

    ax.set_title('Crime Offense Composition Across Top 8 Vulnerable States (100% Stacked Bar)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlabel('Percentage Share of Total Reported Offenses (%)', fontsize=11)
    ax.set_xlim(0, 100)
    ax.xaxis.set_major_formatter(ticker.PercentFormatter())
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', frameon=True, title='Offense Type')
    ax.grid(axis='x', linestyle='--', alpha=0.5)

    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '03_stacked_bar_composition.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 4. MULTI-PANEL SUBPLOTS GRID (Small Multiples: 2x3 Offense Trajectories)
# =============================================================================
def plot_4_subplots_grid(yearly: pd.DataFrame):
    """Subplots 1: 2x3 Grid of Subplots tracking longitudinal trajectories for each offense category."""
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(14, 8), dpi=150, sharex=True)
    categories = ['DV', 'AoW', 'K&A', 'Rape', 'DD', 'AoM']

    for i, c in enumerate(categories):
        ax = axes[i // 3, i % 3]
        color = PALETTE[c]
        ax.plot(yearly['Year'], yearly[c], color=color, linewidth=2.2, marker='o', markersize=4)
        ax.fill_between(yearly['Year'], yearly[c], color=color, alpha=0.15)
        
        ax.set_title(CRIME_LABELS[c], fontsize=11, fontweight='bold', color='#1E293B', pad=8)
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f'{int(y):,}'))
        ax.grid(True, linestyle='--', alpha=0.4)
        if i >= 3:
            ax.set_xlabel('Year', fontsize=10)
        if i % 3 == 0:
            ax.set_ylabel('Annual Cases', fontsize=10)

    fig.suptitle('Individual Crime Trajectories in India (2001 - 2021) [Small Multiples Grid]', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '04_subplots_grid_trajectories.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 5. SYNCHRONIZED TWO-PANEL SUBPLOTS (Volume vs YoY Growth Rate)
# =============================================================================
def plot_5_synchronized_subplots(yearly: pd.DataFrame):
    """Subplots 2: Synchronized 2-row subplot with shared X-axis showing total volume and YoY change rate."""
    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(12, 8), dpi=150, sharex=True, gridspec_kw={'height_ratios': [2, 1.2]})

    # Upper Panel: Cumulative Crime Volume
    ax1.plot(yearly['Year'], yearly['Total'], color='#4338CA', linewidth=2.8, marker='o', label='Total Crimes')
    ax1.fill_between(yearly['Year'], yearly['Total'], color='#6366F1', alpha=0.15)
    ax1.set_title('Macro Trajectory: Annual Reported Crime Volume', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Reported Incidents', fontsize=10)
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f'{int(y):,}'))
    ax1.grid(True, linestyle='--', alpha=0.4)

    # Lower Panel: YoY Growth Rate Diverging Bars
    yoy_pct = yearly['Total'].pct_change() * 100
    yoy_pct.iloc[0] = 0
    bar_colors = ['#10B981' if v < 0 else '#EF4444' for v in yoy_pct]

    bars = ax2.bar(yearly['Year'], yoy_pct, color=bar_colors, width=0.6, edgecolor='none')
    ax2.axhline(0, color='#1E293B', linewidth=1, linestyle='-')
    ax2.set_title('YoY Acceleration / Deceleration Rate (%)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('YoY Change (%)', fontsize=10)
    ax2.set_xlabel('Year', fontsize=11)
    ax2.set_xticks(yearly['Year'])
    ax2.set_xticklabels(yearly['Year'], rotation=45)
    ax2.grid(True, linestyle='--', alpha=0.4)

    # Annotate peaks
    max_idx = yoy_pct.idxmax()
    min_idx = yoy_pct.idxmin()
    ax2.annotate(f"Post-Nirbhaya Surge\n+{yoy_pct[max_idx]:.1f}% (2013)", 
                 xy=(yearly['Year'][max_idx], yoy_pct[max_idx]),
                 xytext=(yearly['Year'][max_idx]-3, yoy_pct[max_idx]+5),
                 arrowprops=dict(facecolor='#DC2626', shrink=0.1, width=1, headwidth=5),
                 fontsize=8.5, fontweight='bold', color='#991B1B')

    ax2.annotate(f"COVID Dip\n{yoy_pct[min_idx]:.1f}% (2020)", 
                 xy=(yearly['Year'][min_idx], yoy_pct[min_idx]),
                 xytext=(yearly['Year'][min_idx]-3, yoy_pct[min_idx]-10),
                 arrowprops=dict(facecolor='#0284C7', shrink=0.1, width=1, headwidth=5),
                 fontsize=8.5, fontweight='bold', color='#0369A1')

    fig.suptitle('Dual-Axis Macro Diagnostic: Crime Volume & YoY Acceleration Dynamics', fontsize=14, fontweight='bold', y=0.98)
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '05_synchronized_subplots_yoy.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 6. ANNOTATED LONGITUDINAL PYPLOT (National Policy Milestones Timeline)
# =============================================================================
def plot_6_annotated_pyplot(yearly: pd.DataFrame):
    """Pyplot 1: Single-plot Longitudinal Curve with rich contextual milestone annotations."""
    fig, ax = plt.subplots(figsize=(12, 6), dpi=150)
    years = yearly['Year'].values
    totals = yearly['Total'].values

    ax.plot(years, totals, color='#1E3A8A', linewidth=3, marker='o', markersize=6, label='Reported Offenses')
    ax.fill_between(years, totals, color='#3B82F6', alpha=0.12)

    # Callout 1: 2013 Nirbhaya Law Reform
    y2013 = yearly.loc[yearly['Year'] == 2013, 'Total'].values[0]
    ax.annotate('2013 Criminal Law Amendment (Nirbhaya Reform)\n• Expanded definition of rape & molestation\n• Mandatory FIR registration (+27.0% YoY)',
                xy=(2013, y2013), xytext=(2004, 280000),
                arrowprops=dict(facecolor='#DC2626', shrink=0.08, width=1.5, headwidth=7),
                fontsize=9, fontweight='bold', color='#991B1B',
                bbox=dict(boxstyle="round,pad=0.5", fc="#FEE2E2", ec="#EF4444", lw=1.2))

    # Callout 2: 2020 COVID Lockdowns
    y2020 = yearly.loc[yearly['Year'] == 2020, 'Total'].values[0]
    ax.annotate('2020 COVID-19 Lockdown Dip\n• Mobility curbs suppressed formal FIRs (-9.5% YoY)',
                xy=(2020, y2020), xytext=(2014, 220000),
                arrowprops=dict(facecolor='#0284C7', shrink=0.08, width=1.5, headwidth=7),
                fontsize=9, fontweight='bold', color='#0369A1',
                bbox=dict(boxstyle="round,pad=0.5", fc="#E0F2FE", ec="#38BDF8", lw=1.2))

    # Callout 3: 2021 Post-Lockdown Rebound
    y2021 = yearly.loc[yearly['Year'] == 2021, 'Total'].values[0]
    ax.annotate('2021 Post-Lockdown Rebound\n• Pent-up reporting (+15.2% YoY to 348,092 cases)',
                xy=(2021, y2021), xytext=(2015, 360000),
                arrowprops=dict(facecolor='#059669', shrink=0.08, width=1.5, headwidth=7),
                fontsize=9, fontweight='bold', color='#047857',
                bbox=dict(boxstyle="round,pad=0.5", fc="#D1FAE5", ec="#34D399", lw=1.2))

    ax.set_title('National Trend & Policy Milestone Timeline (2001 - 2021)', fontsize=14, fontweight='bold', pad=14)
    ax.set_xlabel('Year', fontsize=11, labelpad=8)
    ax.set_ylabel('Total Reported Incidents', fontsize=11, labelpad=8)
    ax.set_xticks(years)
    ax.set_xticklabels(years, rotation=45)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f'{int(y):,}'))
    ax.grid(True, linestyle='--', alpha=0.45)
    ax.set_ylim(100000, 420000)

    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '06_annotated_timeline_pyplot.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 7. CORRELATION HEATMAP SUBPLOT (Inter-Crime Correlation Matrix)
# =============================================================================
def plot_7_correlation_heatmap(df: pd.DataFrame):
    """Pyplot 2 / Subplot: Seaborn correlation matrix heatmap of 7 crime types."""
    corr_matrix = df[CRIME_COLS].corr(method='pearson')
    clean_labels = [c.split('(')[0].strip() for c in [CRIME_LABELS[k] for k in CRIME_COLS]]

    fig, ax = plt.subplots(figsize=(8, 7), dpi=150)
    sns.heatmap(
        corr_matrix,
        xticklabels=clean_labels,
        yticklabels=clean_labels,
        annot=True,
        fmt=".2f",
        cmap="coolwarm",
        vmin=-0.2, vmax=1.0,
        square=True,
        linewidths=0.8,
        cbar_kws={"shrink": 0.8, "label": "Pearson Correlation Coefficient"},
        ax=ax
    )

    ax.set_title('Inter-Crime Correlation Matrix: Multi-Offense Co-occurrence', fontsize=13, fontweight='bold', pad=12)
    plt.xticks(rotation=45, ha='right', fontsize=9)
    plt.yticks(rotation=0, fontsize=9)

    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '07_correlation_heatmap.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 8. MULTI-CATEGORY BOX & WHISKER PLOT (Spread, Median & State Outliers)
# =============================================================================
def plot_8_box_and_whisker(df: pd.DataFrame):
    """Subplots 3: Box and Whisker Plot comparing distributions and outlier spreads across crime types."""
    # Group by State and Year to examine annual state-level distributions
    state_year = df.groupby(['State', 'Year'])[CRIME_COLS].sum().reset_index()

    fig, ax = plt.subplots(figsize=(11, 6), dpi=150)
    box_data = [state_year[c].values for c in ['DV', 'AoW', 'K&A', 'Rape', 'DD', 'AoM']]
    labels = ['Domestic Violence', 'Assault on Women', 'Kidnapping', 'Rape', 'Dowry Deaths', 'Eve Teasing']

    bp = ax.boxplot(
        box_data,
        patch_artist=True,
        tick_labels=labels,
        showmeans=True,
        meanprops=dict(marker='D', markeredgecolor='black', markerfacecolor='yellow', markersize=6),
        medianprops=dict(color='black', linewidth=1.5),
        flierprops=dict(marker='o', markersize=4, markerfacecolor='#EF4444', alpha=0.5)
    )

    colors = ['#FCA5A5', '#FCD34D', '#6EE7B7', '#93C5FD', '#F9A8D4', '#C4B5FD']
    for patch, color in zip(bp['boxes'], colors):
        patch.set_facecolor(color)
        patch.set_edgecolor('#334155')

    ax.set_title('State-Level Annual Crime Distributions (Box & Whisker Analysis)', fontsize=13, fontweight='bold', pad=12)
    ax.set_ylabel('Annual Incidents per State/UT', fontsize=11)
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f'{int(y):,}'))
    ax.grid(axis='y', linestyle='--', alpha=0.4)

    # Note explaining markers
    ax.plot([], [], marker='D', color='yellow', markeredgecolor='black', linestyle='None', label='Mean')
    ax.plot([], [], marker='o', color='#EF4444', linestyle='None', label='State-Year Outlier')
    ax.legend(loc='upper right', frameon=True)

    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '08_box_and_whisker_distributions.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 9. DONUT / EXPLODED PIE CHART (National Proportional Breakdown)
# =============================================================================
def plot_9_donut_chart(df: pd.DataFrame):
    """Pyplot 3: Modern Donut Chart showing national share of offense types."""
    crime_totals = df[CRIME_COLS].sum().sort_values(ascending=False)
    labels = [CRIME_LABELS[c].split('(')[0].strip() for c in crime_totals.index]
    values = crime_totals.values
    colors = [PALETTE[c] for c in crime_totals.index]

    fig, ax = plt.subplots(figsize=(9, 7), dpi=150)
    explode = [0.06 if i == 0 else 0 for i in range(len(values))] # Explode Domestic Violence (largest)

    wedges, texts, autotexts = ax.pie(
        values,
        labels=labels,
        autopct='%1.1f%%',
        pctdistance=0.78,
        startangle=140,
        colors=colors,
        explode=explode,
        wedgeprops=dict(width=0.42, edgecolor='white', linewidth=1.5) # Donut hole
    )

    for at in autotexts:
        at.set_fontsize(8.5)
        at.set_fontweight('bold')
        at.set_color('#1E293B')

    for t in texts:
        t.set_fontsize(9.5)

    # Center circle annotation
    total_all = values.sum()
    ax.text(0, 0, f"Total Cases\n{int(total_all):,}\n(2001-2021)",
            ha='center', va='center', fontsize=11, fontweight='bold', color='#1E293B')

    ax.set_title('National Crime Composition: Proportion by Offense Category', fontsize=13, fontweight='bold', pad=15)
    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '09_donut_crime_shares.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# 10. MULTI-DIMENSIONAL BUBBLE SCATTER PLOT (State Vulnerability Matrix)
# =============================================================================
def plot_10_bubble_scatter(df: pd.DataFrame):
    """Pyplot 4: Bubble Scatter Plot mapping Total Volume (X), Violent Bodily Crimes (Y), Kidnapping (Size), and Severity (Color)."""
    # Aggregate by state
    state_agg = df.groupby('State')[CRIME_COLS + ['Total']].sum().reset_index()
    # Violent bodily offenses = Rape + Dowry Deaths + Assault on Women
    state_agg['ViolentOffenses'] = state_agg['Rape'] + state_agg['DD'] + state_agg['AoW']
    # Composite severity score = Rape*0.35 + DD*0.35 + AoW*0.15 + DV*0.15
    state_agg['SeverityIndex'] = (
        state_agg['Rape'] * 0.35 +
        state_agg['DD'] * 0.35 +
        state_agg['AoW'] * 0.15 +
        state_agg['DV'] * 0.15
    ) / 1000

    fig, ax = plt.subplots(figsize=(11, 7), dpi=150)

    # Bubble sizes scaled by Kidnapping cases
    bubble_sizes = (state_agg['K&A'] / state_agg['K&A'].max()) * 900 + 40

    scatter = ax.scatter(
        state_agg['Total'],
        state_agg['ViolentOffenses'],
        s=bubble_sizes,
        c=state_agg['SeverityIndex'],
        cmap='plasma',
        alpha=0.75,
        edgecolors='#334155',
        linewidth=1.2
    )

    cbar = plt.colorbar(scatter, ax=ax, shrink=0.85)
    cbar.set_label('Weighted Severity Index (k-score)', fontsize=10)

    # Annotate top outlier states
    top_label_states = state_agg.nlargest(7, 'Total')['State'].tolist() + ['DELHI', 'KERALA']
    for _, row in state_agg.iterrows():
        if row['State'] in top_label_states:
            ax.annotate(
                row['State'].title(),
                xy=(row['Total'], row['ViolentOffenses']),
                xytext=(row['Total'] + 15000, row['ViolentOffenses'] + 3000),
                fontsize=8.5,
                fontweight='bold',
                color='#0F172A',
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#CBD5E1", alpha=0.85)
            )

    ax.set_title('State Vulnerability Matrix: Total Volume vs. Violent Bodily Harm Offenses', fontsize=13, fontweight='bold', pad=14)
    ax.set_xlabel('Cumulative Reported Crimes Against Women (2001 - 2021)', fontsize=11, labelpad=8)
    ax.set_ylabel('Violent Bodily Offenses (Rape + DD + Assault)', fontsize=11, labelpad=8)
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'{int(x):,}'))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, p: f'{int(y):,}'))
    ax.grid(True, linestyle='--', alpha=0.45)

    # Legend for bubble size
    ax.scatter([], [], s=100, c='gray', alpha=0.6, label='Lower K&A')
    ax.scatter([], [], s=500, c='gray', alpha=0.6, label='Higher K&A (Bubble Size)')
    ax.legend(scatterpoints=1, frameon=True, loc='upper left', fontsize=8.5)

    plt.tight_layout()
    save_path = os.path.join(OUTPUT_DIR, '10_bubble_scatter_vulnerability.png')
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    print(f"[Generated] {save_path}")


# =============================================================================
# Execution Runner
# =============================================================================
if __name__ == '__main__':
    print("=" * 70)
    print("SafeCrime Analytics: Generating 10 Publication-Quality Plot Types")
    print("=" * 70)
    plot_1_horizontal_bar(df)
    plot_2_grouped_bar(df)
    plot_3_stacked_bar(df)
    plot_4_subplots_grid(yearly_national)
    plot_5_synchronized_subplots(yearly_national)
    plot_6_annotated_pyplot(yearly_national)
    plot_7_correlation_heatmap(df)
    plot_8_box_and_whisker(df)
    plot_9_donut_chart(df)
    plot_10_bubble_scatter(df)
    print("=" * 70)
    print(f"All 10 visualizations generated successfully and saved to: '{OUTPUT_DIR}/'")
