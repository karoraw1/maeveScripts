library(dada2)

# command line arguments
args <- commandArgs(TRUE)

# read in location
seq_ID <- args[1]
in_path <- args[2]
trim_path <- args[3]
out_path <- args[4]

# read in trim params
trim_df = read.csv(trim_path, sep=",")
fwd_row = subset(trim_df, SeqID == seq_ID & R == 1)
rev_row = subset(trim_df, SeqID == seq_ID & R == 2)

# organize command args
trunQ_arg = c(fwd_row[["truncQ"]], rev_row[["truncQ"]])
truncLen_arg = c(fwd_row[["truncLen"]], rev_row[["truncLen"]])
trimLeft_arg = c(fwd_row[["trimLeft"]], rev_row[["trimLeft"]])
maxEE_arg = c(fwd_row[["maxEE"]], rev_row[["maxEE"]])

# find files
pre_fnFs <- sort(list.files(in_path, pattern="R1.fastq"))
pre_fnRs <- sort(list.files(in_path, pattern="R2.fastq"))

# make new files
sample.names <- sapply(strsplit(pre_fnFs, "[.]"), `[`, 1)
filtFs <- file.path(out_path, paste0(sample.names, "_F_filt.fastq"))
filtRs <- file.path(out_path, paste0(sample.names, "_R_filt.fastq"))

filterAndTrim(pre_fnFs, fnFs, pre_fnRs, filtRs,
              compress=FALSE, truncQ=trunQ_arg[1],
              truncLen=truncLen_arg, rm.phix=TRUE, 
              verbose=TRUE, multithread=TRUE,
              maxN=0, trimLeft=trimLeft_arg,
              maxEE=maxEE_arg)
