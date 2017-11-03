#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs

countries = json.load(open('data/iso3166-flat.json'))

keyed = {}
for country in countries:
    # cast floats to string
    fixed = {k: str(int(v)) for k, v in country.items() 
             if k in ["Sub-region Code", "M49", "Region Code", "Intermediate Region Code"]
             and v not in [None, '', ' ']}
    country.update(fixed)
    keyed.update({country['ISO3166-1-Alpha-3']: country})

output_filename = "data/iso3166.json"
f = open(output_filename, mode='w')
stream = codecs.getwriter('utf8')(f)
json.dump(keyed, stream, ensure_ascii=False, indent=2, encoding='utf-8')
