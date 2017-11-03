SHELL := '/bin/bash'

default: test

diff:
	daff previous-country-codes.csv data/country-codes.csv > daffdiff.csv
	daff render daffdiff.csv > daffdiff.html

test:
	goodtables datapackage.json

all:

.SECONDARY:

data/iso3166.csv:
	csvcut -c 10,9 source/UNSD-fr.csv > data/UNSD-fr-cut.csv
	sed -i '' 's/Country or Area/official_name_fr/' data/UNSD-fr-cut.csv
	csvcut -c 10,9 source/UNSD-ar.csv > data/UNSD-ar-cut.csv
	sed -i '' 's/Country or Area/official_name_ar/' data/UNSD-ar-cut.csv
	csvcut -c 10,9 source/UNSD-cn.csv > data/UNSD-cn-cut.csv
	sed -i '' 's/Country or Area/official_name_cn/' data/UNSD-cn-cut.csv
	csvcut -c 10,9 source/UNSD-es.csv > data/UNSD-es-cut.csv
	sed -i '' 's/Country or Area/official_name_es/' data/UNSD-es-cut.csv
	csvcut -c 10,9 source/UNSD-ru.csv > data/UNSD-ru-cut.csv
	sed -i '' 's/Country or Area/official_name_ru/' data/UNSD-ru-cut.csv
	csvjoin --blanks --left -c "M49 Code" source/UNSD-en.csv data/UNSD-fr-cut.csv data/UNSD-ar-cut.csv data/UNSD-cn-cut.csv data/UNSD-es-cut.csv data/UNSD-ru-cut.csv > data/iso3166.csv
	sed -i '' 's/M49 Code/M49/' data/iso3166.csv
	sed -i '' 's/Country or Area/official_name_en/' data/iso3166.csv
	sed -i '' 's/ISO-alpha3 Code/ISO3166-1-Alpha-3/' data/iso3166.csv

data/iso3166.json: data/iso3166.csv
	csvjson --blanks data/iso3166.csv > data/iso3166-flat.json
	scripts/format_json.py

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

data/cldr.csv:
	scripts/cldr.py

data/unterm_names.csv: data/country-codes.json
	scripts/unterm_names.py
	scripts/join_unterm.py
	cp data/country-codes-joined.json data/country-codes.json

country-codes.csv: data/country-codes.json data/geoname.csv data/cldr.csv data/edgar.csv data/unterm_names.csv
	in2csv --no-inference --blanks data/country-codes.json > data/country-codes.csv
	csvjoin --no-inference --blanks --left -c ISO3166-1-Alpha-3 data/country-codes.csv data/geoname.csv > data/country-codes-geoname.csv
	cp data/country-codes-geoname.csv data/country-codes.csv
	csvjoin --no-inference --blanks --left -c ISO3166-1-Alpha-2 data/country-codes.csv data/cldr.csv > data/country-codes-cldr.csv
	cp data/country-codes-cldr.csv data/country-codes.csv
	csvjoin --no-inference --blanks --left -c "ISO4217-currency_country_name,name" data/country-codes.csv data/edgar.csv > data/country-codes-edgar.csv
	cp data/country-codes-edgar.csv data/country-codes.csv
	csvcut -n data/country-codes.csv > data/columns.csv
	scripts/reorder_columns.py
	scripts/reorder_rows.py
	cp data/country-codes-reordered-sorted.csv data/country-codes.csv
	cp data/country-codes.csv previous-country-codes.csv

clean:
	@rm data/*.csv
	@rm data/*.json

.PHONY: diff
.PHONY: test
