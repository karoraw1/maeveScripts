library(dada2)

# command line arguments
args <- commandArgs(TRUE)

# read in location
trim_path <- args[1]
data_path <- args[2]

# read in trim params
trim_df = read.csv(trim_path, sep="\t", row.names=1)

#  check
write(trim_df.head(), stdout())

#pre_fnFs <- sort(list.files(path, pattern=".fastq"))
#sample.names <- sapply(strsplit(pre_fnFs, "[.]"), `[`, 1)
#filt_path <- "/data/sprehei1/Keith_Maeve1_138650/Filtered_Fastq_5"
#fnFs <- file.path(filt_path, paste0(sample.names, ".filt.fastq"))
#filterAndTrim(pre_fnFs, fnFs, compress=FALSE, truncLen=270, rm.phix=TRUE, verbose=TRUE, multithread=TRUE)
