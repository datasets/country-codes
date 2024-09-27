#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

with open('data/iso3166-flat.json', 'r') as f:
    countries = json.load(f)

keyed = {
    country['ISO3166-1-Alpha-3']: {
        **country, 
        **{k: str(int(float(v))) for k, v in country.items() 
           if k in ["Sub-region Code", "M49", "Region Code", "Intermediate Region Code"] 
           and v not in [None, '', ' ']}
    }
    for country in countries
}

with open('data/iso3166.json', 'w', encoding='utf-8') as f:
    json.dump(keyed, f, ensure_ascii=False, indent=2)
