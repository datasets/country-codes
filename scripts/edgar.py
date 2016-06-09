#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib
import csv

from lxml import html

url = "https://www.sec.gov/edgar/searchedgar/edgarstatecodes.htm"

content = urllib.urlopen(url).read()
doc = html.fromstring(content)

rows = doc.xpath('//table')[3].getchildren()

seen_other_countries = False
header = ['EDGAR', 'name']

data = []

for row in rows:
    if seen_other_countries is not True:
        if row.text_content().replace('\n', '') != 'Other Countries':
            print('SKIPPING', row.text_content())
            continue
        else:
            seen_other_countries = True
            print('SEEN OTHER COUNTRIES', row.text_content())
            continue

    cells = row.getchildren()
    if len(cells) != 2:
        print('ERROR IN CELL COUNT')
        for cell in cells:
            print(cell)
            print(cell.text_content())
        continue
    code = cells[0].text_content().replace('\n', '')
    name = cells[1].text_content().replace('\n', '')
    data.append((code, name))

with open('data/edgar.csv', 'wb') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)
    for row in data:
        csv_writer.writerow(row)
