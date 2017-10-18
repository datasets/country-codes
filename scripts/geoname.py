#!/usr/bin/python
# -*- coding: utf-8 -*

import urllib
import csv

url = 'http://download.geonames.org/export/dump/countryInfo.txt'
dest = urllib.urlopen(url)


def get_data():
    '''gets data necessary from retrievd file
    '''
    for line in dest.readlines():
        if line[0] != '#' and line[0] != '\n':
            splited = line.split('\t')
            # iso3166-alpha3, capital, continent code, tld, languages, geoname id
            yield splited[1], splited[5], splited[8], splited[9], splited[15], splited[16]

header = ['ISO3166-1-Alpha-3', 'Capital', 'Continent', 'TLD', 'Languages', 'Geoname ID']
with open('data/geoname.csv', 'wb') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(header)
    for row in get_data():
        csv_writer.writerow(row)
