#!/bin/bash

#SBATCH
#SBATCH --job-name=esakows1_132789_DADA2
#SBATCH --time=30:00:00
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --mem=960G
#SBATCH --partition=lrgmem
#SBATCH --mail-type=END
#SBATCH --mail-user=karoraw1@jhu.edu
#SBATCH --error=esakows1_132789_DADA2.err
#SBATCH --output=esakows1_132789_DADA2.out

module load R/3.4.0
module load python/2.7.10

SEQ_ID=esakows1_132789
BASE_OUT=/home-3/karoraw1@jhu.edu/scratch/16S_Libraries
SUFF1=_F_filt.fastq 
SUFF2=_R_filt.fastq
SAMSPLIT=_F_filt
THREADS=48

Rscript /home-3/karoraw1@jhu.edu/work/sprehei1/Keith_Files/maeveScripts/scripts/fullDADApipe_PE.R $BASE_OUT $SEQ_ID $SUFF1 $SUFF2 $SAMSPLIT $THREADS
