import csv
import json
from collections import defaultdict

with open('crime_data.csv', 'r', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

crime_cols = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']
crime_labels = {
    'Rape': 'Rape (Sec. 376)',
    'K&A': 'Kidnapping & Abduction',
    'DD': 'Dowry Deaths (Sec. 304B)',
    'AoW': 'Assault on Women / Molestation (Sec. 354)',
    'AoM': 'Insult to Modesty / Eve Teasing (Sec. 509)',
    'DV': 'Domestic Violence (Sec. 498A)',
    'WT': 'Women Trafficking'
}

clean_records = []
for r in rows:
    y = int(r['Year'])
    st = r['State'].strip()
    # Normalize state casing
    st_title = st.title().replace('&', 'and').replace('  ', ' ')
    if 'A & N' in st or 'A And N' in st_title:
        st_title = 'Andaman & Nicobar'
    elif 'D & N' in st or 'D&N' in st:
        st_title = 'Dadra & Nagar Haveli'
    elif 'Daman' in st:
        st_title = 'Daman & Diu'
    elif 'Delhi' in st:
        st_title = 'Delhi'
    elif 'Keralal' in st_title:
        st_title = 'Kerala'
    
    rec = {
        'state': st_title,
        'year': y,
        'Rape': int(float(r['Rape'])),
        'K&A': int(float(r['K&A'])),
        'DD': int(float(r['DD'])),
        'AoW': int(float(r['AoW'])),
        'AoM': int(float(r['AoM'])),
        'DV': int(float(r['DV'])),
        'WT': int(float(r['WT'])),
    }
    rec['total'] = sum(rec[c] for c in crime_cols)
    clean_records.append(rec)

# Write to data.js
js_content = f"// Generated Crime Data for Analytics Dashboard\nwindow.CRIME_DATA = {json.dumps(clean_records, indent=2)};\nwindow.CRIME_COLS = {json.dumps(crime_cols)};\nwindow.CRIME_LABELS = {json.dumps(crime_labels)};\n"

with open('data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("data.js written successfully with", len(clean_records), "records.")
