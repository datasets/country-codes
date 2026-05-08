#!/usr/bin/env python3
"""
Manual corrections for known data errors that survive pipeline reruns.

WHY THIS EXISTS
---------------
Most fields are populated automatically from upstream sources (statoids.com,
geonames.org, UN Statistics, etc.). When an upstream source contains an error
or lags behind reality, the automated pipeline faithfully reproduces the wrong
value on every run — making a direct CSV edit pointless, because `make update`
overwrites it the next time it runs.

This script applies a curated set of overrides *after* all automated sources
have been merged (it is the last step in the Makefile). Corrections here
survive pipeline reruns and are auditable: each entry records what is wrong,
why, and where the correct value was verified.

HOW TO ADD A CORRECTION
------------------------
Append an entry to CORRECTIONS below. Each dict requires:

  match_col   — column used to identify the row, ideally a stable unique key
                such as 'ISO3166-1-Alpha-2' or 'ISO3166-1-Alpha-3'
  match_val   — value in that column that identifies the target row
  field       — column whose value needs to be fixed
  correct_val — the correct value to write
  reason      — plain-English explanation of why the upstream value is wrong
  source      — URL or citation confirming the correct value

WHY NO AUTOMATED SOURCE FOR FIFA CODES?
----------------------------------------
FIFA codes are the primary driver of this script. There is no single
authoritative, machine-readable, freely-licensed list of FIFA codes:

statoids.com (current source for FIFA codes in this pipeline)
  Gwillim Law's reference site is well-researched and covers many code
  systems simultaneously, making it the most practical single scrape
  target. However, it is a personal project that is no longer actively
  maintained. Some FIFA codes have not been updated to reflect changes
  made by FIFA over the past decade (code changes, newly admitted
  associations). Statoids remains the source for all other codes it
  provides (IOC, FIPS, DS, WMO, etc.); only specific FIFA values are
  overridden here.

FIFA's own website (https://www.fifa.com/associations/)
  Authoritative, but FIFA provides no downloadable or machine-readable
  list. The association pages use JavaScript rendering. The project
  already uses Selenium for EDGAR scraping, so adding a FIFA scraper
  is technically feasible, but FIFA's page structure changes without
  notice and would require ongoing maintenance. A dedicated FIFA scraper
  would also be slower and less stable than the statoids scrape.

footballsquads.co.uk (https://www.footballsquads.co.uk/fifacodes.htm)
  Scrapeable without JavaScript, but covers only ~142 of FIFA's ~211
  member associations (Sudan and South Sudan are absent entirely). It
  also contains some of the same outdated codes as statoids (e.g. LIB
  for Lebanon instead of LBN), so substituting it would not eliminate
  the need for this correction layer.

Wikipedia (https://en.wikipedia.org/wiki/List_of_FIFA_country_codes)
  Generally more complete and more current than statoids or
  footballsquads. However: (1) Wikipedia's content licence (CC BY-SA
  4.0) requires attribution and share-alike, which conflicts with this
  dataset's public-domain dedication; (2) the page structure changes
  without notice, making scrapers fragile; (3) Wikipedia itself
  sometimes lags FIFA announcements by weeks or months.

Bottom line: the correction layer is the pragmatic choice. It keeps the
statoids pipeline intact (which correctly supplies many other fields),
and surfaces divergences explicitly in version-controlled code rather
than silently in data.
"""

import pandas as pd

CORRECTIONS = [
    {
        'match_col': 'ISO3166-1-Alpha-2',
        'match_val': 'SD',
        'field': 'FIFA',
        'correct_val': 'SDN',
        'reason': (
            'Statoids lists SUD, the historical code used before FIFA aligned '
            'its codes more closely with ISO 3166-1 alpha-3. The current FIFA '
            'designation for the Sudan Football Association is SDN.'
        ),
        'source': 'https://www.fifa.com/associations/association/SDN/',
    },
    {
        'match_col': 'ISO3166-1-Alpha-2',
        'match_val': 'SS',
        'field': 'FIFA',
        'correct_val': 'SSD',
        'reason': (
            'South Sudan was admitted to FIFA in 2012 and assigned the code '
            'SSD. Statoids has no FIFA entry for South Sudan.'
        ),
        'source': 'https://www.fifa.com/associations/association/SSD/',
    },
    {
        'match_col': 'ISO3166-1-Alpha-2',
        'match_val': 'LB',
        'field': 'FIFA',
        'correct_val': 'LBN',
        'reason': (
            'Statoids lists LIB, which is Lebanon\'s MARC library cataloguing '
            'code, not its FIFA code. The Lebanese Football Association is '
            'designated LBN by FIFA.'
        ),
        'source': 'https://www.fifa.com/associations/association/LBN/',
    },
    {
        'match_col': 'ISO3166-1-Alpha-2',
        'match_val': 'GI',
        'field': 'FIFA',
        'correct_val': 'GIB',
        'reason': (
            'Gibraltar was admitted to FIFA in 2016 and assigned the code GIB. '
            'Statoids still lists GBZ, which is the vehicle distinguishing sign '
            'for Gibraltar, not its FIFA code.'
        ),
        'source': 'https://www.fifa.com/associations/association/GIB/',
    },
]


def apply_corrections(df: pd.DataFrame) -> pd.DataFrame:
    for c in CORRECTIONS:
        mask = df[c['match_col']] == c['match_val']
        if not mask.any():
            print(f"WARNING: no row matched {c['match_col']}={c['match_val']!r} — correction skipped")
            continue
        old = df.loc[mask, c['field']].iloc[0]
        if old == c['correct_val']:
            print(f"OK (already correct): {c['match_val']} {c['field']}={c['correct_val']!r}")
        else:
            df.loc[mask, c['field']] = c['correct_val']
            print(f"CORRECTED: {c['match_val']} {c['field']} {old!r} -> {c['correct_val']!r}")
    return df


def run():
    df = pd.read_csv('data/country-codes.csv', keep_default_na=False)
    df = apply_corrections(df)
    df.to_csv('data/country-codes.csv', index=False)


if __name__ == '__main__':
    run()
