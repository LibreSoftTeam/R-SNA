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

    line += "\r\n\r\nDEPENDENCIES\r\n\r\nPerl, git and ctags are required to run "
    line += "this script.\r\n\r\nOUTPUT\r\n\r\n"
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
        return 0;
    else:
        return 1;


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


class GraphData:


    def __init__(self):
        
        self.DATA_PATH = "Data"
        self.out_names = {}
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
        self.conf_opt['f'] = '1971-1-1' # Starting date of study option (-f)
        self.conf_opt['t'] = self.date_now # Ending date opt. (-t)
        self.conf_opt['r'] = "" # Repository URL option (-r)
        self.conf_opt['h'] = False  # Show help option (-h)

    def log(self, verbose, log_line):
        str_out = ""
        log_file = open("log_file", 'a')
        log_file.write(log_line + '\n')
        log_file.close()
        if verbose:
            str_out = str(log_line) + "\r\n"
        return str_out

    def create_data_files(self):
            os.mkdir(self.DATA_PATH)
            os.mkdir(self.DATA_PATH + "/tags")
            for out_file in self.out_names.keys():
                dir_to_open = self.DATA_PATH + '/' + self.out_names[out_file]
                self.out_files[out_file] = open(dir_to_open, 'a')

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

    def findFittingTag(self, file_compare, ln_num, rev, author, verbose):
    
        """
        # First argument: file to compare
        # Second argument: line number
        # Third argument: rev
        # Fourth argument: author
        """

        command1 = ["grep", file_compare, "tags"]
        """
        matches = ""
        try:
            matches = subprocess.check_output(command1)
        except subprocess.CalledProcessError:
            print "Error with ctags"
        #Case of not matching any tag
        if matches == "":
            #In this case the output has three fields (no tag)
            #log: "Adding file tag"
            fich = open("output_file", 'a')
            line = rev + "," + file_compare + "," + author
            fich.write(line)
            fich.close()
        else:
            fittingLine = ""
            bestNumber = ""

            # This While loop calculates the method where the line number
            # received belongs to

            matches_lines = matches.split('\n')
            for match_line in matches_lines:
                
                command2 = ["echo", match_line, "|", "awk", "print  " + ln_num]
                fMatch = subprocess.check_output(command2)
                
                command3 = ["echo", fMatch, "|", "sed", "'s/*\.//'"]
                ext = subprocess.check_output(command3)

                specialExt = False

                ###
                lines depending on language
                case ext in cs|java|js|m|mm
                    specialExt = True
                esac
                ###

                # Fourth parameter in tags file holds the type of tag
                parameters = match_line.split()
                isAFunction = parameters[3]
                # Take #4 parameter, which is type of method in tags
                condition1 = specialExt and (isAFunction == 'm')
                condition2 = not specialExt and (isAFunction == 'f')
                if (condition1 or condition2):
                    log_line = "We are in a function-> f: "
                    log_line += fMatch + "ext: " + ext 
                    log_line += "Spec: " + specialExt + "tag: " + isAFunction
                    print self.log(verbose, log_line)
                    
                    # Removing two last chars from third field to get the line number
                    LineNumber = parameters[3][:-2]
                    
                    # Case of methods matching 
                    if fittingLine == "":
                        if lineNumber > ln_num:
                            fittingLine = match_line
                            bestNumber = lineNumber
                    else:
                        if ((lineNumber > ln_num) and (lineNumber < bestNumber)):
                            fittingLine = match_line
                            bestNumber = lineNumber

                # Not sure of this
                if fittingLine != "":
                    log_line = "..and fitting line has been: " + fittingLine
                    print self.log(verbose, log_line)
                    tagToWrite = fittingLine.split()[0]

                    # Adding tag to output file
                    log_line = "Adding " + file_compare + tagToWrite
                    log_line += "to output_file"
                    fich = open("output_file", 'a')
                    line = rev + "," + file_compare + tagToWrite + "," + author
                    fich.write(line)
                    fich.close()
                """

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
    # Checking existance of Repository; we need it!
    my_graph.check_program_starting()
    my_graph.create_data_files()

    # Check introduced parameters
    my_graph.check_options()

    # First: git clone: project as a parameter
    # -------- git clone url folder-name ----------------
    my_graph.download_repo()
    
    my_graph.extract_git_log()
    print "Break-point"
    raise SystemExit

    # Now we read the first line of the file with the commit revs

    print "Reading first line and checking out from first commit"

    fich = open(commits_file, 'r')
    commit_lines = fich.readlines()
    if len(commit_lines) == 0:
        print "Empty commits file"
        raise SystemExit

    start_line = commit_lines[0]
    fich.close()
    print my_graph.log(verbose, "First line: " + start_line)

    to_exe = 'git checkout -f ' + start_line.split()[1]
    print "Executing: " + to_exe
    os.system(to_exe)
        
    print  "Creating tags file: tags"
    # Do this if ctags does not exist, otherwise just update it
    # Getting rid of annoying warning output
    print "Executing: ctags -w -R -n . >> 2&>1 > output_file"
    os.system('ctags -w -R -n . >> 2&>1 > output_file')

    # From 'archivoDeCommitsDesdeScript.txt' file
    # get file and line of change,
    # and then get tag, we have to update

    fich = open(commits_file, 'r')
    commit_lines = " ".join(fich.readlines())
    commit_lines = commit_lines.split("commit ")
    rev = ""
    author = ""
    file1 = ""
    lineNumber1 = ""
    for line in commit_lines:
        if line != "":
            # Extracting info: commit-id and author
            print my_graph.log(verbose, "NEW LINE: " + line)
            line = line.split()
            rev = line[0]
            line = " ".join(line[1:])
            line = line.split("Date")
            line = line[0].split()
            author = line[1]

            print my_graph.log(verbose, "Author: " + author)
            to_exe = ['git','diff', '--unified=0', rev + "^!"]
            entireDiff = subprocess.check_output(to_exe)
            fich_diff = open("diff_file", 'w')
            fich_diff.write(entireDiff)
            fich_diff.close()
            to_exe = 'git checkout ' + rev
            os.system(to_exe)

            fich_diff = open("diff_file", 'r')
            entireDiff_lines = fich_diff.readlines()
            fich_diff.close()
            
            allFiles = open("allFiles_file", 'a')
            for grepline in entireDiff_lines:
      ### Getting rid of all lines we dont care about
      ### We only want this when we don't need to read the output of git diff, 
      ### but only the files modified ###   

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
                        print my_graph.log(verbose, "File: " + file1)
    
                    if lineNumber1 == "":
                        # When grep is empty, we add a tag -> 
                        # it will be a file-to-file collaboration
                        lastFile2 = file1
                        out1 = my_graph.findFittingTag(lastFile2, lineNumber1,
                                                rev, author, verbose)
                        #Value of lastFile2 in other case?

            print "Tag and committer added to output file"
            print "Now updating ctags file"
            ## HERE UPDATING TAGS FILE WITH TAGS OF MODIFIED FILES

            allFiles.close()
            allFiles_data = open("allFiles_file", 'r')
            allFiles_lines = allFiles_data.readlines()

            for file_line in allFiles_lines:
                print my_graph.log(verbose, "FILE: " + file_line)
                # FIXME: avoid absolute path!
                to_exe_tmp = "ctags -f auxTags_file -n /Data/ctags"
                to_exe_tmp += file_line
                # ctags warning: can't open such file or directory
                print "Executing: " + to_exe_tmp
                os.system(to_exe_tmp)
                # remove comment lines from the just-created tag file
                rmv_cmt1 = 'perl -n -i.bak -e "print unless '
                rmv_cmt1 += '/_TAG_FILE_/" auxTags_file'
                os.system(rmv_cmt1)

                rmv_cmt2 = 'perl -n -i.bak -e "print unless '
                rmv_cmt2 += '/_TAG_PROGRAM_/" auxTags_file'
                os.system(rmv_cmt2)
