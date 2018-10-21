#!/usr/bin/python

# by Sebalinux (sebalinux@sebalinux.it)

from datetime import datetime, timedelta, time
import argparse
import sys

# Consts
dateformat = "%Y-%m-%d"
timeformat = "%H:%M:%S"
# Create argument parser
myparser = argparse.ArgumentParser(description='Generate a date list with optional delta', 
                                   usage='%(prog)s [options]')
myparser = argparse.ArgumentParser(description='Please note: End date '
                                               'is the upper limit, '
                                               'could be not included in the '
                                               'output')

myparser.add_argument('-d', '--delta', help='Delta days, interval between '
                                            'date (default=1)', default='1')

myparser.add_argument('-st','--start-time', help='Start time HH:MM:SS ('
                                                 'default=00:00:00)',
                      default='00:00:00')

myparser.add_argument('-et','--end-time',help='End time HH:MM:SS ('
                                              'default=23:59:59)',
                      default='23:59:59')

required = myparser.add_argument_group('required arguments')
required.add_argument('-s', '--start-date', help='Start date YYYY-MM-DD',
                      required=True)

required.add_argument('-e', '--end-date', help='Up to date YYYY-MM-DD ('
                                               'may be excluded from list '
                                               'based on delta value)',
                      required=True)


# check if arguments is passed, otherwise print help
if len(sys.argv) == 1:
    myparser.parse_args(['-h'])
else:
    args = myparser.parse_args()

delta = int(args.delta)

# validate date
try:
    startdate = datetime.strptime(args.start_date, dateformat)
except ValueError:
    print("ERROR - Date format MUST be YYYY-MM-DD")
    sys.exit(1)

try:
    enddate = datetime.strptime(args.end_date, dateformat)
except ValueError:
    print("ERROR - Date format MUST be YYYY-MM-DD")
    sys.exit(1)

if startdate > enddate:
    print("ERROR - Start date can't be after end date!")
    print("")
    print("Start date: %s") % startdate.date()
    print("End date  : %s") % enddate.date()
    sys.exit(1)

# validate time
try:
    start_time = datetime.strptime(args.start_time, timeformat)
except ValueError:
    print("ERROR - Time format MUST be HH:MM:SS")
    print("")
    sys.exit(1)

try:
    end_time = datetime.strptime(args.end_time, timeformat)
except ValueError:
    print("ERROR - Time format MUST be HH:MM:SS")
    print("")
    sys.exit(1)

# Check time
if delta == 1 and (end_time <= start_time):
    print("ERROR - Within the same day End time MUST be greater than Start "
          "time")
    print("")
    sys.exit(1)

# Split time values
st_hours, st_minutes, st_seconds = map(int, args.start_time.split(":"))
et_hours, et_minutes, et_seconds = map(int, args.end_time.split(":"))

# Setting loop variables
loop_startdate = startdate
loop_enddate = loop_startdate + timedelta(days=delta-1)

# start loop
while loop_enddate <= enddate:
    start_period = datetime.combine(loop_startdate, time(st_hours,
                                                         st_minutes,
                                                         st_seconds))

    end_period = datetime.combine(loop_enddate, time(et_hours, et_minutes,
                                                     et_seconds))

    print(str(start_period) + "," + str(end_period))
    loop_startdate = loop_enddate + timedelta(days=1)
    loop_enddate = loop_startdate + timedelta(days=delta - 1)
