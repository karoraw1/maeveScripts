library(dada2)

# command line arguments
args <- commandArgs(TRUE)

# read in location
seq_ID <- args[1]
in_path <- args[2]
trim_path <- args[3]
out_path <- args[4]

write(seq_ID, stdout())
write(in_path, stdout())
write(trim_path, stdout())
write(out_path, stdout())

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
if (length(pre_fnFs) == 0) {
    pre_fnFs <- sort(list.files(in_path, pattern="R1_001.fastq"))
    pre_fnRs <- sort(list.files(in_path, pattern="R2_001.fastq"))
}
fnFs = file.path(in_path, pre_fnFs)
fnRs = file.path(in_path, pre_fnRs)

# make new files
sample.names <- sapply(strsplit(pre_fnFs, "[.]"), `[`, 1)
filtFs <- file.path(out_path, paste0(sample.names, "_F_filt.fastq"))
filtRs <- file.path(out_path, paste0(sample.names, "_R_filt.fastq"))

array1 = (5:-5)*10
for (j in array1){
    stat_len = truncLen_arg[1]
    dyn_len = truncLen_arg[2]+j
    truncLen_test = c(stat_len, dyn_len)
    out = filterAndTrim(fnFs[1:2], filtFs[1:2], fnRs[1:2], filtRs[1:2],
                        compress=FALSE, truncQ=trunQ_arg[1],
                        truncLen=truncLen_test, rm.phix=TRUE, 
                        verbose=FALSE, multithread=TRUE,
                        maxN=0, trimLeft=trimLeft_arg,
                        maxEE=maxEE_arg)
    retained = mean( out[,"reads.out"] / out[,"reads.in"] )
    write( paste("Retained", retained, "(", stat_len, ",", dyn_len, ")" ), stdout() )
}

for (j in array1){
    dyn_len = truncLen_arg[1]+j
    stat_len = truncLen_arg[2]
    truncLen_test = c(dyn_len, stat_len)
    out = filterAndTrim(fnFs[1:2], filtFs[1:2], fnRs[1:2], filtRs[1:2],
                        compress=FALSE, truncQ=trunQ_arg[1],
                        truncLen=truncLen_test, rm.phix=TRUE, 
                        verbose=FALSE, multithread=TRUE,
                        maxN=0, trimLeft=trimLeft_arg,
                        maxEE=maxEE_arg)
    retained = mean(out[,"reads.out"]/out[,"reads.in"])
    write( paste("Retained", retained, "(", dyn_len, ",", stat_len, ")" ), stdout() )
}
