#!/bin/bash

echo " - Graph Data Creator Started - "
echo " - MAKE SURE CTAGS, PERL AND GIT ARE INSTALLED IN YOUR COMPUTER"
sleep 5

function help()
{
echo "NAME

   GraphDataCreator.sh

USAGE

   ./GrahDataCreator [SHORT-OPTION]

EXAMPLE

   ./GraphDataCreator.sh -f 2010-1-1 -t 2011-1-1 -r git://git.openstack.org/openstack/swift -v


DESCRIPTION

   GraphDataCreator.sh reads information of a Git repository and outputs two
   .csv files ready to be read to represent a software community. The files
   contain pairs developer-developer meaning that both developers have
   worked together. One file uses file-scope to create a relationship while
   the other narrows relationship down using a method-scope.

OPTIONS

   -h    Prints help page.

   -f    Starting date of study. When empty, study start the beginning of times.
         Format: 2012-12-31

   -f    Ending date of study. When empty, current date will be chosen.
         Format: 201-12-31

   -r    Repository url. When empty, we assume we are in a directory tracked
         by Git. Example: git://git.openstack.org/openstack/swift

   -v    Verbose mode.

DEPENDENCIES

   Perl, Git and Ctags need to run this script.

OUTPUT

   DataMethods.csv - File using relationship-in-method approach

   DataFiles.csv - File using relantionship-in-file approach

"

}

function log ()
{
  if [ "$verbose" = true ]
  then
    echo "$@"
  fi
}

function findFittingTag()
{

  # Firs argument: file to compare
  # Second argument: line number
  # Third argument: rev
  # Fourth argument: author

  matches=$( grep $1 tags )
  # Case of not matching any tag
  if [ -z "${matches}" ]
  then
    # In this case the output has three fields (no tag)
    log “Adding file tag”
    echo "$3,$1,$4" >> outputFile.txt

  else
  
    fittingLine=""
    bestNumber=""

    # This While loop calculates the method where the line number received belongs to

    while read matchLine
    do
      fMatch=$( echo "$matchLine" | awk '{print $2}' )
      ext=$(echo "$fMatch" | sed 's/^.*\.//')

      specialExt=false
      # for javascript, c#, java and objectiveC files, a function is defined as an "n" instead of an "f" in ctags
      case "$ext" in
      cs|java|js|m|mm )
         specialExt=true
         ;;
      esac

      # Fourth parameter in tags file holds the type of tag
      isAFunction=$( echo "$matchLine" | awk '{print $4}' )

      if [[ "$specialExt" == true  &&  "$isAFunction" == "m" ]] || [[ "$specialExt" == false && "$isAFunction" == "f" ]]
      then
        log "We are in a function-> f: $fMatch ext: $ext Spec: $specialExt tag: $isAFunction"
        LineNumberFromCtag=$( echo "$matchLine" | awk '{print $3}' )
        # Removing two last chars from third field to get the line number
        LineNumber=$( echo ${LineNumberFromCtag%??} )
        # Case of methods matching #
        if [ -z "${fittingLine}" ]
        then
          if [ "$LineNumber" -gt "$2" ]
          then
            fittingLine=$( echo "$matchLine" )
            bestNumber=$( echo "$LineNumber" )
          fi
        else
          if [ "$LineNumber" -gt "$2" ] && [ "$LineNumber" -lt "$bestNumber" ]
          then
            fittingLine=$( echo "$matchLine" )
            bestNumber=$( echo "$LineNumber" )
          fi
        fi
      fi  
    done <<< "$matches"

  
    log "..and fitting line has been: $fittingLine"

    TagToWrite=$( echo "$fittingLine" | awk '{print $1}' )

    # Adding tag to output file
    log "Adding $1 $TagToWrite to outputFile.txt"
    echo "$3,$1 $TagToWrite,$4" >> outputFile.txt

  fi

}

##########################    MAIN     ########################

# Initialising options
verbose=false
from="1971-1-1"
until=$(date +%Y-%m-%d)

