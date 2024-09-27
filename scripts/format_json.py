#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

# Load the countries data from the JSON file
with open('data/iso3166-flat.json', 'r', encoding='utf-8') as f:
    countries = json.load(f)

keyed = {}
for country in countries:
    # Cast floats to strings for specific fields
    fixed = {k: str(int(float(v))) for k, v in country.items() 
             if k in ["Sub-region Code", "M49", "Region Code", "Intermediate Region Code"]
             and v not in [None, '', ' ']}
    country.update(fixed)
    keyed[country['ISO3166-1-Alpha-3']] = country

# Write the updated JSON to a file
output_filename = "data/iso3166.json"
with open(output_filename, 'w', encoding='utf-8') as f:
    json.dump(keyed, f, ensure_ascii=False, indent=2)
