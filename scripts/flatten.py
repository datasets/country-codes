#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import json

with open("data/statoids.json", "r", encoding="utf-8") as f:
    country_info = json.load(f)


def itemgetter(*items):
    """Helper function to extract item(s) from a dictionary."""
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return obj.get(item, '')
    else:
        def g(obj):
            return tuple(obj.get(item, '') for item in items)
    return g


country_info = sorted(country_info.values(), key=itemgetter('official_name_en'))

# Write the flattened JSON to a new file
output_filename = "data/statoids-flat.json"
with open(output_filename, mode='w', encoding='utf-8') as f:
    json.dump(country_info, f, ensure_ascii=False, indent=2)

