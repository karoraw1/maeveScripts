library(dada2)

# command line arguments
args <- commandArgs(TRUE)

# read in location
base_path <- args[1]
seq_ID <- args[2]
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
