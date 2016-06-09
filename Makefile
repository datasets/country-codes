all:

.SECONDARY:

data/iso3166.json:
	scripts/iso3166.py

data/iso4217.json: data/iso3166.json
	scripts/iso4217.py

data/statoids.json: data/iso3166.json data/iso4217.json
	scripts/statoids.py

data/country-codes.json: data/statoids.json
	scripts/flatten.py
	cp data/statoids-flat.json data/country-codes.json

data/geoname.csv:
	scripts/geoname.py

data/edgar.csv:
	scripts/edgar.py

country-codes.csv: data/country-codes.json data/geoname.csv data/edgar.csv
	in2csv data/country-codes.json > data/country-codes.csv
	scripts/cldr.py
	csvjoin -c ISO3166-1-Alpha-3 data/country-codes-cldr.csv data/geoname.csv > data/country-codes.csv
	csvjoin -c "ISO4217-currency_country_name,name" data/country-codes.csv data/edgar.csv > data/country-codes-edgar.csv
	csvcut -c "name","official_name_en","official_name_fr","ISO3166-1-Alpha-2","ISO3166-1-Alpha-3","ISO3166-1-numeric","ITU","MARC","WMO","DS","Dial","FIFA","FIPS","GAUL","IOC","ISO4217-currency_alphabetic_code","ISO4217-currency_country_name","ISO4217-currency_minor_unit","ISO4217-currency_name","ISO4217-currency_numeric_code","is_independent","Capital","Continent","TLD","Languages","geonameid","EDGAR" data/country-codes-edgar.csv > data/country-codes-reordered.csv
	csvsort -c "name" data/country-codes-reordered.csv > data/country-codes-reordered-sorted.csv
	mv data/country-codes-reordered-sorted.csv data/country-codes.csv

clean:
	@rm data/*.json
	@rm data/*.csv
	@rm data/*.tsv
