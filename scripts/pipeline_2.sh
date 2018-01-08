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
BASE_OUT=^OP^
BCODE=^B^
TSTAT=^T^
DEMUX_DIR=$BASE_OUT/$SEQ_ID/Demux
TRIM_DIR=$BASE_OUT/$SEQ_ID/Trim

mkdir -p $TRIM_DIR
Rscript ^PWD^/dada2_trimFilter.R $SEQ_ID $DEMUX_DIR $TSTAT $TRIM_DIR
