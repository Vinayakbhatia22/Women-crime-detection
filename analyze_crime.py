import csv
import json
from collections import defaultdict

def run_analysis():
    filepath = 'crime_data.csv'
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)

    crime_cols = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
    
    # Clean state names
    for r in rows:
        r['Year'] = int(r['Year'])
        state = r['State'].strip().upper()
        # Normalize state names
        state = state.replace('&', 'AND').replace('  ', ' ')
        state = state.replace('D&N HAVELI', 'D AND N HAVELI').replace('D AND N HAVELI', 'DADRA AND NAGAR HAVELI')
        state = state.replace('DAMAN AND DIU', 'DAMAN AND DIU')
        state = state.replace('A AND N ISLANDS', 'ANDAMAN AND NICOBAR')
        state = state.replace('DELHI UT', 'DELHI')
        state = state.replace('KERALAL', 'KERALA')
        r['CleanState'] = state
        for c in crime_cols:
            r[c] = float(r[c])
        r['TotalCrime'] = sum(r[c] for c in crime_cols)

    # 1. Year-wise National Totals
    yearly_totals = defaultdict(lambda: defaultdict(float))
    for r in rows:
        y = r['Year']
        for c in crime_cols:
            yearly_totals[y][c] += r[c]
        yearly_totals[y]['TotalCrime'] += r['TotalCrime']

    years = sorted(yearly_totals.keys())

    print("=== YEAR-WISE NATIONAL CRIME TOTALS ===")
    print(f"{'Year':<6} | {'Total Crime':<12} | {'YoY Change':<12} | {'YoY %':<8} | {'Rape':<8} | {'K&A':<8} | {'DD':<6} | {'AoW':<8} | {'AoM':<6} | {'DV':<8} | {'WT':<6}")
    print("-" * 105)
    
    prev_total = None
    yoy_changes = {}
    for y in years:
        tot = yearly_totals[y]['TotalCrime']
        if prev_total is not None:
            diff = tot - prev_total
            pct = (diff / prev_total) * 100
            yoy_changes[y] = (diff, pct)
            diff_str = f"{diff:+,.0f}"
            pct_str = f"{pct:+.2f}%"
        else:
            diff_str = "N/A"
            pct_str = "N/A"
        prev_total = tot
        print(f"{y:<6} | {tot:<12,.0f} | {diff_str:<12} | {pct_str:<8} | {yearly_totals[y]['Rape']:<8,.0f} | {yearly_totals[y]['K&A']:<8,.0f} | {yearly_totals[y]['DD']:<6,.0f} | {yearly_totals[y]['AoW']:<8,.0f} | {yearly_totals[y]['AoM']:<6,.0f} | {yearly_totals[y]['DV']:<8,.0f} | {yearly_totals[y]['WT']:<6,.0f}")

    # Largest Increase and Largest Decrease Years
    sorted_increases = sorted(yoy_changes.items(), key=lambda x: x[1][0], reverse=True)
    print("\n=== YEAR OF LARGEST CRIME INCREASE ===")
    for y, (d, p) in sorted_increases[:3]:
        print(f"Year {y}: +{d:,.0f} cases ({p:+.2f}%)")

    print("\n=== YEARS OF CRIME DECREASE ===")
    decreasing_years = [item for item in sorted_increases if item[1][0] < 0]
    for y, (d, p) in sorted(decreasing_years, key=lambda x: x[1][0]):
        print(f"Year {y}: {d:,.0f} cases ({p:+.2f}%)")

    # 2. Crime Type Trends (2001 to 2019 and 2001 to 2021)
    print("\n=== CRIME GROWTH FROM 2001 TO 2019 (Pre-Pandemic / Clean Align) ===")
    for c in crime_cols:
        v2001 = yearly_totals[2001][c]
        v2019 = yearly_totals[2019][c]
        growth = ((v2019 - v2001) / v2001) * 100 if v2001 > 0 else 0
        abs_diff = v2019 - v2001
        print(f"{c:<5}: 2001={v2001:>8,.0f} -> 2019={v2019:>8,.0f} | Abs Growth={abs_diff:>+8,.0f} | % Growth={growth:>+8.2f}%")

    print("\n=== CRIME GROWTH FROM 2001 TO 2021 ===")
    for c in crime_cols:
        v2001 = yearly_totals[2001][c]
        v2021 = yearly_totals[2021][c]
        growth = ((v2021 - v2001) / v2001) * 100 if v2001 > 0 else 0
        abs_diff = v2021 - v2001
        print(f"{c:<5}: 2001={v2001:>8,.0f} -> 2021={v2021:>8,.0f} | Abs Growth={abs_diff:>+8,.0f} | % Growth={growth:>+8.2f}%")

    # 3. State-wise Total Analysis (2001-2021)
    state_totals = defaultdict(lambda: defaultdict(float))
    for r in rows:
        st = r['CleanState']
        for c in crime_cols:
            state_totals[st][c] += r[c]
        state_totals[st]['TotalCrime'] += r['TotalCrime']

    sorted_states = sorted(state_totals.items(), key=lambda x: x[1]['TotalCrime'], reverse=True)
    grand_total = sum(v['TotalCrime'] for v in state_totals.values())

    print("\n=== TOP 10 CRIME HOTSPOTS (STATE-WISE TOTAL 2001-2021) ===")
    print(f"{'Rank':<4} | {'State':<25} | {'Total Crime':<12} | {'National Share':<14} | {'Top Crime Category'}")
    print("-" * 80)
    for idx, (st, data) in enumerate(sorted_states[:15], 1):
        share = (data['TotalCrime'] / grand_total) * 100
        # Find dominant crime category
        dom = max(crime_cols, key=lambda c: data[c])
        print(f"{idx:<4} | {st:<25} | {data['TotalCrime']:<12,.0f} | {share:>6.2f}%       | {dom} ({data[dom]:,.0f})")

    # 4. Crime-Specific Hotspots
    print("\n=== TOP 3 HOTSPOTS PER CRIME CATEGORY (Cumulative 2001-2021) ===")
    for c in crime_cols:
        sorted_by_c = sorted(state_totals.items(), key=lambda x: x[1][c], reverse=True)
        top3_str = ", ".join([f"{st} ({data[c]:,.0f})" for st, data in sorted_by_c[:3]])
        print(f"{c:<5}: {top3_str}")

    # 5. Sudden Spikes / Anomalies in Crimes
    print("\n=== LARGEST YEAR-OVER-YEAR CRIME SPIKES (NATIONAL) ===")
    for c in crime_cols:
        max_spike_y = None
        max_spike_diff = -1e9
        max_spike_pct = 0
        for i in range(1, len(years)):
            y_prev = years[i-1]
            y_curr = years[i]
            # Avoid 2011 to 2012 for AoW due to 2011 missing data
            if c == 'AoW' and y_prev == 2011:
                continue
            v_prev = yearly_totals[y_prev][c]
            v_curr = yearly_totals[y_curr][c]
            diff = v_curr - v_prev
            if diff > max_spike_diff:
                max_spike_diff = diff
                max_spike_y = y_curr
                max_spike_pct = (diff / v_prev * 100) if v_prev > 0 else 0
        print(f"{c:<5}: Biggest surge in {max_spike_y} (+{max_spike_diff:,.0f} cases, {max_spike_pct:+.1f}%)")

if __name__ == '__main__':
    run_analysis()
