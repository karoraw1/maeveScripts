
args <- commandArgs(TRUE)
base_path <- as.double(args[1])
seq_ID <- as.double(args[2])


path <- paste(base_path
fnFs <- sort(list.files(path, pattern=".R1.fastq", full.names = TRUE))
fnRs <- sort(list.files(path, pattern=".R2.fastq", full.names = TRUE))


png(filename=fwdPNGname)
plotQualityProfile(fnFs[1:2])
dev.off()

png(filename=revPNGname)
plotQualityProfile(fnRs[1:2])
dev.off
