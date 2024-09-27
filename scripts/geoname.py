#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib.request
import csv

url = 'http://download.geonames.org/export/dump/countryInfo.txt'
dest = urllib.request.urlopen(url)
header = ['ISO3166-1-Alpha-3', 'Capital', 'Continent', 'TLD', 'Languages', 'Geoname ID']

def get_data():
    '''gets data necessary from retrieved file
    '''
    for line in dest.readlines():
        line = line.decode('utf-8')  # Decode bytes to string
        if line[0] != '#' and line[0] != '\n':
            splited = line.split('\t')
            # iso3166-alpha3, capital, continent code, tld, languages, geoname id
            yield splited[1], splited[5], splited[8], splited[9], splited[15], splited[16]

def run():
    with open('data/geoname.csv', 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(header)
        for row in get_data():
            csv_writer.writerow(row)

if __name__ == '__main__':
    run()
