#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from https://docs.python.org/2/library/csv.html
import functools

replacements = (u'\xa0', u''), (u'\n', u''), (u'\r', u'')

def clean(word):
    # Clean up the word by applying replacements and trimming extra spaces
    return functools.reduce(lambda a, kv: a.replace(*kv), replacements, word).strip()
