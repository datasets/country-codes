#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs

from fuzzywuzzy import process

import utils

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

country_info = json.load(open('data/country-codes.json'))

keyed = {}
for country in country_info:
    keyed.update({country.get('official_name_en', country['ISO3166-1-Alpha-3']): country})

with open('data/unterm_names.csv', 'rb') as csvfile:
    reader = utils.UnicodeReader(csvfile)
    # ignore header
    reader.next()
    for row in reader:
        name = row[0]
        matches = process.extract(name, keyed.keys(), limit=5)
        if matches[0][1] == 100:
            keyed[matches[0][0]].update(dict(zip(headers, row)))
        else:
            if '(the)' in name:
                no_the = process.extract(name.replace('(the)', ''),
                                         keyed.keys(),
                                         limit=5)
                if no_the[0][1] == 100:
                    keyed[no_the[0][0]].update(dict(zip(headers, row)))
                else:
                    # looks like UNTERM has not been updated for Czechia
                    if name == "Czech Republic (the)":
                        keyed["Czechia"].update(dict(zip(headers, row)))
                    else:
                        print "NOT FOUND:"
                        print name
                        print matches

def itemgetter(*items):
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return obj.get(item, '')
    else:
        def g(obj):
            return tuple(obj.get(item, '') for item in items)
    return g


keyed = sorted(keyed.values(), key=itemgetter('official_name_en'))
output_filename = "data/country-codes-joined.json"

for country in keyed:
    for k, v in country.items():
        if k in ['M49', 'ISO3166-1-numeric']:
            if v not in [None, 'null', '']:
                country[k] = str(int(v)).zfill(3)

f = open(output_filename, mode='w')
stream = codecs.getwriter('utf8')(f)
json.dump(keyed, stream, ensure_ascii=False, indent=2, encoding='utf-8')
