#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import subprocess

subprocess.call('csvcut -c "name","name_fr","ISO3166-1-Alpha-2","ISO3166-1-Alpha-3","ISO3166-1-numeric","ITU","MARC","WMO","DS","Dial","FIFA","FIPS","GAUL","IOC","currency_alphabetic_code","currency_country_name","currency_minor_unit","currency_name","currency_numeric_code","is_independent" data/country-codes.csv > data/country-codes-reordered.csv', shell=True)
subprocess.call('mv data/country-codes-reordered.csv data/country-codes.csv', shell=True)
