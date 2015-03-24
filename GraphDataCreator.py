#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
GraphDataCreator Shell(bash)-to-Pyhton translation from Christian Ramiro code
Miguel Angel Fernandez Sanchez
"""

import os
import sys
from time import strftime, gmtime

print " - Graph Data Creator Started - "
print " - MAKE SURE CTAGS, PERL AND GIT ARE INSTALLED IN YOUR COMPUTER\r\n"


def help():
    """
        Prints usage & description
    """
    line = "\r\nNAME\r\n\r\nGraphDataCreator.sh\r\n\r\n"
    line += "USAGE\r\n\r\n./GrahDataCreator [SHORT-OPTION]\r\n\r\n"
    line += "EXAMPLE\r\n\r\n"
    line += "./GraphDataCreator.sh -f 2010-1-1 -t 2011-1-1 -r "
    line += "git://git.openstack.org/openstack/swift -v\r\n\r\n"

    line += "DESCRIPTION\r\n\r\n"
    line += "GraphDataCreator.sh reads information of a Git repository and"
    line += " outputs two\n.csv files ready to be read to represent"
    line += " a software community. The files\ncontain pairs "
    line += "developer-developer meaning that both developers have\nworked "
    line += "together. One file uses file-scope to create a relationship "
    line += "while\nthe other narrows relationship down using"
    line += " a method-scope.\r\n"

    line += "\r\nOPTIONS\r\n\r\n-h\tPrints help page.\r\n\r\n"
    line += "-f\tStarting date of study. When empty, study start "
    line += "the beginning of times.\n\tFormat: 2012-12-31\r\n\r\n"
    line += "-t\tEnding date of study. When empty, current date will "
    line += "be chosen.\n\tFormat: 2012-12-31\r\n\r\n"
    line += "-r\tRepository url. When empty, we assume we are "
    line += "in a directory tracked by Git. \n\tExample: "
    line += "git://git.openstack.org/openstack/swift\r\n"
    line += "\r\n-v\tVerbose mode."

    line += "\r\n\r\nDEPENDENCIES\r\n\r\nPerl, Git and Ctags need to run "
    line += "this script.\r\n\r\nOUTPUT\r\n\r\n"
    line += "DataMethods.csv-File using relationship-in-method approach\r\n"
    line += "DataFiles.csv-File using relantionship-in-file approach\r\n"
    return line


def check_date(date):
    """
    Checks if a date has format 'YYYY-MM-DD'
    """
    date = str(date)
    date_fields = date.split('-')
    ans = 0
    if len(date_fields) == 3:
        if date_fields[0] >= 1971:
            if (int(date_fields[1]) > 0) and (int(date_fields[1]) < 13):
                if (int(date_fields[2]) > 0) and (int(date_fields[2]) < 32):
                    ans = 1
    return ans


class GraphData:

    def log(self, verbose, log_line):
        str_out = ""
        if verbose:
            str_out = str(log_line) + "\r\n"
        return str_out


if __name__ == "__main__":
    my_graph = GraphData()
    commits_file = 'archivoDeCommitsDesdeScript.txt'
    
    # Initialising options
    verbose = False
    from_date = '1971-1-1'
    until_date = strftime("%Y-%m-%d", gmtime())
    unamestr = os.uname()[0]
    if unamestr != 'Linux':
        print "We are not under Linux, no options available"
        raise SystemExit

    url_repo = ""

    # Check introduced paramenters
    user_param = " ".join(sys.argv)
    list_param = user_param.split(" -")
    for value in list_param:
        value_tmp = value.split()
        if len(value_tmp) == 2:
            if value_tmp[0] == 'f':
                from_date = value_tmp[1]
            elif value_tmp[0] == 't':
                until_date = value_tmp[1]
            elif value_tmp[0] == 'r':
                url_repo = value_tmp[1]
        else:
            if value == 'v':
                verbose = True
                print "Verbose mode on"
            elif value == 'h':
                print help()

    # Checking existance of Repository; we need it!
    if os.path.exists("Repository"):
        print "Please, remove directory 'Repository' before starting"
        raise SystemExit

    # Checking from and until dates
    if check_date(from_date):
        print "Valid starting date: " + from_date
    else:
        print "Starting date is wrong. "
        print "Please use option -h for further information"
        raise SystemExit

    if check_date(until_date):
        print "Valid ending date: " + until_date
    else:
        print "Ending date is wrong. "
        print "Please use option -h for further information"
        raise SystemExit

    if url_repo != "":
        print "Starting download of Repository"
        to_exe = "git clone " + url_repo + " Repository"
        os.system(to_exe)
        dwnl_error = False
        if not dwnl_error:
            print "Repository downloaded succesfully"
            os.chdir("Repository")
            os.system("pwd")
        else:
            print "Error downloading Repository"
            raise SystemExit


    if not os.path.exists(".git"):
        print "No Git repository found."
        print "Please use option -h for further information."
        raise SystemExit

    # First: git clone: project as a parameter
    # -------- git clone url folder-name ----------------

    git_log = 'git log --all --since=' + str(from_date) + ' --until='
    git_log += str(until_date) + '--pretty=format:"%H &an" > '
    git_log += commits_file
    os.system(git_log)

    if os.path.exists(commits_file):
        print "File of commits created succesfully"
    else:
        print "File of commits empty."
        print "Please use option -h for further information"
    
    # Now we read the first line of the file with the commit revs

    print "Reading first line and checking out from first commit"

    fich = open(commits_file, 'r')
    start_line = fich.readlines()[0]
    fich.close()
    print my_graph.log(verbose, start_line)

    to_exe = 'git checkout -f ' + start_line
    

    
