library(dada2)
seqtab <- readRDS("/data/sprehei1/Keith_Maeve1_138650/seqtab_nochim.rds")
ref_path = "/data/sprehei1/Keith_Maeve1_138650/Taxa_Refs/silva_nr_v128_train_set.fa.gz"
sp_ref_path = "/data/sprehei1/Keith_Maeve1_138650/Taxa_Refs/silva_species_assignment_v128.fa.gz"
tax <- assignTaxonomy(seqtab, ref_path, multithread=TRUE, minBoot=80, verbose=TRUE)
saveRDS(tax, "/data/sprehei1/Keith_Maeve1_138650/tax_nosp_final.rds")
tax.plus <- addSpecies(tax, sp_ref_path, verbose=TRUE, allowMultiple=TRUE)
saveRDS(tax.plus, "/data/sprehei1/Keith_Maeve1_138650/tax_sp_final.rds")
saveRDS(seqtab, "/data/sprehei1/Keith_Maeve1_138650/seqtab_final.rds")
