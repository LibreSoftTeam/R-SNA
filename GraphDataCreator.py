#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
GraphDataCreator Shell(bash)-to-Pyhton translation from Christian Ramiro code
Miguel Angel Fernandez Sanchez
"""

import os
import sys
from time import strftime, gmtime
import subprocess

print " - Graph Data Creator Started - "
print " - MAKE SURE CTAGS, PERL AND GIT ARE INSTALLED IN YOUR COMPUTER\r\n"

INIT_PATH = os.path.abspath(os.curdir)


def help():
    """
        Prints usage & description
    """
    line = "\r\nNAME\r\n\r\nGraphDataCreator.py\r\n\r\n"
    line += "USAGE\r\n\r\n./GrahDataCreator.py [SHORT-OPTION]\r\n\r\n"
    line += "EXAMPLE\r\n\r\n"
    line += "./GraphDataCreator.py -f 2010-1-1 -t 2011-1-1 -r "
    line += "git://git.openstack.org/openstack/swift -v\r\n\r\n"

    line += "DESCRIPTION\r\n\r\n"
    line += "GraphDataCreator.py reads information of a Git repository and"
    line += " outputs two\nCSV files ready to be read to represent"
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
    line += "-r\tRepository URL. When empty, we assume we are "
    line += "in a directory tracked by Git. \n\tExample: "
    line += "git://git.openstack.org/openstack/swift\r\n"
    line += "\r\n-v\tVerbose mode."

    line += "\r\n\r\nDEPENDENCIES\r\n\r\nPerl, git and ctags are required "
    line += "to run this script.\r\n\r\nOUTPUT\r\n\r\n"
    line += "DataMethods.csv-File using relationship-in-method approach\r\n"
    line += "DataFiles.csv-File using relantionship-in-file approach\r\n"
    return line


def error_info(show_line):
    return show_line


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


def under_linux():
    """
    Checks if we are working on a GNU/Linux distribution
    """

    unamestr = os.uname()[0]
    if unamestr != 'Linux':
        print "We are not under Linux, no options available"
        return 0
    else:
        return 1


def extract_options(list_opt, dicc_opt):
    """
    Extracts data from program arguments and fills a dictionary
        # Verbose option (-v)
        # Starting date of study option (-f)
        # Ending date option (-t)
        # Repository URL option (-r)
        # Show help option (-h)
    """
    user_param = " ".join(list_opt)
    list_param = user_param.split(" -")
    for value in list_param:
        value_tmp = value.split()
        if len(value_tmp) == 2:
            if value_tmp[0] == "f":
                dicc_opt['f'] = str(value_tmp[1])
            elif value_tmp[0] == "t":
                dicc_opt['t'] = str(value_tmp[1])
            elif value_tmp[0] == "r":
                dicc_opt['r'] = str(value_tmp[1])
        else:
            if value == 'v':
                dicc_opt['v'] = True
            elif value == 'h':
                dicc_opt['h'] = True


def dir_exists(directory):
    """
    Checks if a directory exists
    """
    if os.path.exists(directory):
        print "Please, remove directory '" + directory + "' before starting"
        return 1
    else:
        return 0


def go_home_dir():
    """
    Goes back in current path to home directory
    """
    init_list = INIT_PATH.split('/')
    cur_dir = os.path.abspath(os.curdir)
    list_dir = cur_dir.split('/')
    exceeds = len(list_dir) - len(init_list)
    if exceeds > 0:
        print "Going up " + str(exceeds) + " directory levels"
        for i in range(exceeds):
            os.chdir('..')


class GraphData:

    def __init__(self):

        self.DATA_PATH = "Data"
        self.CHECKOUT_PATH = self.DATA_PATH + '/' + 'Repository'
        self.out_names = {}
        self.out_paths = {}
        self.out_files = {}

        self.out_names['commits'] = "CommitsFromScriptFile.txt"
        self.out_names['output'] = "outputFile.txt"
        self.out_names['log'] = "graphData.log"
        self.out_names['diff'] = "diffFile.txt"
        self.out_names['allFiles'] = "allFiles.txt"
        self.out_names['auxTag'] = "AuxTagFile.txt"

        self.date_now = strftime("%Y-%m-%d", gmtime())
        self.conf_opt = {}
        self.conf_opt['v'] = True  # Verbose option (-v)
        self.conf_opt['f'] = '1971-1-1'  # Starting date of study option (-f)
        self.conf_opt['t'] = self.date_now  # Ending date opt. (-t)
        self.conf_opt['r'] = ""  # Repository URL option (-r)
        self.conf_opt['h'] = False  # Show help option (-h)

    def create_data_files(self):
            os.mkdir(self.DATA_PATH)
            os.mkdir(self.CHECKOUT_PATH)
            for out_file in self.out_names.keys():
                dir_to_open = self.DATA_PATH + '/' + self.out_names[out_file]
                self.out_paths[out_file] = dir_to_open
                self.out_files[out_file] = open(dir_to_open, 'a')

    def log(self, log_line):
        str_out = ""
        log_file = self.out_files['log']
        log_file.write(log_line + '\n')
        if self.conf_opt['v']:
            str_out = str(log_line) + "\r\n"
        return str_out

    def check_program_starting(self):
        """
        Checks if program can run properly
        """
        if not under_linux():
            raise SystemExit

        if len(sys.argv) == 1:
            print help()
            raise SystemExit

        if (dir_exists("Data")) or (dir_exists("Repository")):
            raise SystemExit

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

    def download_repo(self):
        if self.conf_opt['r'] != "":
            print "|------------ REPO DOWNLOAD START ---------------|"
            print "Starting download of Repository"
            to_exe = "git clone " + self.conf_opt['r'] + " Repository"
            os.system(to_exe)
        else:
            print "No git repo specified!"
            raise SystemExit

        print "Current path: " + os.path.abspath(os.curdir)
        os.chdir("Repository")
        print "Change path to: " + os.path.abspath(os.curdir)
        if not os.path.exists(".git"):
            print "No Git repository found."
            print "Please use option -h for further information."
            raise SystemExit
        else:
            print "Repository downloaded succesfully"
            print "|-------------- REPO DOWNLOAD END --------------|\r\n"
            os.chdir("..")
            print "Going back to directory: " + os.path.abspath(os.curdir)

    def extract_git_log(self):

        print "|--------------- GIT LOG START -----------------|"
        commits_dir = "../" + self.DATA_PATH + "/" + self.out_names['commits']
        os.chdir("Repository")
        git_log = 'git log --all --since=' + self.conf_opt['f'] + ' --until='
        git_log += self.conf_opt['t'] + '--pretty=format:"%H &an" > '
        git_log += commits_dir
        print "Executing: " + git_log
        os.system(git_log)
        os.chdir("../Data")

        self.out_files['commits'].close()
        self.out_files['commits'] = open(self.out_names['commits'], 'r')
        file_content = self.out_files['commits'].readlines()

        if file_content != []:
            print "File of commits filled succesfully"
            os.chdir("..")
        else:
            print "File of commits empty."
            print "Please use option -h for further information"
            raise SystemExit

        print "|---------------- GIT LOG END --------------|\r\n"
        return file_content

    def copy_repo(self, path_cp):
        """
        Copies Repository directory (to prevent unwanted changes)
        into specified path
        """
        print "|---------------- COPY REPO START --------------|\r\n"
        go_home_dir()
        os.system("chmod 755 Repository")
        copy_file = 'cp -r Repository ' + path_cp
        print "Copying: " + copy_file
        os.system(copy_file)
        print "|---------------- COPY REPO END --------------|\r\n"

    def do_checkout(self, rev):
        """
        Creates a directory (if it doesnt't exist yet)
        where do a checkout with specified rev
        """
        print "|---------------- GIT CHEKOUT START --------------|\r\n"
        dir_co = my_graph.CHECKOUT_PATH
        go_home_dir()
        os.chdir(dir_co)
        to_exe = 'git checkout -f ' + rev
        print "Executing: " + to_exe
        os.system(to_exe)
        go_home_dir()
        print "|---------------- GIT CHECKOUT END --------------|\r\n"

    def do_diff(self, rev):
        """
        Does git diff from specified rev
        """
        print "|---------------- GIT DIFF START --------------|\r\n"
        go_home_dir()
        os.chdir(self.CHECKOUT_PATH)
        to_exe = ['git', 'diff', '--unified=0', rev + "^!"]
        entireDiff = subprocess.check_output(to_exe)
        go_home_dir()
        diff_path = self.DATA_PATH + '/' + self.out_names['diff']
        self.out_files['diff'].close()
        self.out_files['diff'] = open(diff_path, 'w')
        self.out_files['diff'].write(entireDiff)
        self.out_files['diff'].close()
        self.out_files['diff'] = open(diff_path, 'r')
        resultDiff = self.out_files['diff'].readlines()
        self.out_files['diff'].close()
        print "|---------------- GIT DIFF END --------------|\r\n"
        return resultDiff

    def create_tags_file(self):
        """
        Creates tags file with ctags if it doesn't exist,
        otherwise just update it.
        """
        os.chdir(my_graph.CHECKOUT_PATH)
        print "Executing: ctags -w -R -n . >> 2&>1"
        #Getting rid of annoying warning output with options in command
        os.system('ctags -w -R -n . >> 2&>1')
        go_home_dir()

    def extract_rev_auth(self, line_to_extract):
        """
        Extracts from a commit-file line rev and author
        """
        line = line_to_extract.split()
        rev = line[0]
        line = " ".join(line[1:])
        line = line.split("Date")
        line = line[0].split()
        author = line[1]
        return [rev, author]

    def findFittingTag(self, file_compare, ln_num, rev, author):

        """
        # First argument: file to compare
        # Second argument: line number
        # Third argument: rev
        # Fourth argument: author
        """

        command1 = ["grep", file_compare, "tags"]
        return 1


if __name__ == "__main__":
    # FIXME: all output files should be named here // Done
    # FIXME: better under a "data" subdirectory // Done
    # FIXME: all these variables should start with conf_ // Done (Dictionary)
    # Initialising options. FIXME: conf_ variables! // Done
    # FIXME: check if there is a data subdirectory as well! // Done

    # Instance of Graph class
    my_graph = GraphData()

    extract_options(sys.argv, my_graph.conf_opt)
    my_graph.check_program_starting()
    my_graph.create_data_files()

    my_graph.check_options()
    my_graph.download_repo()

    print my_graph.log("Reading first line and checking out from first commit")
    commit_lines = my_graph.extract_git_log()

    start_line = commit_lines[0]
    print my_graph.log("First line: " + start_line)
    rev1 = start_line.split()[1]
    print my_graph.log("First checkout")

    my_graph.copy_repo(my_graph.DATA_PATH)
    my_graph.do_checkout(rev1)

    my_graph.log("Creating tags file: tags")
    my_graph.create_tags_file()

    # From 'archivoDeCommitsDesdeScript.txt' file
    # get file and line of change,
    # and then get tag, we have to update

    commit_lines_format = " ".join(commit_lines)
    commit_lines_format = commit_lines_format.split("commit ")

    # Initial asignment for in-loop variables
    rev = ""
    author = ""
    file1 = ""
    lineNumber1 = ""

    for line in commit_lines_format:
        if line != "":
            # Extracting info: commit-id and author
            #print my_graph.log("NEW LINE: " + line)
            rev_author = my_graph.extract_rev_auth(line)

            print my_graph.log("Rev: " + rev_author[0])
            print my_graph.log("Author: " + rev_author[1])

            outdiff = my_graph.do_diff(rev_author[0])
            my_graph.do_checkout(rev_author[0])

            ### Getting rid of all lines we dont care about
            ### We only want this when we don't need to read
            ### the output of git diff, but only the files modified ###

            allFiles = my_graph.out_files['allFiles']
            for grepline in outdiff:
                if grepline[0] != '+' and grepline[0] != '-':
                    grepline_data = grepline.split()
                    if grepline_data[0] == "diff":
                        for data in grepline_data:
                            if (data[0] == 'b') and (data[1] == '/'):
                                file1 = data[2:]
                                allFiles.write(file1 + '\n')
                    elif grepline_data[0] == "@@":
                        for data in grepline_data:
                            if data[0] == "+":
                                lineNumber1 = data[1:]

                    if file1 == "":
                        lastFile2 = file1
                        print my_graph.log("File: " + file1)

                    if lineNumber1 == "":
                        # When grep is empty, we add a tag ->
                        # it will be a file-to-file collaboration
                        lastFile2 = file1
                        out1 = my_graph.findFittingTag(lastFile2, lineNumber1,
                                                       rev, author)
