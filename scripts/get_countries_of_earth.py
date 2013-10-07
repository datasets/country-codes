#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import codecs
import urllib
import argparse
import json
from lxml import html
from lxml import etree

# some ANSI colors, etc
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
BOLD = '\033[1m'
ENDC = '\033[0m'


def print_info(string):
    print GREEN + string + ENDC


def print_warn(string):
    print YELLOW + string + ENDC


def print_error(string):
    print RED + string + ENDC


def process_statoids_row(tr):
    row = []
    for td in tr.iterchildren():
        if len(td.keys()) > 0:
            if td.get('colspan') is not None:
                # if a cell is taking up more than one column,
                # append the same number of blanks to the row
                assert td.get('colspan').isdigit()
                for col in xrange(int(td.get('colspan'))):
                    row.append('')
                continue
        if len(td.getchildren()) == 1:
            if td.find('.//br') is not None:
                if len(td.getchildren()) == 1:
                    if td.getchildren()[0].tag == 'br':
                        td.text = td.text + " " + td.getchildren()[0].tail
                        row.append(td.text)
                        continue
            if td.find("code") is not None:
                # some cells contain more than one code,
                # so append a list also containing the code
                # that appears after the child element (<br>)
                if len(td.find("code").getchildren()) > 0:
                    if td.find('.//br') is not None:
                        row.append(td.find('code').text + ',' + td.find('.//br').tail)
                        continue
                    if td.find('.//a') is not None:
                        anchor = td.find('.//a')
                        # UK has 4 FIFA codes
                        if row[1] == "GB":
                            assert anchor.text == "1"
                            row.append("ENG,NIR,SCO,WAL")
                            continue
                        # MARC treats United States Minor Outlying Islands
                        # as five countries
                        if row[1] == "UM":
                            assert anchor.text == "b"
                            row.append("ji,xf,wk,uc,up")
                            continue
                # some cells contain anchor to footnote,
                # so append only the content of the code element
                row.append(td.find("code").text)
                continue
            else:
                if td.find('.//a') is not None:
                    anchor = td.find('.//a')
                    # FIPS treats United States Minor Outlying Islands
                    # as nine countries
                    if len(row) > 1 and row[1] == "UM":
                        assert anchor.text == "a"
                        row.append("FQ,HQ,DQ,JQ,KQ,MQ,BQ,LQ,WQ")
                        continue
        row.append(td.text_content())
    return row

def clean_line(line):
    try:
        line = line.decode('utf8')
        line = line.rstrip()
        if ';' in line:
            semi = line.index(';')
            name = line[:semi]
            alpha2 = line[semi + 1:]
            return (name, alpha2)
        return (None, None)
    except UnicodeDecodeError:
        print_warn('Unable to decode country name: %s' % line)

def capitalize_country_name(name):
    # replace all-caps name with capitalized country name
    cap_list = []
    always_lower = ['AND', 'THE', 'OF', 'PART', 'DA', 'DE', 'ET', 'DU', 'DES',
                    'LA']
    for w in name.split():
        if w == 'MCDONALD':
            cap_list.append('McDonald')
        if w.find('.') > 0:
            cap_list.append(w.upper())
            continue
        if w.find('\'') > 0:
            # d'Ivoire instead of D'ivoire
            s = w.split('\'')
            if len(s[0]) == 1:
                cap_list.append(s[0].lower() + '\'' + s[1].capitalize())
                continue
        if w.find('-') > 0:
            # Timor-Leste instead of Timor-leste
            cap_list.append('-'.join([s.capitalize() for s in w.split('-')]))
            continue

        if w.startswith('('):
            w = w.replace('(', '')
            if w in always_lower:
                w = w.lower()
            else:
                w = w.capitalize()
            cap_list.append('(' + w)
            continue

        if w[-1] == ')':
            w = w.replace(')', '')
            if w in always_lower:
                w = w.lower()
            else:
                w = w.capitalize()
            cap_list.append(w + ')')
            continue

        if w in always_lower:
            cap_list.append(w.lower())
            continue
        cap_list.append(w.capitalize())

    capitalized = " ".join(cap_list)
    return capitalized

