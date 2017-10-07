library(dada2)

# Load Sample Names
path <- "/data/sprehei1/Keith_Maeve1_138650/Truncated_Fastq_4"
pre_fnFs <- sort(list.files(path, pattern=".fastq"))
sample.names <- sapply(strsplit(pre_fnFs, "[.]"), `[`, 1)
filt_path <- "/data/sprehei1/Keith_Maeve1_138650/Filtered_Fastq_5"
fnFs <- file.path(filt_path, paste0(sample.names, ".filt.fastq"))
names(fnFs) <- sample.names

set.seed(100)

# Load error rate
load("/home-3/karoraw1@jhu.edu/work/sprehei1/Keith_Files/maeveScripts/errorsWS.RData")

dds <- vector("list", length(sample.names))

for(sam in sample.names) {
  cat("Processing:", sam, "\n")
  derep <- derepFastq(fnFs[[sam]])
  dds[[sam]] <- dada(derep, err=err, multithread=TRUE)
}

seqtab <- makeSequenceTable(dds)
saveRDS(seqtab, "/data/sprehei1/Keith_Maeve1_138650/seqtab.rds")

