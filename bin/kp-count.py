#!/usr/bin/env python

"""
Counts hours in specified kp file
Darek Stefanski
"""

import datetime
import sys

HOUR_IN_SECS = 60 * 60
WORK_DAY_IN_SECS = 8 * HOUR_IN_SECS


def usage():
   print "Usage: %s file" % sys.argv[0]


def exit_with_msg(msg):
    print msg
    sys.exit(1)


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
        tokens = line.split(":")
        if len(tokens) != 2:
            exit_with_msg("Incorrect line: %s" % line)
        start, end = map(str2time, tokens[1].split("-"))
        duration = calculate_duration(start, end)
        durations.append(duration)
    return durations


def str2time(str):
    try:
        hours, minutes = str.split(".")
        return datetime.time(int(hours), int(minutes))
    except ValueError:
        exit_with_msg("Cannot parse time%s" % str)


def calculate_duration(start, end):
    dummy_date = datetime.date(2000, 1, 1)
    return datetime.datetime.combine(dummy_date,  end) - datetime.datetime.combine(dummy_date, start)


def ornament(duration):
    if duration.seconds > WORK_DAY_IN_SECS:
        return "+"
    elif duration.seconds < WORK_DAY_IN_SECS:
        return "-"
    else:
        return ""


def seconds2time(seconds):
    seconds = abs(seconds)
    hours = seconds / HOUR_IN_SECS
    minutes = (seconds - hours * HOUR_IN_SECS) / 60
    return "%dh %dm" % (hours, minutes)


def diff_prefix(diff):
    return "positive" if diff >= 0 else "negative"


def main():
    kp_file = get_kp_file()
    print "Counting hours in %s" % kp_file

    sum = 0
    diff = 0
    for d in get_durations(kp_file):
        print "%s %s" % (seconds2time(d.seconds), ornament(d))
        sum += d.seconds
        diff += (d.seconds - WORK_DAY_IN_SECS)
    print "----------------"
    print "TOTAL: %s" % seconds2time(sum)
    print "%s diff: %s" % (diff_prefix(diff), seconds2time(diff))

if __name__ == "__main__":
    main()
