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


BASE_DIR=@#$


# demultiplex 
for i in `cat ./Barcode_sequences.txt`; do grep -B1 "$i" Undetermined_S0_L001_I1_001.fastq > "$i".ids.fastq; done


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
