library(phyloseq)
library(dplyr)
library(ggplot2)
library(easyGgplot2)
library(devtools)
library(dada2)
library(seqinr)
set.seed(100)

setwd("~/Documents/maeveScripts")
samdf <- read.csv("data/sequencing_metadata_v2.csv", header = TRUE, sep = ",", 
			      quote = "\"",dec = ".", fill = TRUE, comment.char = "", row.names=1)
taxa <- readRDS("data/tax_nosp_final.rds")
seqtab <- readRDS("data/seqtab_nochim.rds")
sd <- sample_data(samdf)

ps <- phyloseq(otu_table(seqtab, taxa_are_rows=FALSE), sd, tax_table(taxa))
small_samples = c("AAGGAACG", "CCGCACCG", "CGAATATT")
not_controls <- rownames(sd[sd[,"Control"] != TRUE])
big_not_controls <- not_controls[! not_controls %in% small_samples]

ps.exp <- prune_samples(big_not_controls, ps) %>% prune_taxa(taxa_sums(.) > 0, .)

find a taxa-specific sequences
tt_df = as.data.frame(tax_table(ps.exp))
"Desulfobacterales" %in% tt_df$Order
"Desulfobulbaceae" %in% tt_df$Family
desul_df = subset(tt_df, Family == "Desulfobulbaceae")
desul_seqs = as.list(rownames(desul_df))
otu_df = as.data.frame(as(otu_table(ps.exp), "matrix"))
desul_abund <- otu_df[,colnames(otu_df) %in% desul_seqs]
otu_tab_d_s = otu_df[rowSums(desul_abund) > 0, ]
desul_d_s = desul_abund[rowSums(desul_abund) > 0, ]
pct_desul_nz = rowSums(desul_d_s) / rowSums(otu_tab_d_s)
sam_df = as.data.frame(samdf)
desul_sam_df = sam_df[rownames(sam_df) %in% names(pct_desul_nz),]
desul_depth_abund = cbind(desul_sam_df$Depth, pct_desul_nz)
colnames(desul_depth_abund) = c("Depth", "Pct.cable.bacteria")
dda = as.data.frame(desul_depth_abund)
ggplot2.violinplot(data=dda, xName='Depth', yName="Pct.cable.bacteria", groupName='Depth', brewerPalette="Paired")
write.fasta(desul_seqs, c(1:482), "data/chesapeake_desulf.fasta", open = "w", nbchar = 60, as.string = FALSE)