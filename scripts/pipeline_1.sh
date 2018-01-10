#!/bin/bash

#SBATCH
#SBATCH --job-name=^SID^_demux
#SBATCH --time=2:30:00
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --mem=960G
#SBATCH --partition=lrgmem
#SBATCH --mail-type=END
#SBATCH --mail-user=karoraw1@jhu.edu
#SBATCH --error=^SID^_demux_test.err
#SBATCH --output=^SID^_demux_test.out

module load R/3.4.0
module load python/2.7.10

# these will be filled in automatically
SEQ_ID=^SID^
IDX_PATH=^I^
FWD_PATH=^F^
REV_PATH=^R^
BASE_OUT=^OP^
BCODE=^B^

# Preprocess
PP_DIR=$BASE_OUT/$SEQ_ID/Preprocess
mkdir -p $PP_DIR
parallel -j 3 "^PWD^/trim_last_two_header_chars.sh {} $PP_DIR" ::: $IDX_PATH $FWD_PATH $REV_PATH
FWD_PATH=$PP_DIR/`basename $FWD_PATH`;
REV_PATH=$PP_DIR/`basename $REV_PATH`;
IDX_PATH=$PP_DIR/`basename $IDX_PATH`;

for i in $IDX_PATH $FWD_PATH $REV_PATH; do
    ^PWD^/subsect_into_new_dir.sh $i $PP_DIR;
done;
python ^PWD^/check_headers.py $PP_DIR


# auto path shortcuts
DEMUX_DIR=$BASE_OUT/$SEQ_ID/Demux
mkdir -p $DEMUX_DIR

echo "Parsing Index File"

parallel -j 48 -a $BCODE --colsep '\t' "grep --no-group-separator -B1 {2} $IDX_PATH | grep "^@" | sed 's/^@//g' > $DEMUX_DIR/{1}.headers"

echo "Demultiplexing" 

for header in `ls $DEMUX_DIR/*.headers`; do
    path_name=$(dirname $header)
    file_name=$(basename $header)
    sample_name=$(cut -d "." -f 1 <<< "$file_name")
    sample_path=$path_name/$sample_name
    filterbyname.sh in=$FWD_PATH in2=$REV_PATH out=$sample_path.R1.fastq out2=$sample_path.R2.fastq names=$header include=t;
done

Rscript ^PWD^/quality_plot.R $BASE_OUT $SEQ_ID Demux
