#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
GraphDataCreator Shell-to-Pyhton translation from Christian Coré Ramiro code
Miguel Angel Fernandez Sanchez
"""

import os
import sys

print " - Graph Data Creator Started - "
print " - MAKE SURE CTAGS, PERL AND GIT ARE INSTALLED IN YOUR COMPUTER\r\n"

class GraphData:

    def help(self):
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
        line += "-f\tEnding date of study. When empty, current date will "
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

if __name__ == "__main__":
    my_graph = GraphData()
    print my_graph.help()

