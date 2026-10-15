<a className="gh-badge" href="https://datahub.io/core/country-codes"><img src="https://badgen.net/badge/icon/View%20on%20datahub.io/orange?icon=https://datahub.io/datahub-cube-badge-icon.svg&label&scale=1.25" alt="badge" /></a>

# Country codes

Codes and names for every country and territory that has an ISO 3166-1 entry, in one CSV file. It combines the ISO 3166 alpha-2, alpha-3 and numeric codes with other code systems (ITU, FIPS, IOC, FIFA, WMO and more), telephone dialling codes, ISO 4217 currency codes, UN M49 region groupings, country names in six languages, and identifiers from GeoNames, the SEC (EDGAR) and Wikidata.

Column definitions and types are in `datapackage.yml`. Provided as a [Tabular Data Package](https://specs.frictionlessdata.io/tabular-data-package): [view datapackage](https://raw.githubusercontent.com/datasets/country-codes/refs/heads/main/datapackage.yml).

## Data

`data/country-codes.csv` has one row per country or territory. The columns come from several sources; the table under [Data sources](#data-sources) shows which source feeds which columns. Rows are sorted by `official_name_en`, using the sort order of the machine that builds the file, so a few names can change places from one build to another. The columns `ISO3166-1-Alpha-2` and `ISO3166-1-Alpha-3` are each unique.

### Known limitations

* **`NA` is real data.** The `Continent` code for North America is `NA`, the alpha-2 code of Namibia is `NA`, and the `DS` value of Bonaire, Sint Eustatius and Saba is `NA`. `pandas.read_csv` turns `NA` into a missing value by default, so these cells come back empty. Turn that off and read everything as text:

  ```python
  import pandas as pd
  df = pd.read_csv("data/country-codes.csv", dtype=str, keep_default_na=False)
  ```

* **Numeric codes have no leading zeros.** `ISO3166-1-numeric`, `M49` and the UN region codes are stored as plain numbers, for example `4` for Afghanistan, where ISO writes `004`. To get the 3-digit form:

  ```python
  df["ISO3166-1-numeric"] = df["ISO3166-1-numeric"].str.zfill(3)
  ```

  `ISO4217-currency_numeric_code` keeps its leading zeros (for example `008`), so read it as text too.
* **Some empty cells are not empty.** Where Statoids has no code, the cell holds a single non-breaking space (U+00A0) instead of nothing. This happens in `FIFA`, `Dial`, `MARC`, `FIPS`, `WMO`, `ITU`, `IOC` and `DS`; a few other cells (for example `Capital`) have stray spaces. Remove them after reading:

  ```python
  df = df.apply(lambda col: col.str.strip())
  ```

* **One cell can hold several values, separated by commas.** For example `Dial` for `DO` is `1-809,1-829,1-849`, `Languages` lists several language codes, and countries with two currencies have two values in each `ISO4217-currency_*` column, in the same order (for example `BT` has `INR,BTN` and `356,064`). Use `.str.split(",")` to separate them.
* **Not every column is filled for every row.** The `UNTERM ...` columns are empty for many territories and for some countries (for example `AQ`, `HK` and `CI`). `EDGAR` is matched by country name, so it is empty where the SEC name differs (for example `CA` and `US`). The region columns are empty for Antarctica (`AQ`). The optional UN groupings (`Least Developed Countries (LDC)`, `Land Locked Developing Countries (LLDC)`, `Small Island Developing States (SIDS)`) are empty unless the country is in that group.
* **A few `FIFA` values are not 3-letter codes** (for example `1` for `GB` and `ROS3` for `AQ`). The pipeline leaves a value as it is when neither it nor the country's ISO alpha-3 code is on the FIFA list. Check this column before relying on it.
* **`wikidata_id` is a full URL**, for example `https://www.wikidata.org/wiki/Q889`, not just the `Q` number.
* Only ISO 3166-1 entries have a row. Kosovo (`XK`), for example, has none.

## Data sources

The licence column says what we found about reuse; see [License](#license) for what was checked.

| Source | Columns it feeds | Licence |
|---|---|---|
| [UN Protocol and Liaison Service, UNTERM names](https://www.un.org/dgacm/sites/www.un.org.dgacm/files/Documents_Protocol/unterm-efsrca.xlsx) | `UNTERM <language> Short` and `UNTERM <language> Formal`, for English, French, Spanish, Russian, Chinese and Arabic | **Restricted.** The [UN website terms of use](https://www.un.org/en/about-us/terms-of-use) allow downloading and copying "for the User’s personal, non-commercial use, without any right to resell or redistribute them or to compile or create derivative works therefrom". The file is hosted on un.org and we found no separate licence for it. |
| [UN Statistics Division, M49](https://unstats.un.org/unsd/methodology/m49/overview/) | `ISO3166-1-Alpha-3`, `M49`, `official_name_en`, `official_name_fr`, `official_name_es`, `official_name_ar`, `official_name_cn`, `official_name_ru`, `Global Code`, `Global Name`, `Region Code`, `Region Name`, `Sub-region Code`, `Sub-region Name`, `Intermediate Region Code`, `Intermediate Region Name`, `Least Developed Countries (LDC)`, `Land Locked Developing Countries (LLDC)`, `Small Island Developing States (SIDS)` | Licence unclear. The page states no licence. The UN website terms quoted above probably apply to it, but we could not confirm that. |
| [Statoids](https://statoids.com/wab.html) | `ISO3166-1-Alpha-2`, `ISO3166-1-numeric`, `ITU`, `FIPS`, `IOC`, `FIFA` (first pass), `DS`, `WMO`, `GAUL`, `MARC`, `Dial`, `is_independent` | Licence unclear. The site carries a copyright notice and states no licence or permission to reuse. |
| [SIX Group, ISO 4217 list one](https://www.six-group.com/dam/download/financial-information/data-center/iso-currrency/lists/list-one.xml) | `ISO4217-currency_country_name`, `ISO4217-currency_name`, `ISO4217-currency_alphabetic_code`, `ISO4217-currency_numeric_code`, `ISO4217-currency_minor_unit` | Licence unclear. SIX publishes the list free of charge and states no licence for the XML file. |
| [FIFA member associations](https://inside.fifa.com/associations) | `FIFA` (checks and corrects the Statoids value, and fills it when empty) | Licence unclear. The terms of this page have not been read. |
| ISO (the codes themselves) | `ISO3166-1-Alpha-2`, `ISO3166-1-Alpha-3`, `ISO3166-1-numeric` and the `ISO4217-currency_*` codes | Licence unclear. [ISO](https://committee.iso.org/iso-4217-currency-codes.html) allows "free-of-charge use of its country, currency and language codes" and also says "Any use, including reproduction requires our written permission." |
| [GeoNames](https://download.geonames.org/export/dump/countryInfo.txt) | `Capital`, `Continent`, `TLD`, `Languages`, `Geoname ID` | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit to GeoNames is required (see [ATTRIBUTION.txt](ATTRIBUTION.txt)). |
| [Unicode CLDR](https://raw.githubusercontent.com/unicode-org/cldr-json/refs/heads/main/cldr-json/cldr-localenames-full/main/en/territories.json) | `CLDR display name` | [Unicode License v3](https://www.unicode.org/license.txt). The copyright and permission notice must travel with the data; it is in [ATTRIBUTION.txt](ATTRIBUTION.txt). |
| [SEC EDGAR](https://www.sec.gov/submit-filings/filer-support-resources/edgar-state-country-codes) | `EDGAR` | Free to copy and share. The SEC [asks for a citation](https://www.sec.gov/privacy.htm) but does not require one. |
| [Wikidata](https://query.wikidata.org/sparql) | `wikidata_id` | [CC0](https://www.wikidata.org/wiki/Wikidata:Licensing) (public domain). |

Notes on the sources:

* The UN short names, M49 codes and region groupings come from the M49 lists, which the UN Statistics Division bases on UNTERM. They are the UN's short forms, not ISO 3166 names, so some differ: for example `official_name_en` is `Ivory Coast` for `CI`, where the ISO 4217 list and CLDR use `Côte d’Ivoire`.
* `CLDR display name` is the customary English short name from CLDR, for example `South Korea`. The ISO 4217 country names are in capitals, as SIX publishes them.
* The Statoids country-code table was last updated in 2016 (see [License](#license)), so some of its codes may lag behind the standards. FIFA codes are checked against FIFA's own list for that reason.

Changes made to the source data: the scripts in `scripts/` download each source and join the tables into one file by ISO alpha-3 code, alpha-2 code or country name (UNTERM names are matched to the UN English names with a fuzzy matcher that must give a perfect score, SIX names by exact match after a fixed list of name fixes, and EDGAR names by exact match to the SIX country names). Columns are renamed and reordered, duplicate rows are dropped, and rows are sorted by `official_name_en`. UNTERM rows that are not complete in all six languages are skipped. SIX entries marked as funds are skipped, and when a country has several currencies the values are joined with commas. For CLDR, where a name has a `-alt-short` form (for example `BA-alt-short`), that shorter name is used; `-alt-variant` names, numeric region codes and the codes `ZZ`, `EZ` and `EU` are ignored. FIFA values that are not on FIFA's list are replaced by the country's ISO alpha-3 code when that code is on the list. For Wikidata, the entity ID is turned into a URL, and a few duplicate or retired items are removed. No GeoNames, CLDR, SEC or Wikidata value is otherwise edited.

Not endorsed by, or affiliated with, the United Nations, ISO, SIX Group, Statoids, FIFA, GeoNames, Unicode, Inc., the U.S. Securities and Exchange Commission or Wikidata.

## Preparation

The file is rebuilt from the live sources by running the scripts. You need:

* Python 3 (the workflow uses 3.12) and the packages in `scripts/requirements.txt`, which include [csvkit](https://github.com/wireservice/csvkit) (the `in2csv`, `csvjoin` and `csvcut` tools), Selenium, pandas and Frictionless:

  ```
  pip install -r scripts/requirements.txt
  ```

* Google Chrome. The EDGAR step (`scripts/edgar.py`) drives it through Selenium because the SEC site refuses plain downloads. On a server without a display, also install Xvfb and start it first:

  ```
  Xvfb :99 -screen 0 1024x768x24 &
  export DISPLAY=:99
  ```

* `curl` for the Wikidata step, and the `en_US.UTF-8` locale for the row sorting in `scripts/reorder_rows.py`.

Then, from the repository root:

```
make update
make clean
```

`make update` downloads the sources and rebuilds `data/country-codes.csv`; `make clean` deletes the temporary files it leaves in `data/`. `make test` checks the result with `frictionless validate datapackage.yml`.

The six UN M49 files in `tmp/` (`UNSD-en.csv`, `UNSD-fr.csv`, `UNSD-es.csv`, `UNSD-ar.csv`, `UNSD-cn.csv`, `UNSD-ru.csv`) are committed to this repository and read by `scripts/iso3166.py`. `make update` does not download them, so the UN M49 region codes and the UN names in six languages only change when someone replaces these files. To refresh them, download the six language versions from the [M49 page](https://unstats.un.org/unsd/methodology/m49/overview/), rename them to the names above and copy them into `tmp/`. No manual step is needed for a normal `make update`.

A GitHub workflow (`.github/workflows/actions.yml`) runs the same steps with Xvfb on the 1st of every month at 00:00 UTC, on every push to `main`, and on demand. It commits `data/country-codes.csv` if it changed.

## License

This file combines data from several sources whose terms differ. Where they are clear, they are given in the table above. In short:

* **Restricted:** the `UNTERM ...` columns. The UN terms quoted above allow personal, non-commercial use and give no right to redistribute or to create derivative works. The file is compiled from these names and redistributes them.
* **Clear, with credit or a notice:** GeoNames (CC BY 4.0, credit required), Unicode CLDR (notice required), SEC EDGAR (citation requested). Wikidata is CC0.
* **Licence unclear:** the UN Statistics Division M49 columns, Statoids, SIX Group, FIFA, and ISO's own rights in the codes.

What was checked, and what could not be established:

* UN: the UN website terms of use and copyright page. We found no UNTERM or M49 licence that replaces them.
* Statoids: the site has copyright notices and no licence page. It also sells its administrative-division spreadsheets under reuse limits (those are different files from the free code table). Its founder, Gwillim Law, died in 2016; the site is now run by his family, and the country-code table was last updated in 2016.
* SIX Group: the data standards page says the lists are free of charge, but there is no licence for the XML file. The SIX website terms say the content of the SIX website may not be reproduced or reused commercially; they do not say whether that covers the XML.
* ISO: the sentence quoted in the table, read on [ISO's page](https://committee.iso.org/iso-4217-currency-codes.html).
* FIFA: we did not read any terms.

We could not establish whether the unclear sources allow republishing or commercial use. Before using this file in a public or commercial product, check the terms of the sources marked restricted or unclear.

The maintainers place only their own work (the scripts, and the selection and arrangement of the data) under the [Public Domain Dedication and License (PDDL)](https://opendatacommons.org/licenses/pddl/1.0/). This does not cover the data taken from the sources and does not remove the UN restriction. See also [ATTRIBUTION.txt](ATTRIBUTION.txt).
