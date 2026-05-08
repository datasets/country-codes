#!/usr/bin/env python3
"""
Fetch the authoritative list of FIFA member association codes from
inside.fifa.com and update the FIFA column in country-codes.csv.

SOURCE
------
https://inside.fifa.com/associations — server-side rendered page that lists
all 211 FIFA member associations as hyperlinks in the form /associations/<CODE>.
A 200 response confirms a code is a current FIFA member; a 404 confirms it is
not. No individual association pages are fetched; the full member list comes
from a single request to the index.

WHY NOT STATOIDS?
-----------------
FIFA codes in this dataset were historically sourced from statoids.com, a
reference site by Gwillim Law covering many code systems simultaneously.
Statoids is no longer actively maintained. Some of its FIFA codes predate
changes FIFA made years ago — code reassignments and newly admitted members
— and there is no automated way to detect when statoids lags behind FIFA.

WHY NOT OTHER SOURCES?
----------------------
No single authoritative machine-readable source for FIFA codes exists apart
from FIFA's own site:

  footballsquads.co.uk  — covers only ~142 of 211 members; also has
                          outdated codes (e.g. LIB for Lebanon)

  Wikipedia             — generally more current than statoids, but its
                          CC BY-SA licence conflicts with this dataset's
                          public-domain dedication, and page structure
                          changes without notice

  fifa.com              — the public-facing site is a JavaScript SPA that
                          returns no useful data to plain HTTP requests

inside.fifa.com is the FIFA intranet/editorial site. It returns fully
server-side rendered HTML, requires no authentication, and its /associations
index is stable and complete.

APPROACH
--------
1. Fetch the index page in one HTTP request and extract all /associations/<CODE>
   hrefs, excluding the six confederation codes (AFC, CAF, CONCACAF, CONMEBOL,
   OFC, UEFA).

2. For each row in country-codes.csv:
   - If the current FIFA code is already in the valid set, leave it unchanged.
   - If the current FIFA code is absent or not in the valid set, try the
     country's ISO 3166-1 alpha-3 code as a candidate. Many FIFA codes are
     identical to the ISO alpha-3 code, and this covers the majority of cases
     where statoids has an outdated or missing value.
   - If neither works, leave the field unchanged and emit a warning so the
     case can be handled in corrections.py if needed.
"""

import csv
import re
import urllib.request

INDEX_URL = 'https://inside.fifa.com/associations'
CONFEDERATION_CODES = {'AFC', 'CAF', 'CONCACAF', 'CONMEBOL', 'OFC', 'UEFA'}
CSV_PATH = 'data/country-codes.csv'


def fetch_valid_codes() -> set:
    req = urllib.request.Request(
        INDEX_URL,
        headers={'User-Agent': 'Mozilla/5.0 (compatible; country-codes-bot/1.0)'},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        html = resp.read().decode('utf-8', errors='replace')
    codes = set(re.findall(r'/associations/([A-Z]{2,4})"', html))
    return codes - CONFEDERATION_CODES


def run():
    valid = fetch_valid_codes()
    print(f'Fetched {len(valid)} valid FIFA member codes from inside.fifa.com')

    with open(CSV_PATH, newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
        fieldnames = list(rows[0].keys())

    changed = 0
    warned = 0
    for row in rows:
        current = row['FIFA'].strip()
        if current in valid:
            continue

        iso3 = row['ISO3166-1-Alpha-3'].strip()
        if iso3 in valid:
            action = 'ASSIGNED' if not current else 'CORRECTED'
            print(f'{action}: {row["ISO3166-1-Alpha-2"]} FIFA {current!r} -> {iso3!r}')
            row['FIFA'] = iso3
            changed += 1
        elif current:
            print(
                f'WARNING: {row["ISO3166-1-Alpha-2"]} FIFA {current!r} not in valid FIFA codes '
                f'and ISO alpha-3 {iso3!r} also not valid — left unchanged; '
                f'add to corrections.py if the correct code is known'
            )
            warned += 1

    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)

    print(f'Done. {changed} FIFA codes updated, {warned} unresolved warnings.')


if __name__ == '__main__':
    run()
