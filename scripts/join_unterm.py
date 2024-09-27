#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
from fuzzywuzzy import process


with open('data/country-codes.json', 'r', encoding='utf-8') as f:
    country_info = json.load(f)


headers = ['UNTERM English Short',
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


keyed = {country.get('official_name_en', country['ISO3166-1-Alpha-3']): country for country in country_info}


with open('data/unterm_names.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header
    for row in reader:
        name = row[0]
        matches = process.extract(name, keyed.keys(), limit=5)
        if matches[0][1] == 100:
            keyed[matches[0][0]].update(dict(zip(headers, row)))
        else:
            if '(the)' in name:
                no_the = process.extract(name.replace('(the)', ''), keyed.keys(), limit=5)
                if no_the[0][1] == 100:
                    keyed[no_the[0][0]].update(dict(zip(headers, row)))
                else:
                    if name == "Czech Republic (the)":
                        keyed["Czechia"].update(dict(zip(headers, row)))
                    else:
                        print(f"NOT FOUND: {name}")
                        print(matches)


def itemgetter(*items):
    if len(items) == 1:
        item = items[0]
        return lambda obj: obj.get(item, '')
    else:
        return lambda obj: tuple(obj.get(item, '') for item in items)


keyed = sorted(keyed.values(), key=itemgetter('official_name_en'))

# Format certain numeric fields (M49 and ISO3166-1-numeric) with leading zeros
for country in keyed:
    for k, v in country.items():
        if k in ['M49', 'ISO3166-1-numeric']:
            if v not in [None, 'null', '']:
                country[k] = str(int(v)).zfill(3)


output_filename = "data/country-codes-joined.json"
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(keyed, f, ensure_ascii=False, indent=2)
