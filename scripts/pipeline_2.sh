#!/bin/bash

#SBATCH
#SBATCH --job-name=pipeline_test
#SBATCH --time=5:00:00
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

# will actually take 30 hours + demuxing time

RAW_BASE=/data/sprehei1/Raw_data_group
SEQ_ID=esakows1_132789
RAW_FWD=Undetermined_S0_L001_R1_001.fastq
RAW_REV=Undetermined_S0_L001_R2_001.fastq
RAW_IDX=Undetermined_S0_L001_I1_001.fastq
BASE_OUT=/home-3/karoraw1@jhu.edu/scratch/16S_Libraries
BCODE=../data/Barcode_sequences.txt
IDX_PATH=$RAW_BASE/$SEQ_ID/$RAW_IDX
FWD_PATH=$RAW_BASE/$SEQ_ID/$RAW_FWD
REV_PATH=$RAW_BASE/$SEQ_ID/$RAW_REV

# demultiplex 
DEMUX_DIR=$BASE_OUT/$SEQ_ID/Demux
#mkdir -p $DEMUX_DIR

vsearch --fastq_truncee --fastq_mergepairs  --reverse fastqfile (--fastaout | --fastqout | --fastaout_notmerged_fwd
| --fastaout_notmerged_rev|--fastqout_notmerged_fwd | --fastqout_notmerged_rev |
--eetabbedout) outputfile [options] --threads 48

## combine paired end reads
#mkdir Flash_Files
#scripts/flash Undetermined_S0_L001_R1_001.fastq.gz Undetermined_S0_L001_R2_001.fastq.gz -o Flash_Files -M 300

## add orphaned reads back

## print out read lengths and unique counts 
#python scripts/prepForDBotu.py -i demux_derep_trim_dirs.txt

# 
#python scripts/prepForDBotu.py -i demux_derep_trim_dirs.txt -trim L270H281 -trim-out /data/sprehei1/Keith_Maeve1_138650/Truncated_Fastq_4
#Rscript scripts/learnErrors.r
#Rscript scripts/callOTUsAndnoChim.r
#Rscript scripts/assignTaxonomy.r
