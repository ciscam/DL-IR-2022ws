import matplotlib.pyplot as plt
import re

with open('titles.txt') as f:
    text = f.read()

text_rows = text.split('\n')
data_rows = [[field for field in row.split('\t')] for row in text_rows if '\t' in row]

# order dataset
rows_by_n_colons_by_year = {}
for i, row in enumerate(data_rows):
    # get dict per year
    rows_by_n_colons_by_year[int(row[1])] = rows_by_n_colons_by_year.get(int(row[1]), {})
    rows_by_n_colons = rows_by_n_colons_by_year[int(row[1])]
    
    # get list per n_colons
    n_colons = row[2].count(':')
    # catch multiple colon like '::'
    if len(re.findall(r':+', row[2])) != n_colons:
        print(i, row)
    # line 21654 is affected: ['article', '2016', 'R-Syst::diatom: an open-access and curated barcode database for diatoms and freshwater monitoring.']
    rows_by_n_colons[n_colons] = rows_by_n_colons.get(n_colons, [])
    rows_by_n_colons[n_colons].append((i, row))

# explore n_colons
cd={}
for n_colons in rows_by_n_colons_by_year.values():
    for n, rows in n_colons.items():
        cd[n] = cd.get(n, 0)
        cd[n] += len(rows)

# {0: 246444, 1: 54971, 2: 1194, 3: 112, 4: 19, 5: 5, 6: 1}


# so three bars: 0-, 1-, and >1-bar
# maybe highlight the 6-colon-row somewhere?

# years ascending as x-values
x = list(rows_by_n_colons_by_year)
x.sort()

# get the y values for the years
y = [[], [], []]
for year in x:
    for y_sub in y:
        y_sub.append(0)
    for n_colons, rows in rows_by_n_colons_by_year[year].items():
        if n_colons == 0:
            y[0][-1] += len(rows)
        elif n_colons == 1:
            y[1][-1] += len(rows)
        elif n_colons > 1:
            y[2][-1] += len(rows)
        else:
            raise(Exception('of epic proportions'))

plt.bar(x, y[0])
plt.bar(x, y[1], bottom=y[0])
plt.bar(x, y[2], bottom=y[0]+y[1])

plt.show()


# a relative plot would make sense
y = [[], []]
for year in x:
    without_colon = 0
    with_colon = 0
    for n_colons, rows in rows_by_n_colons_by_year[year].items():
        if n_colons == 0:
            without_colon += len(rows)
        elif n_colons >= 1:
            with_colon += len(rows)
        else:
            raise(Exception('of epic proportions'))
    total = without_colon + with_colon
    y[0].append(without_colon / total)
    y[1].append(with_colon / total)

plt.bar(x, y[0])
plt.bar(x, y[1], bottom=y[0])

plt.show()