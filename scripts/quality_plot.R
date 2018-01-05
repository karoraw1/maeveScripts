library(dada2)
args <- commandArgs(TRUE)
base_path <- args[1]
seq_ID <- args[2]

# library(dada2)
# base_path = "/home-3/karoraw1@jhu.edu/scratch/16S_Libraries"
# seq_ID = "esakows1_132789"

path=file.path(base_path, seq_ID, "Demux")
fnFs <- sort(list.files(path, pattern="fastq", full.names = TRUE))
file_sizes_f = sort(sapply(fnFs, file.size), decreasing = T, na.last = NA)


fwdPNGname = file.path(base_path, seq_ID, "R1_quals.png")
revPNGname = file.path(base_path, seq_ID, "R2_quals.png")


to_plot_fwd=row.names(as.data.frame(file_sizes_f[c(1,3)]))
to_plot_rev=row.names(as.data.frame(file_sizes_f[c(6,8)]))

write("Two biggest files (in Kb) are:", stdout())
write(file_sizes_f[1], stdout())
write(file_sizes_f[3], stdout())

png(filename=fwdPNGname)
plotQualityProfile(to_plot_fwd)
dev.off()

png(filename=revPNGname)
plotQualityProfile(to_plot_rev)
dev.off()
