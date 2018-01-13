library(dada2)
set.seed(100)
getN <- function(x) length(derepFastq(x)$uniques)

# command line arguments
args <- commandArgs(TRUE)

# read in location
base_path <- args[1]
seq_ID <- args[2]
n_threads <- strtoi(args[3])
ref_path <- args[4]
sp_ref_path <- args[5]

# location of seqtabs & files
data_path <- file.path(base_path, seq_ID)
demux_path <- file.path(data_path, "Demux")
trim_path <- file.path(data_path, "Trim")

# all four output file paths
nosp_path = file.path(data_path, paste(substr(seq_ID, 1, 15), "tax_nosp_final.rds", sep="_"))
sp_path = file.path(data_path, paste(substr(seq_ID, 1, 15), "tax_sp_final.rds", sep="_"))
final_tab_path = file.path(data_path, paste(substr(seq_ID, 1, 15), "seqtab_final.rds", sep="_"))
track_path <- file.path(data_path, paste(substr(seq_ID, 1, 15), "read_loss.csv", sep="_"))

# locate & load two input files
chim_fname <- sort(list.files(data_path, pattern="_seqtab_chim.rds"))
nochim_fname <- sort(list.files(data_path, pattern="_seqtab_nochim.rds"))
chim_path <- file.path(data_path, chim_fname)
nochim_path <- file.path(data_path, nochim_fname)
seqtab <- readRDS(nochim_path)
seqtab.chim <- readRDS(chim_path)

fnFs <- sort(list.files(demux_path, pattern="R1.fastq"))
if (length(fnFs) == 0) { fnFs <- sort(list.files(demux_path, pattern="R1_001.fastq"))}
dmux_paths = file.path(demux_path, fnFs)
fnTFs <- sort(list.files(trim_path, pattern="_F_filt.fastq"))
trim_paths = file.path(trim_path, fnTFs)
dmux_col = sapply(dmux_paths, getN)
trim_col = sapply(trim_paths, getN)
track <- cbind(dmux_col, trim_col, rowSums(seqtab.chim), rowSums(seqtab))
colnames(track) <- c("raw", "filtered", "tabled", "denoised")
sample.names <- sapply(strsplit(fnFs, "[.]"), `[`, 1)
rownames(track) <- sample.names
trackdf = data.frame(track)
# write it to disk
write.csv(trackdf, track_path)

# call taxonomy
tax <- assignTaxonomy(seqtab, ref_path, multithread=n_threads, minBoot=80, verbose=TRUE)
saveRDS(tax, nosp_path)
tax.plus <- addSpecies(tax, sp_ref_path, verbose=TRUE, allowMultiple=TRUE)
saveRDS(tax.plus, sp_path)
saveRDS(seqtab, final_tab_path)


