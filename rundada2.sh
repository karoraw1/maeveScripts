#!/bin/bash

#SBATCH
#SBATCH --job-name=learnerrors
#SBATCH --time=4:00:00
#SBATCH --ntasks=48
#SBATCH --cpus-per-task=1
#SBATCH --partition=lrgmem
#SBATCH --mail-type=END
#SBATCH --mail-user=karoraw1@jhu.edu
#SBATCH --error=errors_dada.err
#SBATCH --output=errors_dada.out

module load R/3.4.0
Rscript /home-3/karoraw1@jhu.edu/work/sprehei1/Keith_Files/maeveScripts/learnErrors.r

