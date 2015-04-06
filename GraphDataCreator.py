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
        log_file = open("graph_log.txt", 'a')
        log_file.write(log_line + '\n')
        log_file.close()
        if verbose:
            str_out = str(log_line) + "\r\n"
        return str_out

    
    def findFittingTag(self, file_compare, ln_num, rev, author, verbose):
    
        """
        # First argument: file to compare
        # Second argument: line number
        # Third argument: rev
        # Fourth argument: author
        """

        command1 = ["grep", file_compare, "tags"]
        matches = ""
        try:
            matches = subprocess.check_output(command1)
        except subprocess.CalledProcessError:
            print "Error with ctags"
        #Case of not matching any tag
        if matches == "":
            #In this case the output has three fields (no tag)
            #log: "Adding file tag"
            fich = open("outputFile.txt", 'a')
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

                """
                lines depending on language
                case ext in cs|java|js|m|mm
                    specialExt = True
                esac
                """

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
                    log_line += "to outputFile.txt"
                    fich = open("outputFile.txt", 'a')
                    line = rev + "," + file_compare + tagToWrite + "," + author
                    fich.write(line)
                    fich.close()

                return 1
        


if __name__ == "__main__":
    my_graph = GraphData()
    # FIXME: all output files should be named here
    # FIXME: better under a "data" subdirectory
    # FIXME: all these variables should start with conf_
    commits_file = 'archivoDeCommitsDesdeScript.txt'
    
    if len(sys.argv) == 1:
        print help()
        raise SystemExit
    
    # Initialising options. FIXME: conf_ variables!
    verbose = False
    from_date = '1971-1-1'
    until_date = strftime("%Y-%m-%d", gmtime())
    unamestr = os.uname()[0]
    if unamestr != 'Linux':
        print "We are not under Linux, no options available"
        raise SystemExit

    url_repo = ""

    # Check introduced parameters
    # FIXME: change this to a dictionary!
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
        
    # FIXME: check if there is a data subdirectory as well!

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
    else:
        print "No git repo specified!"
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
    print "Executing: " + git_log

    if os.path.exists(commits_file):
        print "File of commits created succesfully"
    else:
        print "File of commits empty."
        print "Please use option -h for further information"
    
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
    print "Executing: ctags -w -R -n . >> 2&>1 > outputFile.txt"
    os.system('ctags -w -R -n . >> 2&>1 > outputFile.txt')

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
            fich_diff = open("diff.txt", 'w')
            fich_diff.write(entireDiff)
            fich_diff.close()
            to_exe = 'git checkout ' + rev
            os.system(to_exe)

            fich_diff = open("diff.txt", 'r')
            entireDiff_lines = fich_diff.readlines()
            fich_diff.close()
            
            allFiles = open("allFiles.txt", 'a')
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
            allFiles_data = open("allFiles.txt", 'r')
            allFiles_lines = allFiles_data.readlines()

            for file_line in allFiles_lines:
                print my_graph.log(verbose, "FILE: " + file_line)
                # FIXME: avoid absolute path!
                to_exe_tmp = "ctags -f AuxTagFile.txt -n /home/grex/tmp/R-SNA/Repository/"
                to_exe_tmp += file_line
                # ctags warning: can't open such file or directory
                print "Executing: " + to_exe_tmp
                os.system(to_exe_tmp)
                # remove comment lines from the just-created tag file
                rmv_cmt1 = 'perl -n -i.bak -e "print unless '
                rmv_cmt1 += '/_TAG_FILE_/" AuxTagFile.txt'
                os.system(rmv_cmt1)

                rmv_cmt2 = 'perl -n -i.bak -e "print unless '
                rmv_cmt2 += '/_TAG_PROGRAM_/" AuxTagFile.txt'
                os.system(rmv_cmt2)
