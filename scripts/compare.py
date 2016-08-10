#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import os
import subprocess

# TODO doesnt work with python 3
# TODO https://docs.python.org/2/library/os.path.html#os.path.join
local_changes = subprocess.check_output(["git", "diff",
                                         "data/country-codes.csv"])

latest_commit_sha = subprocess.check_output(["git", "rev-parse",
                                             "HEAD"]).rstrip()
latest_commit_stats = "tests/%s-csvstat.txt" % latest_commit_sha


def save_stats_for_latest_commit():
    try:
        latest_commit_stats_filename = "tests/%s-csvstat.txt" % latest_commit_sha
        latest_commit_stats_file = open(latest_commit_stats_filename, "w")
        subprocess.call(["csvstat", "data/country-codes.csv"],
                        stdout=latest_commit_stats_file)
    except:
        print("something went wrong!")


if not os.path.isfile(latest_commit_stats):
    try:
        # check for uncommitted, staged changes
        staged = subprocess.check_output(["git", "diff-index", "--quiet",
                                          "--cached", "data/country-codes.csv"])
        # check for working tree changes
        dirty = subprocess.check_output(["git", "diff-files", "--quiet",
                                         "data/country-codes.csv"])
        save_stats_for_latest_commit()
    except subprocess.CalledProcessError:
        print("no stats for last commit and there are uncommited changes to data/country-codes.csv!")
        print("attempting to stash changes...")
        subprocess.call(["git", "stash", "--quiet"])
        save_stats_for_latest_commit()
        subprocess.call(["git", "stash", "--quiet", "pop"])

if local_changes:
    current_stats = open("tests/csvstat.txt", "w")
    subprocess.call(["csvstat", "data/country-codes.csv"], stdout=current_stats)

    try:
        subprocess.check_output(["diff",
                                 "tests/csvstat.txt", latest_commit_stats])
    except subprocess.CalledProcessError as diff:
        print('comparing csvstat output of local changes and latest commit:')
        print(diff.output)
