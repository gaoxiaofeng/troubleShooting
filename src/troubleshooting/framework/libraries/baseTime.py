# -*- coding: utf-8 -*-
import re
def convertTime(Timestr):
    Time = 0
    pattern_hours = re.compile(".*?(\d+)\s*h")
    match = pattern_hours.match(Timestr)
    if match:
        _hours = match.group(1)
        try:
            _hours_int = int(_hours)
        except:
            _hours_int = 0
        Time += 3600 * _hours_int

    pattern_minutes = re.compile(".*?(\d+)\s*m")
    match = pattern_minutes.match(Timestr)
    if match:
        _minutes = match.group(1)
        try:
            _minutes_int = int(_minutes)
        except:
            _minutes_int = 0
        Time += 60 * _minutes_int

    pattern_secs = re.compile(".*?(\d+)\s*s")
    match = pattern_secs.match(Timestr)
    if match:
        _secs = match.group(1)
        try:
            _secs_int = int(_secs)
        except:
            _secs_int = 0
        Time += _secs_int

    return Time