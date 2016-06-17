#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import json
import codecs

country_info = json.loads(open("data/statoids.json").read())


def itemgetter(*items):
    if len(items) == 1:
        item = items[0]

        def g(obj):
            return obj.get(item, '')
    else:
        def g(obj):
            return tuple(obj.get(item, '') for item in items)
    return g


country_info = sorted(country_info.values(), key=itemgetter('official_name_en'))

output_filename = "data/statoids-flat.json"
f = open(output_filename, mode='w')
stream = codecs.getwriter('utf8')(f)
json.dump(country_info, stream, ensure_ascii=False, indent=2, encoding='utf-8')
