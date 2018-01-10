#library(dada2)
set.seed(100)

# command line arguments
args <- commandArgs(TRUE)

# read in location
base_path <- args[1]
seq_ID <- args[2]
trim_path = file.path(base_path, seq_ID, "Trim")

# get file & sample names & paths
pre_fnFs <- sort(list.files(trim_path, pattern="_F_filt.fastq"))
pre_fnRs <- sort(list.files(trim_path, pattern="_R_filt.fastq"))
sample.names <- sapply(strsplit(pre_fnFs, "_F_filt"), `[`, 1)
fnFs <- file.path(trim_path, pre_fnFs)
fnRs <- file.path(trim_path, pre_fnRs)
names(fnFs) <- sample.names
names(fnRs) <- sample.names

# make intermediate saved files
error_file_name_F = paste(substr(seq_ID, 1, 15), "errorsWS_F.RData", sep="_")
error_file_path_F = file.path(base_path, seq_ID, error_file_name_F)
error_file_name_R = paste(substr(seq_ID, 1, 15), "errorsWS_R.RData", sep="_")
error_file_path_R = file.path(base_path, seq_ID, error_file_name_R)

# fit error model
#errF <- learnErrors(fnFs, multithread=TRUE, randomize=TRUE)
#save(errF, file=error_file_path_F)
write(paste("Writing (F) errors to", error_file_name_F), stdout())

#errR <- learnErrors(fnRs, multithread=TRUE, randomize=TRUE)
#save(errR, file=error_file_path_R)
write(paste("Writing (R) errors to", error_file_name_R), stdout())

# dereplicate & call OTUs
dds <- vector("list", length(sample.names))
names(dds) <- sample.names

for(sam in sample.names) {
  cat("Processing:", sam, "\n")
#  derepF <- derepFastq(fnFs[[sam]])
#  derepR <- derepFastq(fnRs[[sam]])
#  ddF <- dada(derepF, err=errF, multithread=TRUE)
#  ddF <- dada(derepR, err=errR, multithread=TRUE)
#  merger <- mergePairs(ddF, derepF, ddR, derepR)
#  dds[[sam]] <- merger
}

#otu_tab_name = paste(substr(seq_ID, 1, 15), "raw_tab.RData", sep="_")
#otu_tab_path = file.path(base_path, seq_ID, otu_tab_name)
write(paste("Writing (R) errors to", otu_tab_path), stdout())
#save(dds, file=otu_tab_path)

#seq_tab_name = paste(substr(seq_ID, 1, 15), "seqtab_chim.rds", sep="_")
#seq_tab_path = file.path(base_path, seq_ID, seq_tab_name)             
#seqtab1 <- makeSequenceTable(dds)
#saveRDS(seqtab1, seq_tab_path)

#nochim_tab_name = paste(substr(seq_ID, 1, 15), "seqtab_nochim.rds", sep="_")
#nochim_tab_path = file.path(base_path, seq_ID, nochim_tab_name)
#seqtab2 <- removeBimeraDenovo(seqtab1, method="consensus", multithread=TRUE)
#saveRDS(seqtab2, nochim_tab_path)
