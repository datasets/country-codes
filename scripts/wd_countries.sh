#!/bin/bash

## retrieving Wikidata dataset by SparQL:
curl -o data/wd_countries.csv -G 'https://query.wikidata.org/sparql' \
     --header "Accept: text/csv"  \
     --data-urlencode query='
 SELECT DISTINCT (?simple_value AS ?iso2_code) ?wd_id
 WHERE {
   ?item p:P297 ?statement .
   ?statement ps:P297 ?simple_value .
   OPTIONAL { ?statement pq:P582 ?qualifier . }
   FILTER ( !bound(?qualifier) )
   BIND ( strafter(str(?item), str(wd:)) AS ?wd_id ).
 } ORDER BY ?iso2_code
'

# Eliminate duplication (confusion with kingdoms and territories)
# in the future we can use "P31 Q417175" to eliminate doublets of kingdows, but "territory vs nation" need some check.
# so, filtering invalid doublets and saving with same name:
grep -v 'Q756617\|Q29999\|Q407199\|Q240592\|Q83286\|Q1246' data/wd_countries.csv  | sponge data/wd_countries.csv

# Use awk to modify the second column, write to a temporary file
awk -F, 'BEGIN {OFS = FS} {if (NR > 1) $2="https://www.wikidata.org/wiki/" $2; print}' "data/wd_countries.csv" > "data/wd_countries.tmp.csv"

# Replace original file with the updated file
mv data/wd_countries.tmp.csv data/wd_countries.csv

# filtering also the last two, that are not in use at ISO: Q83286=old YU, Yugoslavia; Q1246=XK, Kosovo.
# filtering wrong duplicated Q240592 Macedonia.
