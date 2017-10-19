#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import json
import urllib

from lxml import etree
from fuzzywuzzy import process

import utils

country_info = json.loads(open("data/iso3166.json").read())
# mapping of names to ISO3166-1-numeric
en_names = {v.get('official_name_en').upper(): k
            for k, v in country_info.iteritems()}

iso4217_url = "https://www.currency-iso.org/dam/downloads/lists/list_one.xml"
#currencies_xml_str = open("source/table_a1.xml").read()
currencies_xml_str = urllib.urlopen(iso4217_url).read()
currencies = etree.fromstring(currencies_xml_str)

# map source's tag names to our property names
currency_tag_map = {
    u"CtryNm": u"ISO4217-currency_country_name",
    u"CcyNm": u"ISO4217-currency_name",
    u"Ccy": u"ISO4217-currency_alphabetic_code",
    u"CcyNbr": u"ISO4217-currency_numeric_code",
    u"CcyMnrUnts": u"ISO4217-currency_minor_unit",
    u"AddtlInf": u"ISO4217-currency_additional_info"
}
# reconcile country names, add entries for non-country-based currencies
currency_country_name_map = {
    u"MACEDONIA, THE FORMER \nYUGOSLAV REPUBLIC OF": "MACEDONIA, THE FORMER YUGOSLAV REPUBLIC OF",
    u"SAINT HELENA, ASCENSION AND \nTRISTAN DA CUNHA": "SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA",
    u"CABO VERDE": "CAPE VERDE",
    u"HEARD ISLAND AND McDONALD ISLANDS": "HEARD ISLAND AND MCDONALD ISLANDS",
    u"LAO PEOPLE’S DEMOCRATIC REPUBLIC": "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
    u"SERBIA ": "SERBIA",
    u"PALESTINIAN TERRITORY, OCCUPIED": "PALESTINE, STATE OF",
    u"Vatican City State (HOLY SEE)": "HOLY SEE (VATICAN CITY STATE)",
    u"VIRGIN ISLANDS (BRITISH)": "VIRGIN ISLANDS, BRITISH",
    u"VIRGIN ISLANDS (U.S.)": "VIRGIN ISLANDS, U.S.",
    u"MEMBER COUNTRIES OF THE AFRICAN DEVELOPMENT BANK GROUP": None,
    u"INTERNATIONAL MONETARY FUND (IMF)": None,
    u"SISTEMA UNITARIO DE COMPENSACION REGIONAL DE PAGOS \"SUCRE\"": None,
    u"EUROPEAN UNION": None,
    u"ZZ01_Bond Markets Unit European_EURCO": None,
    u"ZZ02_Bond Markets Unit European_EMU-6": None,
    u"ZZ03_Bond Markets Unit European_EUA-9": None,
    u"ZZ04_Bond Markets Unit European_EUA-17": None,
    u"ZZ05_UIC-Franc": None,
    u"ZZ06_Testing_Code": None,
    u"ZZ07_No_Currency": None,
    u"ZZ08_Gold": None,
    u"ZZ09_Palladium": None,
    u"ZZ10_Platinum": None,
    u"ZZ11_Silver": None,
    u"BOLIVIA, PLURINATIONAL STATE OF": u"Bolivia (Plurinational State of)",
    u"HOLY SEE (VATICAN CITY STATE)": u"Holy See",
    u"IRAN, ISLAMIC REPUBLIC OF": u"Iran (Islamic Republic of)",
    u"MACAO": u"China, Macao Special Administrative Region",
    u"MICRONESIA, FEDERATED STATES OF": u"Micronesia (Federated States of)",
    u"PALESTINE, STATE OF": u"State of Palestine",
    u"SAINT HELENA, ASCENSION AND TRISTAN DA CUNHA": u"Saint Helena",
    u"SVALBARD AND JAN MAYEN": u"Svalbard and Jan Mayen Islands",
    u"TANZANIA, UNITED REPUBLIC OF": u"United Republic of Tanzania",
    u"UNITED KINGDOM": u"United Kingdom of Great Britain and Northern Ireland",
    u"UNITED STATES": u"United States of America",
    u"VENEZUELA, BOLIVARIAN REPUBLIC OF": u"Venezuela (Bolivarian Republic of)",
    u"WALLIS AND FUTUNA": u"Wallis and Futuna Islands",
    u"VIRGIN ISLANDS (U.S.)": u"UNITED STATES VIRGIN ISLANDS",
    u"VIRGIN ISLANDS (BRITISH)": u"BRITISH VIRGIN ISLANDS",

    u"CONGO (THE DEMOCRATIC REPUBLIC OF THE)": "DEMOCRATIC REPUBLIC OF THE CONGO",
    u"KOREA (THE DEMOCRATIC PEOPLE’S REPUBLIC OF)": u"DEMOCRATIC PEOPLE'S REPUBLIC OF KOREA",
    u"KOREA (THE REPUBLIC OF)": u"REPUBLIC OF KOREA",
    u"FALKLAND ISLANDS [MALVINAS]": u"FALKLAND ISLANDS",
    u"HONG KONG": u'CHINA, HONG KONG SPECIAL ADMINISTRATIVE REGION',
    u"MACEDONIA (THE FORMER YUGOSLAV REPUBLIC OF)": U"THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA",
    u"MOLDOVA (THE REPUBLIC OF)": u"REPUBLIC OF MOLDOVA",
}


def process_element(country):
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
        # some countries have multiple currency records in source dataset
        # so check whether we have already added keys for currency info
        # to our country_info dict
        if set(currency_dict.keys()).issubset(set(country_info[country_code].keys())):
            for k, v in currency_dict.items():
                # don't duplicate name of country
                if k != "ISO4217-currency_country_name":
                    existing_value = country_info[country_code][k]
                    country_info[country_code][k] = ','.join([existing_value, v])
        else:
            country_info[country_code].update(currency_dict)
    else:
        print('Failed to match currency data for country: "%s"'
                % currency_name)

    return

for iso_currency_table in currencies.iterchildren():
    for country in iso_currency_table.iterchildren():
        process_element(country)

output_filename = "data/iso4217.json"
f = open(output_filename, mode='w')
stream = codecs.getwriter('utf8')(f)
json.dump(country_info, stream, ensure_ascii=False, indent=2, encoding='utf-8')
