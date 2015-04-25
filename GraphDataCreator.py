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
import shutil
import commands

print " - Graph Data Creator Started - "
print " - MAKE SURE CTAGS AND GIT ARE INSTALLED IN YOUR COMPUTER\r\n"

INIT_PATH = os.path.abspath(os.curdir)


def help():
    """
        prints usage & description
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

    line += "\r\nOPTIONS\r\n\r\n-h\tprints help page.\r\n\r\n"
    line += "-f\tStarting date of study. When empty, study start "
    line += "the beginning of times.\n\tFormat: 2012-12-31\r\n\r\n"
    line += "-t\tEnding date of study. When empty, current date will "
    line += "be chosen.\n\tFormat: 2012-12-31\r\n\r\n"
    line += "-r\tRepository URL. When empty, we assume we are "
    line += "in a directory tracked by Git. \n\tExample: "
    line += "git://git.openstack.org/openstack/swift\r\n"
    line += "\r\n-v\tVerbose mode."

    line += "\r\n\r\nDEPENDENCIES\r\n\r\nGit and ctags are required "
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
        print "Do you want to remove directory '" + directory + "'? (Y / n)"
        ans = raw_input()
        if (ans == 'Y') or (ans == 'y'):
            print "Removing directory: " + directory
            shutil.rmtree(directory, ignore_errors=True)
            out = 0
        else:
            out = 1
    else:
        out = 0
    return out


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


def add_backslash(line):
    line2 = ""
    for char in line:
        if char == '/':
            line2 += '\\' + char
        else:
            line2 += char
    return line2

class GraphData:

    def __init__(self):

        self.DATA_PATH = "Data"
        self.OUT_PATH = self.DATA_PATH + '/' + 'output'
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
            os.mkdir(self.OUT_PATH)
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

        if (dir_exists("Repository")) or (dir_exists("Data")):
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
        status_checkout, checkout_did = commands.getstatusoutput(to_exe)
        print self.log(checkout_did)
        go_home_dir()
        print "|---------------- GIT CHECKOUT END --------------|\r\n"

    def do_diff(self, rev):
        """
        Does git diff from specified rev
        """
        print "|---------------- GIT DIFF START --------------|\r\n"
        go_home_dir()
        os.chdir(self.CHECKOUT_PATH)
        to_exe = 'git diff --unified=0 ' + rev + '^!'
        status_diff, entireDiff = commands.getstatusoutput(to_exe)
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
        os.chdir(self.CHECKOUT_PATH)
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
        
        print self.log("Line extract: " + line)
        line = line.split("<")
        author = line[0].split('Author: ')[1]
        print self.log("Author function: " + author)
        return [rev, author]

    def grepline_info(self, grepline):
        """
        Extracts file name and/or a line number from a line of diff.txt
        """
        file1 = ""
        lineNumber1 = ""
        if grepline[0] != '+' and grepline[0] != '-':
                grepline_data = grepline.split()
                if grepline_data[0] == "diff":
                    for data in grepline_data:
                        if (data[0] == 'b') and (data[1] == '/'):
                            file1 = data[2:]
                elif grepline_data[0] == "@@":
                    for data in grepline_data:
                        if data[0] == "+":
                            num = data.split(',')
                            lineNumber1 = num[0][1:]
        return [file1, lineNumber1]
    
    def extract_file_names(self, diff):
        file_names = []
        fich = self.out_files['allFiles']
        for line in diff:
            if line != "":
                line_list = line.split()
                if len(line_list) > 2:
                    cond1 = line_list[0] == 'diff'
                    cond2 = line_list[1] == '--git'
                    if cond1 and cond2:
                        fname = line_list[3]
                        file_names.append(fname[2:])
                        fich.write(fname[2:])
                        
        return file_names
                        
    def rm_comment_lines(self, file_name):
        """
        Removes unnecessary lines from a tag file
        (/_TAG_FILE_/ and /_TAG_PROGRAM_/ or
        !_TAG_FILE_/ and !_TAG_PROGRAM_/ lines)
        """
        op1 = "!_TAG_"
        op2 = "/_TAG_"
        fich = open(file_name, 'r')
        lines = fich.readlines()
        fich.close()
        lines_ok = []
        for line in lines:
            line_list1 = line.split(op1)
            line_list2 = line.split(op2)
            if not ((len(line_list1) > 1) or (len(line_list2) > 1)):
                lines_ok.append(line)
        fich = open(file_name, 'w')

        for new_line in lines_ok:
            fich.write(new_line)
        fich.close
        return lines_ok

    def print_unless(self, text, file_name):
        # FIXME: Add function description

        fich = open(file_name, 'r')
        lines = fich.readlines()
        fich.close()
        lines_ok = []
        for line in lines:
            line_list = line.split(text)
            if not (len(line_list) > 1):
                lines_ok.append(line)
        fich = open(file_name, 'w')
        for new_line in lines_ok:
            fich.write(new_line)
        fich.close
        return lines_ok

    def findFittingTag(self, file_compare, ln_num, rev, author):

        """
        # First argument: file to compare
        # Second argument: line number
        # Third argument: rev
        # Fourth argument: author
        """
        print self.log("|------------ FIND FITTING TAG START ----------|")
        print self.log("Param: " + file_compare + ", " + ln_num + ", " + rev + ", " + author)
        go_home_dir()
        os.chdir(self.CHECKOUT_PATH)
        matches = ""
        file_list = os.listdir(os.curdir)
        fich = self.out_files['output']
        
        if file_compare in file_list:
            command1 = "grep " + file_compare + " tags"
            print self.log("Executing: " + command1)
            status, matches = commands.getstatusoutput(command1)
        #Case of not matching any tag
        if matches == "":
            #In this case the output has three fields (no tag)
            print self.log("Adding file tag")
            print "Linea vacia"
            line = rev + "," + file_compare + "," + author
            fich.write(line + '\n')
            #? Even if file isn't in folder?
        else:
            
            fittingLine = ""
            bestNumber = ""
            # This While loop calculates the method where the line number
            # received belongs to


            matches_lines = matches.split('\n')
            for match_line in matches_lines:
                if match_line != "":
                    match_list = match_line.split()
                    # We have a line like this: AUDIO_FILE uaserver.py 26;" v
                    fMatch = match_list[1]
                    ext = match_list[1].split('.')[-1]
                    specialExt = False
                    
                    # Depending on language
                    spc_ext = ['cs', 'java', 'js', 'm', 'mm']
                    if ext in spc_ext:
                        specialExt = True

                    # Fourth parameter in tags file holds the type of tag
                    isAFunction = match_list[3]

                    # Take #4 parameter, which is type of method in tags
                    condition1 = specialExt and (isAFunction == 'm')
                    condition2 = not specialExt and (isAFunction == 'f')
                    if (condition1 or condition2):

                        log_line = "We are in a function-> f: "
                        log_line += fMatch + "ext: " + ext
                        log_line += "Spec: " + str(specialExt) + " tag: " + str(isAFunction)
                        print self.log(log_line)
                        # Removing two last chars from third field to get the line number
                        lineNumber = match_list[2][:-2]
                        
                        # Case of methods matching 
                        if fittingLine == "":
                            if lineNumber > ln_num:
                                fittingLine = match_line
                                bestNumber = lineNumber
                        else:
                            if ((lineNumber > ln_num) and (lineNumber < bestNumber)):
                                fittingLine = match_line
                                bestNumber = lineNumber
                     

            log_line = "..and fitting line has been: " + fittingLine
            print self.log(log_line)
            if fittingLine != "":
                tagToWrite = fittingLine.split()[0]
            else:
                tagToWrite = ""

            # Adding tag to output file
            fichtag = open('fichtag.log', 'a')
            fichtag.write("Tag-to-write: " + tagToWrite + "\n")
            fichtag.close()
            log_line = "Adding " + file_compare + ' ' + tagToWrite
            log_line += "to output_file"
            line = rev + "," + file_compare + ' ' + tagToWrite + "," + author
            fich.write(line + '\n')
            print self.log(log_line)

            go_home_dir()

        print self.log("|------------ FIND FITTING TAG END ----------|\r\n")
        print "|------------ FIND FITTING TAG END ----------|\r\n"
        return 1


if __name__ == "__main__":

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

    # FIXME: From here, this has to be divided in smaller functions
    for line in commit_lines_format:
        if line != "":
            # Extracting info: commit-id and author
            print my_graph.log("NEW LINE: " + line)
            rev_author = my_graph.extract_rev_auth(line)

            print my_graph.log("Rev: " + rev_author[0])
            print my_graph.log("Author: " + rev_author[1])

            outdiff = my_graph.do_diff(rev_author[0])
            my_graph.do_checkout(rev_author[0])

            lastFile2 = ""
            allFiles = my_graph.out_files['allFiles']
            for grepline in outdiff:
               lineNumber1 = ""

               if grepline[0] != '+' and grepline[0] != '-':
                grepline_data = grepline.split()
                if (grepline_data[0] == "diff"):
                    if grepline_data[1] == "--git":
                        for data in grepline_data:
                            if (data[0] == 'b') and (data[1] == '/'):
                                file1 = data[2:]
                elif grepline_data[0] == "@@":
                    for data in grepline_data:
                        if data[0] == "+":
                            num = data.split(',')
                            lineNumber1 = num[0][1:]
                if file1 != "":
                    print my_graph.log("File: " + file1)
                    lastFile2 = file1
                if lineNumber1 != "":
                    # When grep is empty, we add a tag ->
                    # it will be a file-to-file collaboration
                    print my_graph.log("Line number: " + lineNumber1)
                    
                    out1 = my_graph.findFittingTag(lastFile2, lineNumber1,
                                                   rev_author[0], 
                                                   rev_author[1])

            # FIXME: This has to be in allFiles.txt also

            print my_graph.log("Tag and committer added to output file")
            print my_graph.log("Now updating ctags file")
            ## HERE UPDATING TAGS FILE WITH TAGS OF MODIFIED FILES
            all_files = my_graph.extract_file_names(outdiff)
            go_home_dir()
            os.chdir(my_graph.CHECKOUT_PATH)
            current_files = os.listdir(os.curdir)

            for fileModifiedTag in all_files:
                if fileModifiedTag in current_files:
                    print my_graph.log("FILE: " + fileModifiedTag)
                    upd_ctags = "ctags -f " + my_graph.out_names['auxTag']
                    upd_ctags += " -n " + fileModifiedTag
                    print my_graph.log("Executing: " + upd_ctags)
                    os.system(upd_ctags)
                    # remove comment lines from the just-created tag file
                    auxTag_nm = my_graph.out_names['auxTag']
                    lines_ok = my_graph.print_unless("!_TAG_", auxTag_nm)
                    lines_ok = my_graph.print_unless("/_TAG_", auxTag_nm)
                    # remove lines of that file in tags file
                    # adding backslash to scape slash before removing
                    second = add_backslash(fileModifiedTag)
                    print my_graph.log("second: " + str(second))
                    clean_lines = my_graph.print_unless(second, 'tags')
                    # FIXME: Some log lines not added yet
                    #add new lines
                    fich_tags = open('tags', 'a')
                    for line_ok in lines_ok:
                        fich_tags.write(line_ok)
                    fich_tags.close()
                    info = "Tags added to tags file: now is up to date"
                    print my_graph.log(info)

    info = "Starting to create data files -methods and files-"
    print my_graph.log(info)
    go_home_dir()
    my_graph.out_files['output'].close()
    os.chdir(my_graph.DATA_PATH)
    outp_name = my_graph.out_names['output']
    outpfile = open(outp_name, 'r')
    
    outp_lines = outpfile.readlines()
    outpfile.close()  

    dm_file = open('DataMethods.csv', 'a')
    df_file = open('DataFiles.csv', 'a')
    
    for oLine in outp_lines:
        # Extracting all relevant data
        
        oLine_data = oLine.split(',')
        print my_graph.log(str(oLine_data))
        oRev = oLine_data[0]
        oTag = oLine_data[1]
        oCommitter = oLine_data[2]
        oComm_prop = ""
        for letter in oCommitter:
            if (letter != " ") and (letter != '\n'):
                oComm_prop += letter
        oCommitter = oComm_prop
                
        oTag_data = oTag.split()

        if len(oTag_data) == 2:
            oFile = oTag_data[0]
            oMethod = oTag_data[1]
        else:
            oFile = oTag_data[0]
            oMethod = ""
        print "oFile: " + oFile
        print my_graph.log("Committer: " + oCommitter)

        # Array of committers to avoid repetitions
        listCommitters = []

        # Grepping lines with same method
        print my_graph.log("Grepping for " + oFile)
        
        grep_command = 'grep "' + oFile + '" ' + outp_name
        print my_graph.log("Grepping for " + oFile)

        status, grep_output = commands.getstatusoutput(grep_command)
        grep_outf = open("grep_outf.txt", 'w')
        grep_outf.write(grep_output)
        grep_outf.close()
        grep_outf = open("grep_outf.txt", 'r')
        grep_outlist = grep_outf.readlines()

        for gLine in grep_outlist:
            grepline_data = gLine.split(',')
            iComm_prop = ""
            iCommitter = grepline_data[2][:-1]
            for letter in iCommitter:
                if (letter != " ") and (letter != '\n'):
                    iComm_prop += letter
            iCommitter = iComm_prop
            iTag = grepline_data[1]
            iTag_data = iTag.split()
            if len(iTag_data) == 2:
                iMethod = iTag_data[1]
            else:
                iMethod = ""

            # If Committer is not in the list
            log_line =  "File " + oFile + " and Method " + iMethod
            log_line += " of Committer " + iCommitter
            print my_graph.log(log_line)
            if iCommitter not in listCommitters:
                if (oCommitter != iCommitter) and ((iCommitter != "") and (oCommitter != "")):
                    if (oCommitter != " ") and (iCommitter != " "):
                        # Match

                        listCommitters.append(iCommitter)
                        log_line = "Adding file " + oFile
                        my_graph.log(log_line)
                        line_df = '"' + oCommitter + '","' + iCommitter + '"\n'
                        df_file.write(line_df)
                    
                        # If it also matches a method 
                        # (as long as we have one)
                        if (oMethod == iMethod) and (oMethod != ""):
                            log_line = "Adding method " + oMethod
                            line_dm = '"' + oCommitter + '","' + iCommitter + '"\n'
                            dm_file.write(line_dm)
            if len(grepline_data) == 4:
                iMethod = grepline_data[2]  

        # FIXME: To do: Check csv file-format and data

    df_file.close()
    dm_file.close()
    print my_graph.log("Finished: output created:")
    comm1 = "mv DataMethods.csv " + my_graph.OUT_PATH[5:]
    comm2 = "mv DataFiles.csv " + my_graph.OUT_PATH[5:]
    print "Executing: " + comm1
    print "Executing: " + comm2
    os.system(comm1)
    os.system(comm2)
    go_home_dir()
    
    print "WARNING: You might be in 'detached HEAD' state."
    print "You might want to remove Repository directory."
    print my_graph.log("\r\n - Graph Data Creator End - \r\n")
