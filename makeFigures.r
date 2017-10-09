library(ggplot2)
library(dada2)
library(phyloseq)

# 

read.csv(file, header = TRUE, sep = ",", quote = "\"",dec = ".", fill = TRUE, comment.char = "")

taxa <- readRDS("/data/sprehei1/Keith_Maeve1_138650/tax_nosp_final.rds")
seqtab <- readRDS("/data/sprehei1/Keith_Maeve1_138650/seqtab_nochim.rds")
ps <- phyloseq(otu_table(seqtab, taxa_are_rows=FALSE), sample_data(samdf), 
               tax_table(taxa))