unamestr=`uname`
if [[ "$unamestr" != 'Linux' ]]
then
  echo "We are not under Linux, no options available"
else
	while getopts ":t:r:f:hv" flag; do
		case "${flag}" in
		  v) verbose=true
		     echo "Mode verbose on"
		     ;;
		  f) from=$OPTARG
		     ;;
		  t) until=${OPTARG}
		     ;;
		  r) r=${OPTARG}
		     repo=true
		     echo "Repository: $r"
		     ;;
		  h) help
		     exit 1
		     ;;
		  *) echo "Unexpected option. Please use option -h for further information"
		     exit 1
		     ;;
		esac
	done

	# Checking existance of Repository; we need it!
	if [ -d "Repository" ]
	then
		echo "Please, remove directory Repository before starting"
		exit 1
	fi

	# Checking from and until dates
	fromString=$(date -d $from)

	if [ $? -eq 0 ]
	then
		echo "Valid starting date: $fromString"
	else
		echo "Starting date is wrong. Please use option -h for further information"
		exit 1
	fi

	untilString=$(date -d $until)

	if [ $? -eq 0 ]
	then
		echo "Valid ending date: $untilString"
	else
		echo "Ending date is wrong. Please use option -h for further information"
		exit 1
	fi

	# Check if repository exists
	if [ "$repo" = true ]
	then
		echo "Starting download of Repository"
		git clone $r Repository
		if [ $? -eq 0 ]
		then
		  echo "Repository downloaded succesfully"
		  cd Repository
		else
		  echo "Error downloading Repository"
		  exit 1
		fi
	fi
fi #of Linux check

if [ ! -d ".git" ]
then
  echo "No Git repository found. Please use option -h for further information"
  exit 1
fi

# First: git clone: project as a parameter
# ----------- git clone url folder-name -------------------

git log --all --since="$from" --until="$until" --pretty=format:"%H %an" > ./archivoDeCommitsDesdeScript.txt

if [ -s archivoDeCommitsDesdeScript.txt ]
then
  echo "File of commits created succesfully"
else
  echo "File of commits empty. Please use option -h for further information"
fi

# Now we read the first line of the file with the commit revs

echo "Reading first line and checking out from first commit"
read -r startline<./archivoDeCommitsDesdeScript.txt
revline=$(echo "$startline" | awk '{print $1}')
# Deberia coger el segundo parámetro en vez del primero
# ¿Por qué coge la palabra 'commit' en vez del identificador?
log "First line: $revline"

git checkout -f $revline 

# ctags out of Linux
unamestr=`uname`
if [[ "$unamestr" != 'Linux' ]]
then
  # expanding aliases first.... (MacOS)
  shopt -s expand_aliases
  alias ctags="`brew --prefix`/bin/ctags"
fi

echo "Creating tags file: tags"
# Do this if ctags does not exist, otherwise just update it
# Getting rid of annoying warning output
ctags -w -R -n . >> 2&>1

> outputFile.txt

