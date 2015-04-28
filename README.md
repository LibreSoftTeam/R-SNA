# R-SNA - LibreSoft

Social Network Analysis software Shell(bash)-to-Python translation, from Christian Coré Ramiro code.
Note: This program uses Git and Ctags, please install both programs before running GraphDataCreator

Usage:
$python GraphDataCreator.py -f <starting-date of study*> -t <ending date of study*> -r <url-repo>/<reuse**>

*Starting and ending date of study format: YYYY-MM-DD
*When starting date is empty, study starts at the beginning of times.
*When ending date is empty, current date will be chosen.

** In -r field, 'reuse' Re-uses a previously downloaded repository (It has to be a folder called 'Repository' in directory)

Example:
$python GraphDataCreator.py -f 2014-01-01 -t 2014-03-31 -r https://github.com/GNOME/gedit

Output:

This program creates two main folders, Data and Repository,
and outputs two csv files (DataFiles.csv and DataMethods.csv) in directory Data/output

Other options:

  -h  prints help page.
  -v  Verbose mode.
