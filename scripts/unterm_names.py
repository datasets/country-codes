#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib

from openpyxl import load_workbook

import utils

url = "https://protocol.un.org/dgacm/pls/site.nsf/files/Country%20Names%20UNTERM2/$FILE/UNTERM%20EFSRCA.xlsx"

opener = urllib.URLopener()
opener.retrieve(url, "UNTERM EFSRCA.xlsx")

wb = load_workbook("UNTERM EFSRCA.xlsx")

sheet1 = wb['Sheet1']

header = ['official_name_en',
          'UNTERM French Short',
          'UNTERM Spanish Short',
          'UNTERM Russian Short',
          'UNTERM Chinese Short',
          'UNTERM Arabic Short',
          'UNTERM English Formal',
          'UNTERM French Formal',
          'UNTERM Spanish Formal',
          'UNTERM Russian Formal',
          'UNTERM Chinese Formal',
          'UNTERM Arabic Formal']

with open('data/unterm_names.csv', 'wb') as csv_file:
    csv_writer = utils.UnicodeWriter(csv_file)
    csv_writer.writerow(header)
    for row in sheet1.iter_rows(row_offset=1, max_col=12, max_row=200):
	values = [cell.value for cell in row]
	if all(values):
            csv_writer.writerow(values)

