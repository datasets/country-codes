#!/usr/bin/env python
# -*- coding: utf-8 -*-

import operator

import utils

get_column_number = operator.itemgetter(0)
get_column_name = operator.itemgetter(1)

columns = []
with open('data/columns.csv', 'rb') as f:
    reader = utils.UnicodeReader(f)
    for row in reader:
        cells = row[0].split(': ')
        columns.append((int(cells[0]), cells[1].strip()))

official = map(lambda c: columns.pop(columns.index(c)), [c for c in columns
                  if c[1].startswith('official')])

iso_columns = map(lambda c: columns.pop(columns.index(c)), [c for c in columns
                  if c[1].startswith('ISO')])
iso_columns.append(columns.pop(
                   map(get_column_name, columns).index('M49')))

unterm = map(lambda c: columns.pop(columns.index(c)), [c for c in columns
                  if c[1].startswith('UNTERM')])

# sort chunks of columns
ordered = sorted(official, key=get_column_name) + \
          sorted(iso_columns, key=get_column_name) + \
          sorted(unterm, key=get_column_name) + \
          sorted(columns, key=get_column_name)

# join column numbers with commas for use as argument to csvcut
ordered_column_numbers = ','.join(map(str, map(get_column_number, ordered)))

with open('data/column-order.txt', 'w') as f:
    f.write(ordered_column_numbers + "\n")