while read line
do
  # Get file and line of change
  # and then get tag, we have to update
  
  log “- NEW LINE $line -“
    
    rev=$(echo "$line" | awk '{print $1}')
    author=$(echo "$line" | awk '{$1=""; print $0}' )
    log "Author: $author"
    entireDiff=$(git diff --unified=0 $rev^!)
    
    git checkout $rev

    while read grepline
    do
      ### Getting rid of all lines we dont care about
      ### We only want this when we don't need to read the output of git diff, but only the files modified ###
      if [ ${grepline:0:1} != '+' ] && [ ${grepline:0:1} != '-' ]
      then

        file1=$(echo "$grepline" | grep "diff --git" | cut -d " " -f 4 | cut -c 3-)

        lineNumber1=$(echo "$grepline" | grep "@@" | cut -d " " -f 3 | cut -c 2- | cut -d "," -f 1)
    
        if [ -n "$file1" ]
        then
          lastFile2=$(echo "$file1 ")
          log "File: $file1" 
        fi
      
        if [ -n "$lineNumber1" ]
        then
          # When grep is empty, we add a tag -> it will be a file-to-file collaboration
          findFittingTag $lastFile2 $lineNumber1 $rev "$author"
        fi
      fi
    done <<< "$entireDiff"
    
    echo "Tag and committer added to output file"
    echo "Now updating ctags file"
    ## HERE UPDATING TAGS FILE WITH TAGS OF MODIFIED FILES

    allFiles=$(echo "$entireDiff" | grep "diff --git" | cut -d " " -f 4 | cut -c 3-)
    while read fileModifiedTag
    do
      log "FILE: $fileModifiedTag"
      ctags -f AuxTagFile.txt -n $fileModifiedTag
      # remove comment lines from the just-created tag file
      perl -n -i.bak -e "print unless /_TAG_FILE_/" AuxTagFile.txt
      perl -n -i.bak -e "print unless /_TAG_PROGRAM_/" AuxTagFile.txt
      
      # remove lines of that file in tags file
      # adding backslash to scape slash before removing (perl input)
      Second=$( sed 's|/|\\/|g' <<< $fileModifiedTag )
      log ">> To be removed $fileModifiedTag"
      bef=$(ls -tlar tags)
      log "Original $bef"
      perl -n -i.bak -e "print unless /$Second/" tags
      aft=$(ls -tlar tags)
      log "After removals $aft"
      #add new lines
      cat AuxTagFile.txt >> tags
      adds=$(ls -tlar tags)
      log "After additions $adds"
    done <<< "$allFiles"
    echo "Tags added to tags file: now is up to date"

done < ./archivoDeCommitsDesdeScript.txt

> DataFiles.csv
> DataMethods.csv

echo "Starting to create data files -methods and files-“

while read line
do
  log "$line"
  # Extracting all relevant data
  oRev=$( echo $line | awk -F',' '{print $1}')
  oTag=$( echo $line | awk -F',' '{print $2}')
  oFile=$( echo $oTag | awk '{print $1}')
  oMethod=$( echo $oTag | awk '{print $2}')
  oCommitter=$( echo $line | awk -F',' '{print $3}')
  log "COMMITTER $oCommitter"

  # Array of committers to avoid repetitions
  arrayCommitters=()
  # Grepping lines with same method
   log "Grepping for $oFile"
  grep $oFile ./outputFile.txt | while read -r gLine
  do
    iCommitter=$( echo $gLine | awk -F',' '{print $3}')
    iTag=$( echo $gLine | awk -F',' '{print $2}')
    iMethod=$( echo $iTag | awk '{print $2}')
    # If Committer is not in the list
    log "File $oFile and Method $iMethod of Committer $iCommitter"
    if ! `echo ${arrayCommitters[@]} | grep -q "$iCommitter"` ; then
      # Avoiding links between same committer
      if [[ "$oCommitter" != "$iCommitter" ]]
      then
        # Match
        arrayCommitters+=("$iCommitter")
        log "Adding file $oFile"
        echo "\"$oCommitter\",\"$iCommitter\"" >> DataFiles.csv
 
        # If it also matches a method (as long as we have one)
        if [[ "$oMethod" == "$iMethod" ]] && [ -n "$oMethod" ]
        then
          log "Adding method $oMethod"
          echo "\"$oCommitter\",\"$iCommitter\"" >> DataMethods.csv
        fi 
      fi
    fi
    iMethod=$( echo $gLine | awk '{print $2}')
  done
  # clear array of Committers
  unset $arrayCommitters

done < ./outputFile.txt

mv DataMethods.csv ..
mv DataFiles.csv ..
cd ..

echo "Finished: output created:"
Dm=$(ls -talr DataMethods.csv)
Df=$(ls -talr DataFiles.csv)
echo "$Dm"
echo "$Df"

echo "WARNING: You might be in 'detached HEAD' state."
echo "You might want to remove Repository directory."

