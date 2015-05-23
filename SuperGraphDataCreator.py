#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Date range to periods calculator ; 2015, LibreSoft

"""
Super-script to control GraphDataCreator, specially when study covers wide 
periods of time.
Executes the main script depending on time periods, calculated according
a given value in configuration file. (Default: 6 months periods) and
organizes final data using a folder for each period.
"""

#TODO: Export resulting methods in a CSV file

import os
import sys
from time import strftime, gmtime
import operator
from datetime import datetime,timedelta
from itertools import count, islice
from datetime import date
from dateutil.relativedelta import relativedelta
import subprocess
import shutil
import commands
import graph_settings

config = graph_settings.config

def check_date(date, date_type):
    """
    Checks if a date (type: starting or ending)
    has format 'YYYY-MM-DD'. Returns pair of values:
    [<0/1>(wrong/correct), description]
    """
    date = str(date)
    date_fields = date.split('-')
    result = [0, ""]
    if len(date_fields) == 3:
        if date_fields[0] >= 1971:
            if (int(date_fields[1]) > 0) and (int(date_fields[1]) < 13):
                if (int(date_fields[2]) > 0) and (int(date_fields[2]) < 32):
                    result[0] = 1

    if result[0]:
        result[1] = "Valid " + date_type + " date: " + date
    else:
        result[1] = date_type + " date is wrong. "
        result[1] += "\nPlease use option -h for further information"
    return result

def datetime_range(start, end, num):
    """
    For a given period of time (two dates), the function calculates using this 
    time lapse resulting monthly periods.
    """
    start_secs = (start - datetime(1970, 1, 1)).total_seconds()
    end_secs = (end - datetime(1970, 1, 1)).total_seconds()
    dates = [datetime.fromtimestamp(el) 
             for el in islice(count(start_secs, 
                                    (end_secs - start_secs) / num),
                                     num + 1)]
    return zip(dates, dates[1:])

def MonthsBetweenDates(BeginDate, EndDate):
    """
    Calculates how many months there are between two dates
    """
    firstyearmonths = [mn for mn in range(BeginDate.month, 13)]
    lastyearmonths = [mn for mn in range(1, EndDate.month+1)]
    months = [mn for mn in range(1, 13)]
    numofyearsbtween = EndDate.year - BeginDate.year - 1
    if BeginDate.year == EndDate.year:
        return EndDate.month - BeginDate.month
    else:
        ret = len(firstyearmonths + months * numofyearsbtween + lastyearmonths)
        return ret
        
        
class SuperGraphData:

    def __init__(self):
        self.date_now = strftime("%Y-%m-%d", gmtime())
        self.conf_opt = {}
        self.conf_opt['v'] = True  # Verbose option (-v)
        self.conf_opt['f'] = '1971-1-1'  # Starting date of study option (-f)
        self.conf_opt['t'] = self.date_now  # Ending date opt. (-t)
        self.conf_opt['r'] = ""  # Repository URL option (-r)
        self.conf_opt['h'] = False  # Show help option (-h)
        self.conf_opt['p'] = 6  # Months by period

        self.BD = [0, 0, 0]
        self.ED = [0, 0, 0]
    
    def extract_options(self):
        """
        Extracts data from configuration file and completes options dictionary
        """
        for option in config.keys():
            self.conf_opt[option] = config[option]
        self.BD = self.conf_opt['f'].split('-')
        self.ED = self.conf_opt['t'].split('-')


    def check_options(self):
            """
            Checks if arguments given are valid
            """
            print "|--------------- CHECK OPTIONS START ----------------|"
            if self.conf_opt['v']:
                print "Verbose mode on"
            if self.conf_opt['h']:
                print help()

            # Checking from and until dates
            start_date = check_date(self.conf_opt['f'], 'starting')
            end_date = check_date(self.conf_opt['t'], 'ending')
            print start_date[1] + '\r\n' + end_date[1]
            if (not start_date[0]) or (not end_date[0]):
                raise SystemExit
            print "|--------------- CHECK OPTIONS END ------------|\r\n"
     
      
    def log(self, log_line):
            str_out = ""
            log_file = self.out_files['log']
            log_file.write(log_line + '\n')
            if self.conf_opt['v']:
                str_out = str(log_line) + "\r\n"
            return str_out


if __name__ == "__main__":

    print "\r\n----SuperGraphDataCreator Start----"
    print "Please check configuration file 'graph_settings.py'\r\n"
    sg = SuperGraphData()
    sg.extract_options()
    sg.check_options()
    BD = datetime(int(sg.BD[0]), int(sg.BD[1]), int(sg.BD[2]))
    ED = datetime(int(sg.ED[0]), int(sg.ED[1]), int(sg.ED[2]))

    print "Dates: "
    print str(BD).split()[0] + " " + str(ED).split()[0]
    ED_aux = ED
    months_num = MonthsBetweenDates(BD, ED)
    months_byper = sg.conf_opt['p']
    periods = int(months_num/months_byper)

    if periods > 0:

        uncomp_months = operator.mod(months_num,months_byper)
        info = "We have " + str(periods) + " periods of "
        info += str(months_byper) + " months and a period of " 
        info += str(uncomp_months) + " months."
        print info

        less_months = str(ED_aux + relativedelta(months=-uncomp_months))
        date_less = less_months.split()[0]
        list_date = date_less.split('-')
        year_ls = int(list_date[0])
        month_ls = int(list_date[1])
        day_ls = int(list_date[2])

        ED1 = datetime(year_ls, month_ls, day_ls)
        ED2 = ED

        periods_final = datetime_range(BD, ED1, periods)

        str_date = ""
        print "Periods of " + str(months_byper) + " months: "
        for date_per in periods_final:
            for date_fin in date_per:
                str_date += str(str(date_fin).split()[0]) + " "
            print str_date
            str_date = ""

        print "Last period: "
        print str(ED1).split()[0] + " " + str(ED).split()[0]

    else:
        print "We have only one period: "
        print str(BD).split()[0] + " " + str(ED).split()[0]


