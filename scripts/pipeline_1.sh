#!/bin/bash

#SBATCH
#SBATCH --job-name=pipeline_test
#SBATCH --time=2:30:00
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --mem=960G
#SBATCH --partition=lrgmem
#SBATCH --mail-type=END
#SBATCH --mail-user=karoraw1@jhu.edu
#SBATCH --error=demux_test.err
#SBATCH --output=demux_test.out

#module load R/3.4.0
#module load python/2.7.10

# will actually take 32 hr

# these will be filled in automatically
RAW_BASE=/data/sprehei1/Raw_data_group
SEQ_ID=esakows1_132789
RAW_FWD=Undetermined_S0_L001_R1_001.fastq
RAW_REV=Undetermined_S0_L001_R2_001.fastq
RAW_IDX=Undetermined_S0_L001_I1_001.fastq
BASE_OUT=/home-3/karoraw1@jhu.edu/scratch/16S_Libraries
BCODE=../data/esakows1_132789_barcodes.txt

# auto path shortcuts
IDX_PATH=$RAW_BASE/$SEQ_ID/$RAW_IDX
FWD_PATH=$RAW_BASE/$SEQ_ID/$RAW_FWD
REV_PATH=$RAW_BASE/$SEQ_ID/$RAW_REV
DEMUX_DIR=$BASE_OUT/$SEQ_ID/Demux
mkdir -p $DEMUX_DIR


module load R/3.4.0

echo "Parsing Index File"

parallel -j 48 -a $BCODE --colsep '\t' "grep --no-group-separator -B1 {2} $IDX_PATH | grep @M00776 | sed 's/@M00776/M00776/g' > $DEMUX_DIR/{1}.headers"

echo "Demultiplexing" 

for header in `ls $DEMUX_DIR/*.headers`; do
    path_name=$(dirname $header)
    file_name=$(basename $header)
    sample_name=$(cut -d "." -f 1 <<< "$file_name")
    sample_path=$path_name/$sample_name
    filterbyname.sh in=$FWD_PATH in2=$REV_PATH out=$sample_path.R1.fastq out2=$sample_path.R2.fastq names=$header include=t;
done

#rm -r $DEMUX_DIR/*.headers

Rscript scripts/quality_plot.R $BASE_OUT $SEQ_ID

