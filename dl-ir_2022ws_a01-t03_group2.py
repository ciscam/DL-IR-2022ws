import re

with open('titles.txt') as f:
    text = f.read()

text_rows = text.split('\n')
rows = [[field for field in row.split('\t') if len(row.split('\t')) == 3] for row in text_rows]

colon_separated_titles_by_year = {}
for i, row in enumerate(rows):
    # get dict per year
    colon_separated_titles_by_year[int(row[1])] = colon_separated_titles_by_year.get(int(row[1]), {})
    row_by_n_colons = colon_separated_titles_by_year[int(row[1])]
    
    # get list per n_colons
    n_colons = row[2].count(':')
    # catch multiple colon like '::'
    if len(re.findall(r':+', row[2])) != n_colons:
        print(i, row)
    row_by_n_colons[n_colons] = row_by_n_colons.get(n_colons, [])
    row_by_n_colons[n_colons].append((i, row))
