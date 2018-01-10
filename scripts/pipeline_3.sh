#!/bin/bash

#SBATCH
#SBATCH --job-name=^SID^_DADA2
#SBATCH --time=30:00:00
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --mem=960G
#SBATCH --partition=lrgmem
#SBATCH --mail-type=END
#SBATCH --mail-user=karoraw1@jhu.edu
#SBATCH --error=^SID^_DADA2.err
#SBATCH --output=^SID^_DADA2.out

module load R/3.4.0
module load python/2.7.10

SEQ_ID=^SID^
BASE_OUT=^OP^
SUFF1=^S1^ 
SUFF2=^S2^
SAMSPLIT=^SS^
THREADS=48

Rscript ^PWD^/fullDADApipe_PE.R $BASE_OUT $SEQ_ID $SUFF1 $SUFF2 $SAMSPLIT $THREADS

Rscript ^PWD^/fullDADApipe_SE.R $BASE_OUT $SEQ_ID $SUFF2 $SAMSPLIT $THREADS

Rscript ^PWD^/fullDADApipe_SE.R $BASE_OUT $SEQ_ID $SUFF1 $SAMSPLIT $THREADS
