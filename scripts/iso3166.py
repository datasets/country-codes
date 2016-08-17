#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import codecs
import urllib

from bs4 import BeautifulSoup

import utils


un_iso3166_en_url = "http://unstats.un.org/unsd/methods/m49/m49alpha.htm"
un_iso3166_fr_url = "http://unstats.un.org/unsd/methods/m49/m49alphaf.htm"

content_en = urllib.urlopen(un_iso3166_en_url).read()
soup_en = BeautifulSoup(content_en)

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

rows_en = soup_en.find_all('tr')

for row in rows_en:
    cells = row.find_all('td')
    if len(cells) != 3:
        print('ERROR IN CELL COUNT')
        print(cells)
        continue
    if cells[0] is not None:
        if cells[0].text.startswith('South') or cells[0].text.startswith('Sudan'):
            continue
    numerical = utils.clean(cells[0].text)
    name = utils.clean(cells[1].text)
    alpha3 = utils.clean(cells[2].text)
    if alpha3.startswith('ISO ALPHA-3'):
        # skip first row of column headers
        print('SKIPPING', numerical, name, alpha3)
        continue
    iso3166.update({numerical: {'ISO3166-1-numeric': numerical, 'official_name_en': name,
                                'ISO3166-1-Alpha-3': alpha3}})

# fetch French
content_fr = urllib.urlopen(un_iso3166_fr_url).read()
soup_fr = BeautifulSoup(content_fr)


rows_fr = soup_fr.find_all('tr')

for row in rows_fr:
    cells = row.find_all('td')
    if len(cells) != 3:
        print('ERROR IN CELL COUNT')
        print(cells)
        continue
    numerical = utils.clean(cells[0].text)
    name = utils.clean(cells[1].text)
    alpha3 = utils.clean(cells[2].text)
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
