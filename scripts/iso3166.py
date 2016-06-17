#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import urllib

from lxml import html

un_iso3166_en_url = "http://unstats.un.org/unsd/methods/m49/m49alpha.htm"
un_iso3166_fr_url = "http://unstats.un.org/unsd/methods/m49/m49alphaf.htm"

content_en = urllib.urlopen(un_iso3166_en_url).read()
doc_en = html.fromstring(content_en)

# get last table, then its tbody
tbody_en = doc_en.xpath('//table[last()]')[0].getchildren()[0]

# dict for iso3166 english and french, keyed by ISO3166-1-numeric
#
# FYI Sark, a royal fief that is part of the Bailiwick of Guernsey, is listed
# here with a numeric code (680), but not an ISO3166-1-Alpha-3
# ... same with 'Channel Islands' (830)
#
# view-source:http://unstats.un.org/unsd/methods/m49/m49alpha.htm
# line 1788 is missing an opening <tr>, so lets start with Sudan
# as it shows up as three <td> elements that are siblings to all of
# the other <tr>s and will be skipped in the loop below
iso3166 = {u'729': {u'ISO3166-1-Alpha-3': u'SDN',
                    u'ISO3166-1-numeric': u'729',
                    u'official_name_en': u'Sudan'}}

for row in tbody_en.iterchildren():
    cells = row.getchildren()
    if len(cells) != 3:
        print('ERROR IN CELL COUNT')
        for cell in cells:
            print(cell)
            print(cell.text_content())
        continue
    numerical = cells[0].text_content().replace('\r\n','').strip()
    name = cells[1].text_content().replace('\r\n','').strip()
    alpha3 = cells[2].text_content().replace('\r\n','').strip()
    if alpha3.startswith('ISO ALPHA-3'):
        # skip first row of column headers
        print('SKIPPING', numerical, name, alpha3)
        continue
    iso3166.update({numerical: {'ISO3166-1-numeric': numerical, 'official_name_en': name,
                                'ISO3166-1-Alpha-3': alpha3}})

# fetch French
content_fr = urllib.urlopen(un_iso3166_fr_url).read()
doc_fr = html.fromstring(content_fr)

# of course the French version of the STANDARD has different markup...
table_fr = doc_fr.xpath('//table')[6]

for row in table_fr.iterchildren():
    cells = row.getchildren()
    if len(cells) != 3:
        print('ERROR IN CELL COUNT')
        for cell in cells:
            print(cell)
            print(cell.text_content())
        continue
    numerical = cells[0].text_content().replace('\r\n','').strip()
    name = cells[1].text_content().replace('\r\n','').strip()
    alpha3 = cells[2].text_content().replace('\r\n','').strip()
    if alpha3.startswith('Code ISO'):
        # skip first row of column headers
        print('SKIPPING', numerical, name, alpha3)
        continue
    country = iso3166.get(numerical)
    if country:
        country.update({'official_name_fr': name})
        iso3166.update(country)
    else:
        print('NOT FOUND', numerical, name, alpha3)

# where are these coming from?!
iso3166.pop('ISO3166-1-numeric')
iso3166.pop('ISO3166-1-Alpha-3')
iso3166.pop('official_name_en')
iso3166.pop('official_name_fr')

output_filename = "data/iso3166.json"
f = open(output_filename, mode='w')
stream = codecs.getwriter('utf8')(f)
json.dump(iso3166, stream, ensure_ascii=False, indent=2, encoding='utf-8')
