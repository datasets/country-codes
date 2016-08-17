#!/usr/bin/env python
# -*- coding: utf-8 -*-


replacements = (u'\xa0', u''), (u'\n', u''), (u'\r', u'')


def clean(word):
    reduce(lambda a, kv: a.replace(*kv), replacements, word)
    return " ".join(word.split())
