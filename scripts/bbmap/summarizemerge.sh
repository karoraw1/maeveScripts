#!/bin/bash

usage(){
echo "
Written by Brian Bushnell
Last modified June 6, 2016

Description:  Summarizes the output of GradeMerge for comparing 
read-merging performance.

Usage:  summarizemerge.sh in=<file>

Parameters:
in=<file>           A file containing GradeMerge output.

Please contact Brian Bushnell at bbushnell@lbl.gov if you encounter any problems.
"
}

pushd . > /dev/null
DIR="${BASH_SOURCE[0]}"
while [ -h "$DIR" ]; do
  cd "$(dirname "$DIR")"
  DIR="$(readlink "$(basename "$DIR")")"
done
cd "$(dirname "$DIR")"
DIR="$(pwd)/"
popd > /dev/null

#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )/"
CP="$DIR""current/"

z="-Xmx120m"
EA="-ea"
EOOM=""
set=0

if [ -z "$1" ] || [[ $1 == -h ]] || [[ $1 == --help ]]; then
	usage
	exit
fi

summarizemerge() {
	if [[ $NERSC_HOST == genepool ]]; then
		module unload oracle-jdk
		module load oracle-jdk/1.8_144_64bit
		module load pigz
	fi
	local CMD="java $EA $EOOM $z -cp $CP driver.ProcessSpeed $@"
#	echo $CMD >&2
	eval $CMD
}

summarizemerge "$@"
