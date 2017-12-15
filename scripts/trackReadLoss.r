library(dada2)
load("/data/sprehei1/Keith_Maeve1_138650/raw_otu_table.RData")
seqtab <- readRDS("/data/sprehei1/Keith_Maeve1_138650/seqtab_nochim.rds")
seqtab.chim <- readRDS("/data/sprehei1/Keith_Maeve1_138650/seqtab_chim.rds")
getN <- function(x) sum(getUniques(x))
track <- cbind(sapply(dds, getN), rowSums(seqtab.chim), rowSums(seqtab))
colnames(track) <- c( "denoised" , "tabled", "nonchim" )
path <- "/data/sprehei1/Keith_Maeve1_138650/Truncated_Fastq_4"
pre_fnFs <- sort(list.files(path, pattern=".fastq"))
sample.names <- sapply(strsplit(pre_fnFs, "[.]"), `[`, 1)
rownames(track) <- sample.names
trackdf = data.frame(track)
track_path <- "/home-3/karoraw1@jhu.edu/work/sprehei1/Keith_Files/maeveScripts/read_loss.csv"
write.csv(trackdf, track_path)
