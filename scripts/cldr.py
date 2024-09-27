#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import urllib.request
import config
import utils 

url = config.CLDR_TERRITORIES_URL
header = ['ISO3166-1-Alpha-2', 'CLDR display name']

def run():
    content = json.loads(urllib.request.urlopen(url).read())

    # Adjust the path based on your JSON structure (specifically 'ms' instead of 'en')
    content_territories = content['main']['ms']['localeDisplayNames']['territories']

    # Remove UN regional codes (three digits) and -alt-variants
    territories = {k: v for k, v in content_territories.items() if not k.isdigit() and '-alt-variant' not in k}

    for discard in ['ZZ', 'EZ', 'EU']:
        territories.pop(discard, None)

    # Sort the territories (replace .iteritems() with .items() in Python 3)
    territories = sorted(territories.items())

    cldr = {}
    for territory in territories:
        name = territory[0]

        # Use -alt-short if it exists
        if "-alt-short" in territory[0]:
            name = name.replace("-alt-short", "")
            cldr.pop(name, None)

        cldr[name] = territory[1]

    # Write to CSV file
    with open('data/cldr.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        for row in cldr.items():
            csv_writer.writerow(row)


if __name__ == '__main__':
    run()
