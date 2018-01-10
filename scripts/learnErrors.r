library(dada2)


# command line arguments
args <- commandArgs(TRUE)

# read in location
trim_path <- args[1]
#seq_ID <- args[1]
#in_path <- args[2]
#out_path <- args[4]

pre_fnFs <- sort(list.files(path, pattern=".fastq"))
sample.names <- sapply(strsplit(pre_fnFs, "[.]"), `[`, 1)
filt_path <- "/data/sprehei1/Keith_Maeve1_138650/Filtered_Fastq_5"
fnFs <- file.path(filt_path, paste0(sample.names, ".filt.fastq"))
names(fnFs) <- sample.names
set.seed(100)
err <- learnErrors(fnFs, multithread=TRUE, randomize=TRUE)
save(err, file="/home-3/karoraw1@jhu.edu/work/sprehei1/Keith_Files/maeveScripts/errorsWS.RData")
