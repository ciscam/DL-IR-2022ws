import matplotlib.pyplot as plt
import numpy as np
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
plt.bar(x, y[2], bottom=np.array(y[0])+np.array(y[1]))

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


# exercise part b) chart of wordcount in first part
rows_by_wordcount_before_first_colon = {}
for i, row in enumerate(data_rows):
    title = row[2]
    # match any title with a colon after word characters followed by another word character
    # if re.match(r'.*\w.*:.*\w', title):
    # had to make it anything BUT colon because row 191969 ['article', '2012', ': onastre: OER Development and Promotion. Outcomes of an International Research Projecton the OpenCourseWare Model.']
    if re.match(r'[^:]*\w[^:]*:.*\w', title):
        text_before_first_colon = title.split(':')[0]
        words_before_first_colon = re.findall(r'\w+', text_before_first_colon)
        wordcount = len(words_before_first_colon)
        rows_by_wordcount_before_first_colon[wordcount] = rows_by_wordcount_before_first_colon.get(wordcount, [])
        rows_by_wordcount_before_first_colon[wordcount].append((i, row))

# row 25714 striked out as 72 words before first colon ['article', '2017', "Maryanthe Malliaris and Saharon Shelah, Cofinality spectrum problems in model theory, set theory and general topology . Journal of the American Mathematical Society, vol. 29 (2016), pp. 237-297. - Maryanthe Malliaris and Saharon Shelah, Existence of optimal ultrafilters and the fundamental complexity of simple theories. Advances in Mathematics, vol. 290 (2016), pp. 614-681. - Maryanthe Malliaris and Saharon Shelah, Keisler's order has infinitely many classes. Israel Journal of Mathematics, to appear, https://math.uchicago.edu/∼mem/."]
# URLs or generally a colon that's not part of a sentence structure should be filtered
# a fine finding for exercise part c. Let's ignore that for now

# get x-values
x = range(min(rows_by_wordcount_before_first_colon), max(rows_by_wordcount_before_first_colon) + 1)

# get y-values
y = []
for col in x:
    if col in rows_by_wordcount_before_first_colon:
        y.append(len(rows_by_wordcount_before_first_colon[col]))
    else:
        y.append(0)

plt.bar(x, y)

plt.show()