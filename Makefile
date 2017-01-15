default: diff

diff:
	scripts/compare.py

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
	# cldr.py expects existing data/country-codes.csv and outputs to the same
	scripts/cldr.py
	csvjoin --left -c ISO3166-1-Alpha-3 data/country-codes-cldr.csv data/geoname.csv > data/country-codes.csv
	csvjoin --left -c "ISO4217-currency_country_name,name" data/country-codes.csv data/edgar.csv > data/country-codes-edgar.csv
	# csvjoin includes the `name` column from data/edgar.csv which duplicates `ISO4217-currency_country_name`, so use csvcut to include what we want in correct order
	csvcut -c "name","official_name_en","official_name_fr","ISO3166-1-Alpha-2","ISO3166-1-Alpha-3","ISO3166-1-numeric","ITU","MARC","WMO","DS","Dial","FIFA","FIPS","GAUL","IOC","ISO4217-currency_alphabetic_code","ISO4217-currency_country_name","ISO4217-currency_minor_unit","ISO4217-currency_name","ISO4217-currency_numeric_code","is_independent","Capital","Continent","TLD","Languages","geonameid","EDGAR" data/country-codes-edgar.csv > data/country-codes-reordered.csv
	# quick fix to misnamed column
	# TODO update scripts to use M49 column name
	sed -i '' 's/ISO3166-1-numeric/M49/' data/country-codes-reordered.csv
	csvsort --no-inference -c "name" data/country-codes-reordered.csv > data/country-codes-reordered-sorted.csv
	cp data/country-codes-reordered-sorted.csv data/country-codes.csv

clean:
	@rm data/*.json
	@rm data/*.csv
	@rm data/*.tsv

.PHONY: diff
