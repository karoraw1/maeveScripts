library(dada2)
path <- "/data/sprehei1/Keith_Maeve1_138650/Truncated_Fastq_4"
pre_fnFs <- sort(list.files(path, pattern=".fastq"))
sample.names <- sapply(strsplit(pre_fnFs, "[.]"), `[`, 1)
filt_path <- "/data/sprehei1/Keith_Maeve1_138650/Filtered_Fastq_5"
fnFs <- file.path(filt_path, paste0(sample.names, ".filt.fastq"))
names(fnFs) <- sample.names
set.seed(100)
err <- learnErrors(fnFs, multithread=TRUE, randomize=TRUE)
save(err, file="/home-3/karoraw1@jhu.edu/work/sprehei1/Keith_Files/maeveScripts/errorsWS.RData")
