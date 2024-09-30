SHELL := '/bin/bash'

default: test

diff:
	daff previous-country-codes.csv data/country-codes.csv > daffdiff.csv
	daff render daffdiff.csv > daffdiff.html

test:
	goodtables datapackage.json

all: data/country-codes.csv

.SECONDARY:

data/iso3166.json:
	python3 scripts/iso3166.py  # Calls your custom iso3166 script
	python3 scripts/csvtojson.py data/iso3166.csv data/iso3166-flat.json  # Use your csvtojson function

data/iso4217.json: data/iso3166.json
	python3 scripts/format_json.py
	python3 scripts/iso4217.py

data/statoids.json: data/iso3166.json data/iso4217.json
	python3 scripts/statoids.py

data/country-codes.json: data/statoids.json
	python3 scripts/flatten.py
	cp data/statoids-flat.json data/country-codes.json

data/geoname.csv:
	python3 scripts/geoname.py

data/edgar.csv:
	python3 scripts/edgar.py

data/cldr.csv:
	python3 scripts/cldr.py

data/unterm_names.csv: data/country-codes.json
	python3 scripts/unterm_names.py
	python3 scripts/join_unterm.py
	cp data/country-codes-joined.json data/country-codes.json

data/country-codes.csv: data/country-codes.json data/geoname.csv data/cldr.csv data/edgar.csv data/unterm_names.csv
	in2csv --no-inference --blanks data/country-codes.json > data/country-codes.csv
	csvjoin --no-inference --blanks --left -d ',' -c ISO3166-1-Alpha-3 data/country-codes.csv data/geoname.csv > data/country-codes-geoname.csv
	cp data/country-codes-geoname.csv data/country-codes.csv
	csvjoin --no-inference --blanks --left -d ',' -c ISO3166-1-Alpha-2 data/country-codes.csv data/cldr.csv > data/country-codes-cldr.csv
	cp data/country-codes-cldr.csv data/country-codes.csv
	csvjoin --no-inference --blanks --left -d ',' -c "ISO4217-currency_country_name,name" data/country-codes.csv data/edgar.csv > data/country-codes-edgar.csv
	cp data/country-codes-edgar.csv data/country-codes.csv
	csvcut -n data/country-codes.csv > data/columns.csv
	python3 scripts/reorder_columns.py
	python3 scripts/reorder_rows.py
	cp data/country-codes-reordered-sorted.csv data/country-codes.csv
	./scripts/wd_countries.sh
	python3 scripts/wd_countries.py
	python3 scripts/cleanup.py 
	cp data/country-codes.csv data/previous-country-codes.csv

clean:
	# Delete all .csv files except 'country-codes.csv'
	find data/ -name "*.csv" ! -name "country-codes.csv" -exec rm {} +

	# Delete all .json files
	find data/ -name "*.json" -exec rm {} +

update:
	# Delete the old 'country-codes.csv' if it exists
	rm -f data/country-codes.csv
	
	# Now proceed to update or regenerate 'country-codes.csv'
	make all

.PHONY: diff
.PHONY: test