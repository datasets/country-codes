<a className="gh-badge" href="https://datahub.io/core/country-codes"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

## Description

Comprehensive country code information, including ISO 3166 codes, ITU dialing
codes, ISO 4217 currency codes, and many others. Provided as a [Tabular Data Package](https://specs.frictionlessdata.io/tabular-data-package): [view datapackage](https://raw.githubusercontent.com/datasets/country-codes/refs/heads/main/datapackage.yml)

## Data

Data are fetched from multiple sources:

- Official formal and short names (in English, French, Spanish, Arabic, Chinese, and Russian) are from
[United Nations Protocol and Liaison Service](https://www.un.org/dgacm/sites/www.un.org.dgacm/files/Documents_Protocol/unterm-efsrca.xlsx)

- Customary English short names are from
[Unicode Common Locale Data Repository (CLDR) Project](https://raw.githubusercontent.com/unicode-org/cldr-json/d38478855dd8342749f0494332cc8acc2895d20d/cldr-json/cldr-localenames-full/main/ms/territories.json).

> Note: CLDR shorter names "ZZ-alt-short" are used when available

- ISO 3166 official short names (in English, French, Spanish, Arabic, Chinese, and Russian) are from
[United Nations Department of Economic and Social Affairs Statistics Division](https://unstats.un.org/unsd/methodology/m49/overview/)

- ISO 4217 currency codes are from
[currency-iso.org](https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml)

- Many other country codes are from
[statoids.com](http://www.statoids.com/wab.html)

Special thanks to Gwillim Law for his excellent
[statoids.com](http://www.statoids.com) site (some of the field descriptions
are excerpted from his site), which is more up-to-date than most similar
resources and is much easier to scrape than multiple Wikipedia pages.

- Capital cities, languages, continents, TLDs, and geonameid are from [geonames.org](http://download.geonames.org/export/dump/countryInfo.txt)

- EDGAR codes are from [sec.gov](https://www.sec.gov/submit-filings/filer-support-resources/edgar-state-country-codes)

- Wikidata entity URLs (`wikidata_id`) are fetched via the [Wikidata SPARQL endpoint](https://query.wikidata.org/sparql) using the ISO 3166-1 alpha-2 property (P297)


## Preparation

This package includes Python scripts to fetch current country information
from various data sources and output CSV of combined country code information.

CSV output is provided via the `in2csv` and `csvcut` utilities from [csvkit](http://github.com/onyxfish/csvkit)

NOTE: The six UN M49 files in `tmp/` (`UNSD-en.csv`, `UNSD-fr.csv`, `UNSD-es.csv`,
`UNSD-ar.csv`, `UNSD-cn.csv`, `UNSD-ru.csv`) are committed to this repository and
read by `scripts/iso3166.py`. `make update` does not download them, so the UN M49
region codes and the UN names in six languages only change when someone replaces
these files. To refresh them, download the six language versions from
https://unstats.un.org/unsd/methodology/m49/overview/, rename them to the names
above and copy them into `tmp/`. No manual step is needed for a normal `make update`.

### data/country-codes.csv

Install requirements:

    pip install -r scripts/requirements.txt


Run GNU Make to generate data file:

    make update
    #then
    make clean

### Reading the CSV: the "NA" trap

Some values in `data/country-codes.csv` are the text `NA`: the `Continent` code for
North America (41 rows) and the alpha-2 code and `DS` value of Namibia. `pandas.read_csv`
treats `NA` as a missing value by default, so these cells come back empty. Turn that off:

    import pandas as pd
    df = pd.read_csv("data/country-codes.csv", dtype=str, keep_default_na=False)

## License

This material is licensed by its maintainers under the Public Domain Dedication
and License.

Nevertheless, it should be noted that this material is ultimately sourced from
ISO and other standards bodies and their rights and licensing policies are somewhat
unclear. As this is a short, simple database of facts there is a strong argument
that no rights can subsist in this collection. However, ISO state on [their
site](http://www.iso.org/iso/home/standards/country_codes.htm):

> ISO makes the list of alpha-2 country codes available for internal use and
> non-commercial purposes free of charge.

This carries the implication (though not spelled out) that other uses are not
permitted and that, therefore, there may be rights preventing further general
use and reuse.

If you intended to use these data in a public or commercial product, please
check the original sources for any specific restrictions.

