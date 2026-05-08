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

NOTE ON FIFA CODES
------------------
FIFA codes are handled automatically by scripts/fifa.py, which fetches the
authoritative list of member codes directly from inside.fifa.com on every
pipeline run. Add FIFA corrections there only if the ISO 3166-1 alpha-3
fallback in fifa.py cannot resolve them automatically.
"""

import csv

CORRECTIONS = [
    # No entries yet. Add field-specific overrides here as needed.
    # Example:
    # {
    #     'match_col': 'ISO3166-1-Alpha-2',
    #     'match_val': 'XX',
    #     'field': 'SomeField',
    #     'correct_val': 'correct value',
    #     'reason': 'Why the upstream value is wrong.',
    #     'source': 'https://example.com/reference',
    # },
]


def apply_corrections(rows: list, fieldnames: list) -> list:
    if not CORRECTIONS:
        print('No corrections defined.')
        return rows
    for c in CORRECTIONS:
        for row in rows:
            if row[c['match_col']] == c['match_val']:
                old = row[c['field']]
                if old == c['correct_val']:
                    print(f"OK (already correct): {c['match_val']} {c['field']}={c['correct_val']!r}")
                else:
                    row[c['field']] = c['correct_val']
                    print(f"CORRECTED: {c['match_val']} {c['field']} {old!r} -> {c['correct_val']!r}")
                break
        else:
            print(f"WARNING: no row matched {c['match_col']}={c['match_val']!r} — correction skipped")
    return rows


def run():
    with open('data/country-codes.csv', newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())
    rows = apply_corrections(rows, fieldnames)
    with open('data/country-codes.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)


if __name__ == '__main__':
    run()
