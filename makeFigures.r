library(phyloseq)
library(dplyr)
library(ggplot2)
library(dada2)
set.seed(100)
# 
setwd("~/Documents/maeveScripts")
samdf <- read.csv("data/sequencing_metadata.csv", header = TRUE, sep = ",", 
			      quote = "\"",dec = ".", fill = TRUE, comment.char = "", row.names=1)
taxa <- readRDS("data/tax_nosp_final.rds")
seqtab <- readRDS("data/seqtab_nochim.rds")
sd <- sample_data(samdf)

ps <- phyloseq(otu_table(seqtab, taxa_are_rows=FALSE), sd, tax_table(taxa))
small_samples = c("AAGGAACG", "CCGCACCG", "CGAATATT")
not_controls <- rownames(sd[sd[,"Control"] != TRUE])
big_not_controls <- not_controls[! not_controls %in% small_samples]

ps.exp <- prune_samples(big_not_controls, ps) 
ps.bac <- ps.exp %>% subset_taxa(Kingdom == "Bacteria" & Family  != "mitochondria" & Class   != "Chloroplast")
ps.rar.bac <- rarefy_even_depth(ps.bac, rngseed=100)
ps.rar.2016 <- ps.rar.bac %>% subset_samples(Year == 2016) %>% prune_taxa(taxa_sums(.) > 0, .)

alpha_path = "data/alpha_diversity.png"
png(alpha_path, width = 800, height = 480)
plot_richness(ps.rar.2016, x="Station.Number", measures=c("Shannon"), color="Month") + theme_bw(base_size = 18)
dev.off()

beta_path = "data/pca_of_beta_diversity.png"
ord.pcoa.bray <- ordinate(ps.rar.2016, method="PCoA", distance="bray")
png(beta_path, width = 600, height = 600)
plot_ordination(ps.rar.2016, ord.pcoa.bray, color="Station", title="PCA of Bray Distances") + theme_bw(base_size = 18)
dev.off()


ps.33c <- ps.rar.bac %>% subset_samples(Station == "CB3.3C") %>% prune_taxa(taxa_sums(.) > 0, .)
topSp <- names(sort(taxa_sums(ps.33c), decreasing=TRUE))[1:30]
ps.topSp <- transform_sample_counts(ps.33c, function(OTU) OTU/sum(OTU))
ps.topSp <- prune_taxa(topSp, ps.topSp)
taxa_fig_path = "data/taxaBreakdown_by_year.png"
png(taxa_fig_path, width = 800, height = 600)
plot_bar(ps.topSp, x="Depth", fill="Order") + facet_wrap(~Year, scales="free_x") + theme_bw(base_size = 18)
dev.off()

taxa_tab_path = "data/top_species_names.csv"
topSp_df = as.data.frame(taxa[topSp, ], row.names=1)
topSp_df_nr = topSp_df[!duplicated(topSp_df), ]
write.csv(topSp_df_nr, taxa_tab_path, row.names=FALSE)
