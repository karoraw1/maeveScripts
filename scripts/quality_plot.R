library(dada2)
args <- commandArgs(TRUE)
base_path <- as.double(args[1])
seq_ID <- as.double(args[2])

# library(dada2)
# base_path = "/home-3/karoraw1@jhu.edu/scratch/16S_Libraries"
# seq_ID = "esakows1_132789"

path=file.path(base_path, seq_ID, "Demux")
fnFs <- sort(list.files(path, pattern=".R1.fastq", full.names = TRUE))
fnRs <- sort(list.files(path, pattern=".R2.fastq", full.names = TRUE))
sample.names <- sapply(strsplit(basename(fnFs), ".headers"), `[`, 1)


fwdPNGname = file.path(base_path, seq_ID, "R1_quals.png")
revPNGname = file.path(base_path, seq_ID, "R2_quals.png")

file_sizes_f = sort(sapply(fnFs, file.size), decreasing = T, na.last = NA)
file_sizes_r = sort(sapply(fnRs, file.size), decreasing = T, na.last = NA)
to_plot_fwd=row.names(as.data.frame(file_sizes_f[1:2]))
to_plot_rev=row.names(as.data.frame(file_sizes_r[1:2]))


png(filename=fwdPNGname)
plotQualityProfile(to_plot_fwd)
dev.off()

png(filename=revPNGname)
plotQualityProfile(to_plot_rev)
dev.off()
