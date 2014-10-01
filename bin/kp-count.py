#!/usr/bin/env python

"""
Counts hours in specified kp file
Darek Stefanski
"""

import datetime
import os
import sys

WORK_DAY_IN_SECS = 8 * 60 * 60

def usage():
   print "Usage: %s file" % sys.argv[0]

def get_kp_file():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    return sys.argv[1]

def get_durations(kp_file):
    durations = []
    f = open(kp_file)
    lines = f.readlines()
    for line in lines:
        line = line.replace("\n", "")
        if not line or line.startswith("#"):
            continue
        # dd.mm.yyyy: hh.mm - hh.mm
        start, end = map(str2time, line.split(":")[1].split("-"))
        dummydate = datetime.date(2000,1,1)
        duration = datetime.datetime.combine(dummydate,  end) - datetime.datetime.combine(dummydate, start)
        durations.append(duration)
    return durations

def str2time(str):
    try:
        hours, minutes = str.split(".")
        return datetime.time(int(hours), int(minutes))
    except ValueError:
        print "Cannot parse time%s" % str
        sys.exit(1)

def ornament(duration):
    if duration.seconds > WORK_DAY_IN_SECS:
        return "+"
    if duration.seconds < WORK_DAY_IN_SECS:
        return "-"
    return ""

def seconds2time(seconds):
    seconds = abs(seconds)
    hours = seconds / (60 * 60)
    minutes = (seconds - hours * 60 * 60) / 60
    return "%dh %dm" % (hours, minutes)

def diff_prefix(diff):
    return "positive" if diff >= 0 else "negative"

kp_file = get_kp_file()
print "Counting hours in %s" % kp_file
durations = get_durations(kp_file)

sum = 0
diff = 0
for d in durations:
    print "%s %s" % (seconds2time(d.seconds), ornament(d))
    sum += d.seconds
    diff += (d.seconds - WORK_DAY_IN_SECS)
print "----------------"
print "TOTAL: %s" % seconds2time(sum)
print "%s diff: %s" % (diff_prefix(diff), seconds2time(diff))
