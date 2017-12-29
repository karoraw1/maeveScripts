#!/bin/bash

#SBATCH
#SBATCH --job-name=learnerrors
#SBATCH --time=30:00:00
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --partition=lrgmem
#SBATCH --mail-type=END
#SBATCH --mail-user=karoraw1@jhu.edu
#SBATCH --error=errors_dada.err
#SBATCH --output=errors_dada.out

module load R/3.4.0
module load python/2.7.10

RAW_BASE=/data/sprehei1/Raw_data_group
SEQ_ID=esakows1_132789
RAW_FWD=Undetermined_S0_L001_R1_001.fastq
RAW_REV=Undetermined_S0_L001_R2_001.fastq
RAW_IDX=Undetermined_S0_L001_I1_001.fastq

BASE_OUT=/home-3/karoraw1@jhu.edu/scratch/16S_Libraries

# demultiplex 
DEMUX_DIR=$BASE_OUT/$SEQ_ID/Demux
mkdir -p $DEMUX_DIR

parallel -j 24 -a ../data/Barcode_sequences.txt "grep -B1 {} $RAW_BASE/$SEQ_ID/$RAW_IDX > $DEMUX_DIR/{}.ids.fastq"
ls $DEMUX_DIR/*.ids.fastq | parallel -j 24 "grep -A0 @M00776 {} >> {}.headers.txt"

rm *.ids.fastq
for i in ./*.headers.txt; do cat "$i" | sed 's/1:N:0:0//g' > Barcode_IDs/"$i".2.txt; done
rm *.headers.txt

# combine paired end reads
mkdir Flash_Files
scripts/flash Undetermined_S0_L001_R1_001.fastq.gz Undetermined_S0_L001_R2_001.fastq.gz -o Flash_Files -M 300


# add orphaned reads back

# print out read lengths and unique counts 
python scripts/prepForDBotu.py -i demux_derep_trim_dirs.txt

# 
python scripts/prepForDBotu.py -i demux_derep_trim_dirs.txt -trim L270H281 -trim-out /data/sprehei1/Keith_Maeve1_138650/Truncated_Fastq_4
Rscript scripts/learnErrors.r
Rscript scripts/callOTUsAndnoChim.r
Rscript scripts/assignTaxonomy.r
