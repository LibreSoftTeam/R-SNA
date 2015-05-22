#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

# Date range to periods calculator ; 2015, LibreSoft

"""
For a given period of time (two dates), the program calculates using this 
time lapse resulting 6-month periods (if there are enough months for that) 
and one additional period to complete the given data range if necessary.
"""

#TODO: Export resulting methods in a CSV file

import time
import operator
from datetime import datetime,timedelta
from itertools import count, islice
from datetime import date
from dateutil.relativedelta import relativedelta

def datetime_range(start, end, num):
    start_secs = (start - datetime(1970, 1, 1)).total_seconds()
    end_secs = (end - datetime(1970, 1, 1)).total_seconds()
    dates = [datetime.fromtimestamp(el) 
             for el in islice(count(start_secs, 
                                    (end_secs - start_secs) / num),
                                     num + 1)]
    return zip(dates, dates[1:])

def MonthsBetweenDates(BeginDate, EndDate):
    firstyearmonths = [mn for mn in range(BeginDate.month, 13)]
    lastyearmonths = [mn for mn in range(1, EndDate.month+1)]
    months = [mn for mn in range(1, 13)]
    numofyearsbtween = EndDate.year - BeginDate.year - 1
    if BeginDate.year == EndDate.year:
        return EndDate.month - BeginDate.month
    else:
        ret = len(firstyearmonths + months * numofyearsbtween + lastyearmonths)
        return ret


BD = datetime(1998, 2, 1)
ED = datetime(1999, 5, 18)

print "Dates: "
print str(BD).split()[0] + " " + str(ED).split()[0]
ED_aux = ED
months_num = MonthsBetweenDates(BD, ED)

periods = int(months_num/6)

if periods > 0:

    uncomp_months = operator.mod(months_num,6)
    info = "We have " + str(periods) + " periods of 6 months and a period of " 
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
    print "Periods of 6 months: "
    for date_per in periods_final:
        for date_fin in date_per:
            str_date += str(str(date_fin).split()[0]) + " "
        
        print str_date
        str_date = ""

    print "Last period: "
    ED1 = ED1 + relativedelta(days=+1)
    print str(ED1).split()[0] + " " + str(ED).split()[0]

else:
    print "We have only one period: "
    print str(BD).split()[0] + " " + str(ED).split()[0]


