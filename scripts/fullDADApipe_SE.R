library(dada2)

# command line arguments
args <- commandArgs(TRUE)

# read in location
base_path <- args[1]
seq_ID <- args[2]
fname_spacer <- args[3]
trim_path = file.path(base_path, seq_ID, "Trim")


pre_fnFs <- sort(list.files(trim_path, pattern=".fastq"))
sample.names <- sapply(strsplit(pre_fnFs, "[.]"), `[`, 1)
fnFs <- file.path(trim_path, pre_fnFs)
names(fnFs) <- sample.names
error_file_name = paste(substr(seq_ID, 1, 15), "errorsWS.RData", sep="_")
error_file_path = file.path(base_path, seq_ID, error_file_name)
set.seed(100)

write(error_file_path, stdout())
write(length(pre_fnFs), stdout())

err <- learnErrors(fnFs, multithread=TRUE, randomize=TRUE)
save(err, file=error_file_path)


dds <- vector("list", length(sample.names))
names(dds) <- sample.names

for(sam in sample.names) {
  cat("Processing:", sam, "\n")
  derep <- derepFastq(fnFs[[sam]])
  dds[[sam]] <- dada(derep, err=err, multithread=TRUE)
}

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

otu_tab_name = paste(substr(seq_ID, 1, 15), "raw_tab.RData", sep="_")
otu_tab_path = file.path(base_path, seq_ID, otu_tab_name)
write(paste("Writing (R) errors to", otu_tab_path), stdout())
save(dds, file=otu_tab_path)

seq_tab_name = paste(substr(seq_ID, 1, 15), "seqtab_chim.rds", sep="_")
seq_tab_path = file.path(base_path, seq_ID, seq_tab_name)
seqtab1 <- makeSequenceTable(dds)
saveRDS(seqtab1, seq_tab_path)

nochim_tab_name = paste(substr(seq_ID, 1, 15), "seqtab_nochim.rds", sep="_")
nochim_tab_path = file.path(base_path, seq_ID, nochim_tab_name)
seqtab2 <- removeBimeraDenovo(seqtab1, method="consensus", multithread=TRUE)
saveRDS(seqtab2, nochim_tab_path)
