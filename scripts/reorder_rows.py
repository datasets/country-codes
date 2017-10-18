#!/usr/bin/env python
# -*- coding: utf-8 -*-

import icu

import utils

collator = icu.Collator.createInstance(icu.Locale('{lc}.UTF-8'.format(lc='en_US')))

headers = None
rows = []
with open('data/country-codes-reordered.csv', 'rb') as f:
    reader = utils.UnicodeReader(f)
    headers = reader.next()
    for row in reader:
        rows.append(row)

sorted(rows, key=lambda row: row[headers.index('official_name_en')], cmp=collator.compare)

with open('data/country-codes-reordered-sorted.csv', 'wb') as f:
    csv_writer = utils.UnicodeWriter(f)
    csv_writer.writerow(headers)
    for row in rows:
        csv_writer.writerow(row)
