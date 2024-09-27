#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import utils
import codecs
import config

from lxml import etree
from rapidfuzz import process
from urllib.request import urlopen

output_filename = "data/iso4217.json"
iso4217_url = config.ISO4217_URL
currency_tag_map = config.CURRENCY_TAG_MAP
currency_country_name_map = config.CURRENCY_COUNTRY_NAME_MAP

def process_element(country, en_names, country_info):
    currency_dict = {}
    currency_name = None
    for currency_tag in country.iterchildren():
        # ignore newly added additional info field
        if currency_tag_map[currency_tag.tag] ==\
                "ISO4217-currency_additional_info":
            break
        # skip 'same day', 'next day', etc variations
        elif (currency_tag_map[currency_tag.tag] == "ISO4217-currency_name")\
                and (len(currency_tag.items()) > 0):
            if currency_tag.items()[0][0] == 'IsFund':
                break
        else:
            currency_dict.update({
                currency_tag_map[currency_tag.tag]: currency_tag.text})
            # remove random line breaks, etc
            currency_name = utils.clean(currency_dict['ISO4217-currency_country_name']).upper().replace(' (THE)', '')
            if currency_name is not None:
                # replace name with line breaks, etc removed
                currency_dict['ISO4217-currency_country_name'] = currency_name

    country_code = None
    try:
        country_code = en_names[currency_name]
    except KeyError:
        mapped_name = currency_country_name_map.get(currency_name)
        if mapped_name is not None:
            country_code = en_names.get(mapped_name.upper())
    if country_code:
        # some countries have multiple currency records in the source dataset
        # so check whether we have already added keys for currency info
        if set(currency_dict.keys()).issubset(set(country_info[country_code].keys())):
            for k, v in currency_dict.items():
                # don't duplicate the name of the country
                if k != "ISO4217-currency_country_name":
                    existing_value = country_info[country_code][k]
                    # Only join if the key already exists and isn't empty
                    country_info[country_code][k] = ','.join([existing_value, v]) if existing_value else v
        else:
            country_info[country_code].update(currency_dict)
    else:
        print(f'Failed to match currency data for country: "{currency_name}"')

    return

def run():
    with open(config.ISO3166_FILE_NAME , "r") as f:
        country_info = json.loads(f.read())
    # mapping of names to ISO3166-1-numeric
    en_names = {}
    en_names = {v.get('official_name_en', '').upper(): k
            for k, v in country_info.items()}

    try:
        currencies_xml_str = urlopen(iso4217_url).read()
        currencies = etree.fromstring(currencies_xml_str)
    except Exception as e:
        print(f"Failed to fetch or parse XML: {e}")
    for iso_currency_table in currencies.iterchildren():
        for country in iso_currency_table.iterchildren():
            process_element(country, en_names, country_info)

    f = open(output_filename, mode='w')
    with open(output_filename, mode='w', encoding='utf-8') as f:
        json.dump(country_info, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    run()

