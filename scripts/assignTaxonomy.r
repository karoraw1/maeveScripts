library(dada2)
set.seed(100)
getN <- function(x) sum(getUniques(x))

# command line arguments
args <- commandArgs(TRUE)

# read in location
base_path <- args[1]
seq_ID <- args[2]
n_threads <- strtoi(args[3])
ref_path <- args[4]
sp_ref_path <- args[5]

#base_path = "/home-3/karoraw1@jhu.edu/scratch/16S_Libraries"
#seq_ID = "Miseq_data_SarahPreheim_Sept2016"
#data_path <- file.path(base_path, seq_ID)
#demux_path <- file.path(data_path, "Demux")

# location of seqtabs
data_path <- file.path(base_path, seq_ID)

# all four output file paths
nosp_path = file.path(data_path, paste(substr(seq_ID, 1, 15), "tax_nosp_final.rds", sep=""))
sp_path = file.path(data_path, paste(substr(seq_ID, 1, 15), "tax_sp_final.rds", sep=""))
final_tab_path = file.path(data_path, paste(substr(seq_ID, 1, 15), "seqtab_final.rds", sep=""))
track_path <- file.path(data_path, paste(substr(seq_ID, 1, 15), "read_loss.csv")

# locate & load two input files
chim_fname <- sort(list.files(data_path, pattern="_seqtab_chim.rds"))
nochim_fname <- sort(list.files(data_path, pattern="_seqtab_nochim.rds"))
chim_path <- file.path(data_path, chim_fname)
nochim_path <- file.path(data_path, nochim_fname)
seqtab <- readRDS(nochim_path)
seqtab.chim <- readRDS(chim_path)

# read in raw demuxed read counts 
temp_file_path <- file.path(data_path, "Demux", "read_count_x4.txt")
# process read count file into column and replace double star below 
# will need sorting

# create DataFrame of loss due to filtering, denoising, and tabling 
track <- cbind(**, rowSums(seqtab.chim), rowSums(seqtab))
colnames(track) <- c( "raw" , "filtered", "tabled" )
fnFs <- sort(list.files(demux_path, pattern="R1.fastq"))
if (length(fnFs) == 0) { fnFs <- sort(list.files(demux_path, pattern="R1_001.fastq"))}
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


