Comprehensive country code information, including ISO 3166 codes, ITU dialing
codes, ISO 4217 currency codes, and many others. Provided as a Simple Data
Format Data Package.

## Data

Data comes from multiple sources as follows.

ISO 3166 offical English and French short names are from
[iso.org](http://www.iso.org/iso/country_codes/iso_3166_code_lists.htm)
Note: ISO is no longer providing these code lists for free.

ISO 4217 currency codes are from
[currency-iso.org](http://www.currency-iso.org/en/home/tables/table-a1.html)

Many other country codes are from
[statoids.com](http://www.statoids.com/wab.html)

Special thanks to Gwillim Law for his excellent
[statoids.com](http://www.statoids.com) site (some of the field descriptions
are excerpted from his site), which is more up-to-date than most similar
resources and is much easier to scrape than multiple Wikipedia pages.

## Preparation

This package includes a Python script to fetch current country information
and output a JSON document of combined country code information.
Per-country JSON documents may be keyed by any of the fields below.

CSV output is provided via the `in2csv` and `csvcut` utilities from [csvkit](http://github.com/onyxfish/csvkit)

Run **scripts/get_countries_of_earth.py --help** for usage information

### data/country-codes.csv

Install requirements:

    pip install -r scripts/requirements.pip


Run the python script to generate json file:

    python scripts/get_countries_of_earth.py -l


Convert json file to csv (and reorder columns):

    in2csv data/country-codes.json > data/country-codes.csv
    python scripts/reorder_columns.py


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

