library(dada2)
set.seed(100)

# command line arguments
args <- commandArgs(TRUE)

# read in location
base_path <- args[1]
seq_ID <- args[2]
fwd_ID <- args[3]
sample_splitter <- args[4]
n_threads <- strtoi(args[5])
trim_path = file.path(base_path, seq_ID, "Trim")

# get file & sample names & paths
pre_fnFs <- sort(list.files(trim_path, pattern=fwd_ID))
sample.names <- sapply(strsplit(pre_fnFs, sample_splitter), `[`, 1)
n_l = nchar(sample.names[1])
spacer = substr(sample.names[1], n_l, n_l)
fnFs <- file.path(trim_path, pre_fnFs)
names(fnFs) <- sample.names

# make intermediate saved files
error_file_name_F = paste(substr(seq_ID, 1, 15), spacer, "errorsWS.RData", sep="_")
error_file_path_F = file.path(base_path, seq_ID, error_file_name_F)

# fit error model
write(paste("Start Errors (1)", Sys.time() ), stdout())
errF <- learnErrors(fnFs, multithread=n_threads, randomize=TRUE)
save(errF, file=error_file_path_F)
write(paste("Writing errors to", error_file_name_F), stdout())

# dereplicate & call OTUs
dds <- vector("list", length(sample.names))
names(dds) <- sample.names

for(sam in sample.names) {
   cat("Processing:", sam, "\n")
   write(paste("Start Derep", Sys.time() ), stdout())
   derepF <- derepFastq(fnFs[[sam]])
   write(paste("Start DADA", Sys.time() ), stdout())
   dds[[sam]] <- dada(derepF, err=errF, multithread=n_threads)
}

otu_tab_name = paste(substr(seq_ID, 1, 15), spacer, "raw_tab.RData", sep="_")
otu_tab_path = file.path(base_path, seq_ID, otu_tab_name)
write(paste("Finished DADA", Sys.time() ), stdout())
write(paste("Writing raw table to", otu_tab_path), stdout())
save(dds, file=otu_tab_path)

seq_tab_name = paste(substr(seq_ID, 1, 15), spacer, "seqtab_chim.rds", sep="_")
seq_tab_path = file.path(base_path, seq_ID, seq_tab_name)             
seqtab1 <- makeSequenceTable(dds)
write(paste("Finished Seq table", Sys.time() ), stdout())
write(paste("Writing seq table to", seq_tab_path), stdout())
saveRDS(seqtab1, seq_tab_path)

nochim_tab_name = paste(substr(seq_ID, 1, 15), spacer, "seqtab_nochim.rds", sep="_")
nochim_tab_path = file.path(base_path, seq_ID, nochim_tab_name)
seqtab2 <- removeBimeraDenovo(seqtab1, method="consensus", multithread=n_threads)
write(paste("Finished Chimera Checking", Sys.time() ), stdout())
write(paste("Writing dechimera'd table to", nochim_tab_path), stdout())
saveRDS(seqtab2, nochim_tab_path)
