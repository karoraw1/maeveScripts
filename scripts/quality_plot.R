library(dada2)
args <- commandArgs(TRUE)
base_path <- as.double(args[1])
seq_ID <- as.double(args[2])

path=file.path(base_path, seq_ID, "Demux")
fnFs <- sort(list.files(path, pattern=".R1.fastq", full.names = TRUE))
fnRs <- sort(list.files(path, pattern=".R2.fastq", full.names = TRUE))
sample.names <- sapply(strsplit(basename(fnFs), ".headers"), `[`, 1)

fwdPNGname = file.path(base_path, seq_ID, "R1_quals.png")
revPNGname = file.path(base_path, seq_ID, "R2_quals.png")

png(filename=fwdPNGname)
plotQualityProfile(fnFs[1:2])
dev.off()

png(filename=revPNGname)
plotQualityProfile(fnRs[1:2])
dev.off()
