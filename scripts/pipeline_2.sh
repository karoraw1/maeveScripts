#!/bin/bash

#SBATCH
#SBATCH --job-name=^SID^_trim
#SBATCH --time=00:15:00
#SBATCH --ntasks=24
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=25600
#SBATCH --partition=lrgmem
#SBATCH --mail-type=END
#SBATCH --mail-user=karoraw1@jhu.edu
#SBATCH --error=^SID^_trim_test.err
#SBATCH --output=^SID^_trim_test.out

module load R/3.4.0
module load python/2.7.10

# these will be filled in automatically
SEQ_ID=^SID^
BASE_OUT=^OP^
TSTAT=^T^
DEMUX_DIR=$BASE_OUT/$SEQ_ID/Demux
TRIM_DIR=$BASE_OUT/$SEQ_ID/Trim

mkdir -p $TRIM_DIR
Rscript ^PWD^/FilterNTrim.R $SEQ_ID $DEMUX_DIR $TSTAT $TRIM_DIR
Rscript ^PWD^/quality_plot.R $BASE_OUT $SEQ_ID Trim
