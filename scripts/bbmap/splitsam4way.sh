#!/bin/bash

function usage(){
echo "
Written by Brian Bushnell
Last modified January 21, 2015

Description:  Splits sam reads into 4 output files depending on mapping.

Usage:        splitsam4way.sh <input> <outplus> <outminus> <outchimeric> <outunmapped>

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
EA="-ea"
EOOM=""
set=0

if [ -z "$1" ] || [[ $1 == -h ]] || [[ $1 == --help ]]; then
	usage
	exit
fi

function split() {
	if [[ $NERSC_HOST == genepool ]]; then
		module unload oracle-jdk
		module load oracle-jdk/1.8_144_64bit
		module load pigz
	fi
	local CMD="java $EA $EOOM -Xmx128m -Xms128m -cp $CP jgi.SplitSam4Way $@"
	echo $CMD >&2
	eval $CMD
}

split "$@"
