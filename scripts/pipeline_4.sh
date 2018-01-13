#!/bin/bash

#SBATCH
#SBATCH --job-name=^SID^_taxa
#SBATCH --time=30:00:00
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --mem=960G
#SBATCH --partition=lrgmem
#SBATCH --mail-type=END
#SBATCH --mail-user=karoraw1@jhu.edu
#SBATCH --error=^SID^_taxa.err
#SBATCH --output=^SID^_taxa.out

module load R/3.4.0
module load python/2.7.10

SEQ_ID=^SID^
BASE_OUT=^OP^
THREADS=48
REF_ALL=^RA^
REF_SP=^RS^

Rscript ^PWD^/assign_taxa.R $BASE_OUT $SEQ_ID $THREADS $REF_ALL $REF_SP
