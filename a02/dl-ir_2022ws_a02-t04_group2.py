import sys

if len(sys.argv) < 2:
    fn = 'u02-hirschindex-example.txt'
    print(f'Using default input file name "{fn}".')
elif len(sys.argv) == 2:
    print(f'Using input file name "{fn}".')
    fn = 'u02-hirschindex-example.txt'
else:
    print('Usage: python dl-ir_2022ws_a02-t04_group2.py [filename]')
    sys.exit(-1)
    
with open(fn) as f:
    text = f.read()

lines = text.split('\n')
rows = [(line.split('\t')[0], int(line.split('\t')[1])) for line in lines]

rows.sort(key=lambda x: x[1], reverse=True)

for i, row in enumerate(rows):
    if row[1] < i:
        h_factor = i
        break

print(f'Hirsch factor: {h_factor}')