def fetch_and_write(options):
    # fetch ISO short names in English and French
    print_info('Fetching English country names and codes...')
    iso_names_en = urllib.urlretrieve('http://www.iso.org/iso/list-en1-semic-3.txt')
    print_info('Fetching French country names and codes...')
    iso_names_fr = urllib.urlretrieve('http://www.iso.org/iso/list-fr1-semic.txt')

    # dict for combining en and fr names
    # {alpha2: {'name': en, 'name_fr': fr}}
    iso_names = {}

    # dict for looking up alpha2 from name
    en_names = {}

    # urllib.urlretrieve returns a tuple of (localfile, headers)
    with open(iso_names_en[0], "rU") as fin:
        for line in fin:
            name, alpha2 = clean_line(line)
            if name and alpha2:
                iso_names.update({alpha2: {'name': name}})
                en_names.update({name: alpha2})

    with open(iso_names_fr[0], "rU") as fin:
        for line in fin:
            name, alpha2 = clean_line(line)
            if name and alpha2:
                if alpha2 in iso_names:
                    # alpha2 should be in iso_names because
                    # english was parsed first,
                    # so append french name to list
                    names = iso_names[alpha2]
                    names.update({'name_fr': name})
                    iso_names.update({alpha2: names})
                else:
                    # hopefully this doesnt happen, but
                    # in case there was no english name,
                    # add french with a blank space where
                    # english should be
                    names = {'name': '', 'name_fr': name}
                    iso_names.update({alpha2: names})

    # fetch content of statoids.com country code page
    statoids_url = "http://www.statoids.com/wab.html"
    print_info('Fetching other country codes...')
    content = urllib.urlopen(statoids_url).read()
    doc = html.fromstring(content)

    # i dislike some of statoid's column names, so here i have renamed
    # a few to be more descriptive
    column_names = ["Entity", "ISO3166-1-Alpha-2", "ISO3166-1-Alpha-3",
                    "ISO3166-1-numeric", "ITU", "FIPS", "IOC", "FIFA", "DS",
                    "WMO", "GAUL", "MARC", "Dial", "is_independent"]
    alpha2_key = "ISO3166-1-Alpha-2"

    # comment out the preceding two lines and
    # uncomment these lines to use statoids.com column names
    """
    column_names = []
    alpha2_key = 'A-2'
    for tr in doc.find_class('hd'):
        for th in tr.iterchildren():
            column_names.append(th.text_content())
    """

    # dict to hold dicts of all table rows
    table_rows = {}

    # the country code info is in a table where the trs have
    # alternating classes of `e` and `o`
    # so fetch half of the rows and zip each row together
    # with the corresponding column name
    for tr in doc.find_class('e'):
        row = process_statoids_row(tr)
        row_dict = dict(zip(column_names, row))
        table_rows.update({row_dict[alpha2_key]: row_dict})

    # and again for the other half
    for tr in doc.find_class('o'):
        row = process_statoids_row(tr)
        row_dict = dict(zip(column_names, row))
        table_rows.update({row_dict[alpha2_key]: row_dict})

    if options.as_list:
        # list to hold combined country info
        country_info = []
    else:
        # dict to hold combined country info
        country_info = {}
        keyed_by = options.key

    # iterate through all the table_rows
    # TODO this assumes that statoids will have all of
    # the items that are pulled from iso.org
    for alpha2, info in table_rows.iteritems():
        # ignore this crap that was parsed from other tables on the page
        if alpha2 in ['', 'Codes', 'Codes Codes', 'Codes Codes Codes']:
            continue
        cinfo = info
        # add iso.org's names to combined dict of this country's info
        cinfo.update(iso_names[alpha2])
        # replace all-caps name with capitalized country name
        cinfo.update({'name': capitalize_country_name(cinfo['name'])})
        cinfo.update({'name_fr': capitalize_country_name(cinfo['name_fr'])})
        # add combined dict to global (pun intented) data structure
        if options.as_list:
            country_info.append(cinfo)
        else:
            ckey = cinfo[keyed_by]
            country_info.update({ckey: cinfo})

    # fetch iso currency codes
    currency_url = "http://www.currency-iso.org/dam/downloads/table_a1.xml"
    print_info('Fetching currency codes...')
    currencies_xml_str = urllib.urlopen(currency_url).read()
    currencies = etree.fromstring(currencies_xml_str)

    # map source's tag names to our property names
    currency_tag_map = {
        u"CtryNm": u"currency_country_name",
        u"CcyNm": u"currency_name",
        u"Ccy": u"currency_alphabetic_code",
        u"CcyNbr": u"currency_numeric_code",
        u"CcyMnrUnts": u"currency_minor_unit",
        u"AddtlInf": u"currency_additional_info"
    }
    # reconcile country names, add entries for non-country-based currencies
    currency_country_name_map = {
        u"CONGO, THE DEMOCRATIC REPUBLIC OF": "CONGO, THE DEMOCRATIC REPUBLIC OF THE",
        u"HEARD ISLAND AND McDONALD ISLANDS": "HEARD ISLAND AND MCDONALD ISLANDS",
        u"KOREA, DEMOCRATIC PEOPLE’S REPUBLIC OF": "KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF",
        u"LAO PEOPLE’S DEMOCRATIC REPUBLIC": "LAO PEOPLE'S DEMOCRATIC REPUBLIC",
        u"SERBIA ": "SERBIA",
        u"PALESTINIAN TERRITORY, OCCUPIED": "PALESTINE, STATE OF",
        u"Vatican City State (HOLY SEE)": "HOLY SEE (VATICAN CITY STATE)",
        u"VIRGIN ISLANDS (BRITISH)": "VIRGIN ISLANDS, BRITISH",
        u"VIRGIN ISLANDS (US)": "VIRGIN ISLANDS, U.S.",
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
    }
    for iso_currency_table in currencies.iterchildren():
        for iso_currency_element in iso_currency_table.iterchildren():
            currency_dict = {}
            for currency_tag in iso_currency_element.iterchildren():
                # ignore newly added additional info field
                if currency_tag_map[currency_tag.tag] == "currency_additional_info":
                    continue
                currency_dict.update({
                    currency_tag_map[currency_tag.tag]: currency_tag.text})
            currency_alpha2 = None
            currency_name = currency_dict['currency_country_name'].replace(u'\xa0', u'')
            try:
                currency_alpha2 = en_names[currency_name]
            except KeyError:
                currency_alpha2 = en_names.get(
                    currency_country_name_map.get(currency_name))

            if currency_alpha2:
                if options.as_list:
                    cinfo = [c for c in country_info if c['ISO3166-1-Alpha-2'] == currency_alpha2]
                    if len(cinfo) > 0:
                        cinfo[0].update(currency_dict)
                else:
                    country_info[currency_alpha2].update(currency_dict)
            else:
                if currency_name not in currency_country_name_map:
                    print_warn('Failed to match currency data for country: "%s"'
                            % currency_name)

    # dump dict as json to file
    output_filename = "countries-of-earth.json"
    if options.outfile:
        output_filename = options.outfile
    f = open(output_filename, mode='w')
    stream = codecs.getwriter('utf8')(f)
    json.dump(country_info, stream, ensure_ascii=False, indent=2, encoding='utf-8')
    print_info('Saved country data to: %s' % output_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Fetch current ISO 3166 country codes and other standards and output as JSON file')
    parser.add_argument("-o", "--output", dest="outfile", default="countries-of-earth.json",
                        help="write data to OUTFILE", metavar="OUTFILE")
    parser.add_argument("-l", "--list", dest="as_list", default=False, action="store_true",
                        help="export objects as a list of objects")
    parser.add_argument("-k", "--key", dest="key", default="ISO3166-1-Alpha-2",
                        help="export objects as a dict of objects keyed by KEY", metavar="KEY")

    args = parser.parse_args()

    fetch_and_write(args)
