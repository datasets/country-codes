#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import urllib

import utils

# Retrive data directly from unicode-cldr project hosted at github
url = "https://raw.githubusercontent.com/unicode-cldr/cldr-localenames-full/master/main/en/territories.json"

content = json.loads(urllib.urlopen(url).read())

content_en = content['main']['en']['localeDisplayNames']['territories']

# Remove UN regional codes (three digits) and -alt-variants
territories = {k: v for k, v in content_en.items() if 
      (k.isdigit() is not True and '-alt-variant' not in k)}

map(lambda discard: territories.pop(discard, None), ['ZZ', 'EZ', 'EU'])

# sort as tuples so that XX-alt-short will come after XX
territories = sorted([(k, v) for k, v in territories.iteritems()])

cldr = {}
for territory in territories:
    name = territory[0]

    # use -alt-short if it exists
    if "-alt-short" in territory[0]:
        name = name.replace("-alt-short", "")
        cldr.pop(name, None)

    cldr.update({name: territory[1]})



header = ['ISO3166-1-Alpha-2', 'CLDR display name']
with open('data/cldr.csv', 'wb') as csv_file:
    csv_writer = utils.UnicodeWriter(csv_file)
    csv_writer.writerow(header)
    for row in [(k, v) for k, v in cldr.iteritems()]:
        csv_writer.writerow(row)
