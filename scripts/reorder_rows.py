#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import locale
import functools

# Set the locale to US English with UTF-8 encoding
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

def collator(value):
    return locale.strxfrm(value)

# Read the CSV file
headers = None
rows = []
with open('data/country-codes-reordered.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        rows.append(row)

# Use locale.strxfrm as the key function to handle locale-aware sorting
sorted_rows = sorted(rows, key=lambda row: collator(row[headers.index('official_name_en')]))

# Write the sorted rows to a new CSV file
with open('data/country-codes-reordered-sorted.csv', 'w', newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)  # Write the headers first
    csv_writer.writerows(sorted_rows)  # Write the sorted rows
