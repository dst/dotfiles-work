#!/usr/bin/env python

"""
Counts hours in specified kp file
Darek Stefanski
"""

import ConfigParser
import datetime
import os
import sys
from collections import defaultdict


DEFAULT_WORK_WEEK_HOURS = 40
HOUR_IN_SECS = 60 * 60
KP_CONFIG_FILE = os.path.expanduser('~/.kp.cfg')


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


def get_work_week_hours():
    if os.path.exists(KP_CONFIG_FILE):
        config = ConfigParser.ConfigParser()
        config.read(KP_CONFIG_FILE)
        return config.getint('KP', 'work-week-hours')
    else:
        return DEFAULT_WORK_WEEK_HOURS


def get_work_day_in_secs():
    return get_work_week_hours() / 5. * HOUR_IN_SECS


def get_durations(kp_file):
    durations = defaultdict(datetime.timedelta)
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
        day = tokens[0]
        start, end = map(str2time, tokens[1].split("-"))
        duration = calculate_duration(start, end)
        durations[day] += duration
    return durations


def str2time(str):
    try:
        hours, minutes = str.split(".")
        return datetime.time(int(hours), int(minutes))
    except ValueError:
        exit_with_msg("Cannot parse time%s" % str)


def calculate_duration(start, end):
    dummy_date = datetime.date(2000, 1, 1)
    return datetime.datetime.combine(dummy_date, end) - datetime.datetime.combine(dummy_date, start)


def ornament(duration, work_day_in_secs):
    if duration.seconds > work_day_in_secs:
        return "+"
    elif duration.seconds < work_day_in_secs:
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
    print "Counting hours in %s with work week of %d hours" % (kp_file, get_work_week_hours())

    sum = 0
    diff = 0
    work_day_in_secs = get_work_day_in_secs()
    durations = get_durations(kp_file)
    for day in sorted(durations):
        duration = durations[day]
        print "%s: %s %s" % (day, seconds2time(duration.seconds), ornament(duration, work_day_in_secs))
        sum += duration.seconds
        diff += (duration.seconds - work_day_in_secs)
    print "----------------"
    print "TOTAL: %s" % seconds2time(sum)
    print "%s diff: %s" % (diff_prefix(diff), seconds2time(diff))


if __name__ == "__main__":
    main()
