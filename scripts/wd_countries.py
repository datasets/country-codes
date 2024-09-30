#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

def run():
    """
    Retrieving Wikidata IDs by ISO-code and updating the country-codes CSV file.
    """
    wd_countries = pd.read_csv('/Users/gradedsystem/Desktop/country-codes/data/wd_countries.csv')
    country_codes = pd.read_csv('/Users/gradedsystem/Desktop/country-codes/data/country-codes.csv')

    merged_data = pd.merge(country_codes, wd_countries, left_on='ISO3166-1-Alpha-2', right_on='iso2_code', how='left')

    merged_data['wikidata_id'] = 'https://www.wikidata.org/wiki/' + merged_data['wd_id'].fillna('')

    merged_data.to_csv('/Users/gradedsystem/Desktop/country-codes/data/country-codes.csv', index=False)

if __name__ == '__main__':
    run()
