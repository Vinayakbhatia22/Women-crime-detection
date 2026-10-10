import csv

with open('crime_data.csv', 'r') as f:
    rows = list(csv.DictReader(f))

def get_year_data(year):
    return [r for r in rows if r['Year'] == str(year)]

d19 = get_year_data(2019)
d20 = get_year_data(2020)
d21 = get_year_data(2021)

print(f"{'Idx':<3} | {'State':<20} | {'2019 Rape':<10} | {'2020 Rape':<10} | {'2021 Rape':<10}")
print("-" * 65)
for i in range(len(d19)):
    st = d19[i]['State']
    r19 = d19[i]['Rape']
    r20 = d20[i]['Rape']
    r21 = d21[i]['Rape']
    print(f"{i:<3} | {st:<20} | {r19:<10} | {r20:<10} | {r21:<10}")
