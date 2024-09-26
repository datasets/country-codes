#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import operator


get_column_number = operator.itemgetter(0)
get_column_name = operator.itemgetter(1)

columns = []
with open('data/columns.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:
        cells = row[0].split(': ')
        columns.append((int(cells[0]), cells[1].strip()))


official = [columns.pop(columns.index(c)) for c in columns if c[1].startswith('official')]


iso_columns = [columns.pop(columns.index(c)) for c in columns if c[1].startswith('ISO')]
iso_columns.append(columns.pop([c[1] for c in columns].index('M49')))


unterm = [columns.pop(columns.index(c)) for c in columns if c[1].startswith('UNTERM')]

# Sort chunks of columns
ordered = sorted(official, key=get_column_name) + \
          sorted(iso_columns, key=get_column_name) + \
          sorted(unterm, key=get_column_name) + \
          sorted(columns, key=get_column_name)

# Write the reordered CSV
with open('data/country-codes.csv', 'r', encoding='utf-8') as infile, \
     open('data/country-codes-reordered.csv', 'w', newline='', encoding='utf-8') as outfile:
    
    fieldnames = [get_column_name(c) for c in ordered]
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
    writer.writeheader()
    
    for row in csv.DictReader(infile):
        writer.writerow(row)
