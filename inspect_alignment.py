import csv

with open('crime_data.csv', 'r') as f:
    rows = list(csv.DictReader(f))

# Look at states in 2019, 2020, 2021
s2019 = [r['State'] for r in rows if r['Year'] == '2019']
s2020 = [r['State'] for r in rows if r['Year'] == '2020']
s2021 = [r['State'] for r in rows if r['Year'] == '2021']

print("Count 2019:", len(s2019))
print("Count 2020:", len(s2020))
print("Count 2021:", len(s2021))

# Compare state lists
for i in range(min(len(s2019), len(s2020))):
    print(f"{i:2d}: 2019={s2019[i]:<20} | 2020={s2020[i]:<20} | 2021={s2021[i]:<20}")
