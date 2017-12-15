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
module load python/2.7.10

python prepForDBotu.py -i demux_derep_trim_dirs.txt -trim L270H281 -trim-out /data/sprehei1/Keith_Maeve1_138650/Truncated_Fastq_4
Rscript /home-3/karoraw1@jhu.edu/work/sprehei1/Keith_Files/maeveScripts/learnErrors.r

