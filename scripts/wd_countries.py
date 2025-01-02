#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pandas as pd

def run():
    """
    Retrieving Wikidata IDs by ISO-code and updating the country-codes CSV file.
    """
    wd_countries = pd.read_csv('data/wd_countries.csv')
    country_codes = pd.read_csv('data/country-codes.csv', keep_default_na=False)

    wd_countries = wd_countries.drop_duplicates(subset=['iso2_code'], keep='first')
    
    merged_data = pd.merge(country_codes, wd_countries, left_on='ISO3166-1-Alpha-2', right_on='iso2_code', how='left')

    merged_data['wikidata_id'] = merged_data['wd_id'].fillna('')

    merged_data.to_csv('data/country-codes.csv', index=False)

if __name__ == '__main__':
    run()
