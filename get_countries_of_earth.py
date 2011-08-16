#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4
import codecs
import urllib
from optparse import OptionParser
from lxml import html

try:
    import simplejson as json
except ImportError:
    import json

def fetch_and_write(options):
    # fetch ISO short names in English and French
    iso_names_en = urllib.urlretrieve('http://www.iso.org/iso/list-en1-semic-3.txt')
    iso_names_fr = urllib.urlretrieve('http://www.iso.org/iso/list-fr1-semic.txt')

    # dict for combining en and fr names
    # {alpha2: {'short_name_en': en, 'short_name_fr': fr}}
    iso_names = {}

    # urllib.urlretrieve returns a tuple of (localfile, headers)
    with open(iso_names_en[0], "rU") as fin:
        for line in fin:
            # decode iso.org's silly windows encoding
            line = line.decode('cp1252')
            # strip line endings, etc
            line = line.rstrip()
            # fields are semicolon delineated,
            # so split into separate parts
            if ';' in line:
                semi = line.index(';')
                name = line[:semi]
                alpha2 = line[semi+1:]
                if name and alpha2:
                    iso_names.update({alpha2: {'short_name_en': name}})

    with open(iso_names_fr[0], "rU") as fin:
        for line in fin:
            line = line.decode('cp1252')
            line = line.rstrip()
            if ';' in line:
                semi = line.index(';')
                name = line[:semi]
                alpha2 = line[semi+1:]
                if name and alpha2:
                    if alpha2 in iso_names:
                        # alpha2 should be in iso_names because
                        # english was parsed first,
                        # so append french name to list
                        names = iso_names[alpha2]
                        names.update({'short_name_fr': name})
                        iso_names.update({alpha2: names})
                    else:
                        # hopefully this doesnt happen, but
                        # in case there was no english name,
                        # add french with a blank space where
                        # english should be
                        names = {'short_name_en': '', 'short_name_fr': name}
                        iso_names.update({alpha2: names})

    # fetch content of statoids.com country code page
    statoids_url = "http://www.statoids.com/wab.html"
    content = urllib.urlopen(statoids_url).read()
    doc = html.fromstring(content)

    # i dislike some of statoid's column names, so here i have renamed
    # a few to be more descriptive
    column_names = ["Entity", "ISO3166-1-Alpha-2","ISO3166-1-Alpha-3","ISO3166-1-numeric","ITU","FIPS","IOC","FIFA","DS","WMO","GAUL","MARC","Dial","is_independent"]
    alpha2_key = "ISO3166-1-Alpha-2"

    """
    # comment out the preceding two lines and
    # uncomment these lines to use statoids.com column names
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
        row = []
        for td in tr.iterchildren():
            row.append(td.text_content())
        row_dict = dict(zip(column_names, row))
        table_rows.update({row_dict[alpha2_key]: row_dict})

    # now do the same for the other half
    for tr in doc.find_class('o'):
        row = []
        for td in tr.iterchildren():
            row.append(td.text_content())
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
        if alpha2 in ['Codes', 'Codes Codes', 'Codes Codes Codes']:
            continue
        cinfo = info
        # add iso.org's names to combined dict of this country's info
        cinfo.update(iso_names[alpha2])
        # add combined dict to global (pun intented) data structure
        if options.as_list:
            country_info.append(cinfo)
        else:
            ckey = cinfo[keyed_by]
            country_info.update({ckey: cinfo})

    # dump dict as json to file
    f = open("countries-of-earth.json", mode='w')
    stream = codecs.getwriter('utf8')(f)
    json.dump(country_info, stream, ensure_ascii=False, indent=2, encoding='utf-8')

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-o", "--output", dest="outfile", default="countries-of-earth.json",
                        help="write data to OUTFILE", metavar="OUTFILE")
    parser.add_option("-l", "--list", dest="as_list", default=False, action="store_true",
                        help="export objects as a list of objects")
    parser.add_option("-k", "--key", dest="key", default="ISO3166-1-Alpha-2",
                        help="export objects as a dict of objects keyed by KEY", metavar="KEY")
    
    (options, args) = parser.parse_args()

    fetch_and_write(options)
