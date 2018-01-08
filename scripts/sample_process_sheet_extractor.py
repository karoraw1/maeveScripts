#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:25:38 2017

This is a script specifically designed to parse
the sample processing sheet Excel file used by
our lab. It creates the files needed for the 
general purpose pipeline.

@author: Keith Arora-Williams
"""

import copy
import pandas as pd
import numpy as np
import os
import sys
from Bio.Seq import Seq

write_directory="/home-3/karoraw1@jhu.edu/scratch/16S_Libraries"

def rev_comp_col(a_string):
    return str(Seq(a_string).reverse_complement())

def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0

def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return file_info.st_size

print "\nDetecting data locations"
print "------------------------"

base_data_path = '/data/sprehei1/Raw_data_group/'
sheets = ['esakows1_132789',
          'Keith_Maeve1_138650',
          'MiSeq_data_SarahPreheim_Sept16',
          'sprehei1_122704']
reseq_files = ['sprehei1_123382']
directories = copy.copy(sheets+reseq_files)
directories[2] = 'Miseq_data_SarahPreheim_Sept2016'

seqIDtoFileDict, total_size = {}, 0 
for i in directories:
    seqIDtoFileDict[i] = []
    full_dir_path = os.path.join(base_data_path, i)
    print "DIR: {} detected".format(i)
    for f in os.listdir(full_dir_path):
        full_file_path = os.path.join(full_dir_path, f)
        if ".fastq" in f:
            seqIDtoFileDict[i].append(full_file_path)
            this_size = file_size(full_file_path)
            #print "\t{} : {}".format(f, convert_bytes(this_size)) 
            total_size += this_size
        elif ".txt" in f:
            seqIDtoFileDict[i].append(full_file_path)

print "All sequence files total {}\n".format(convert_bytes(total_size))

print "Reading metadata file"
print "---------------------"

new_master_f = '../data/Sampling_processing_worksheet_121217.xlsx'
print "Metadata sheet exists:", os.path.exists(new_master_f)

for idx, sht in enumerate(sheets):
    metadata_df = pd.read_excel(new_master_f, sht)
    print "Sheet {} has {} cols/rows".format(sht, metadata_df.shape)

    # This section adds entries to the metadata df corresponding
    # to resequenced files.
    resequences = metadata_df.Resequencingfiles.notnull()
    print "\tNumber of resequencing entries:", resequences.sum()
    if resequences.sum() > 0:
        entries_to_duplicate = metadata_df.ix[resequences, :].copy()
        reseq = entries_to_duplicate.Resequencingfiles.values[0]
        sames = (entries_to_duplicate.Resequencingfiles == reseq).sum()
        print "\tNo. of entries equal to {}: {}".format(reseq, sames)
        empty_filler = [""]*resequences.sum()
        entries_to_duplicate.ix[:, "Resequencingfiles"] = empty_filler
        entries_to_duplicate.ix[:, "sequencingfileindexname"] = empty_filler
        entries_to_duplicate.ix[:, "sequencingfilereversename"] = empty_filler
        entries_to_duplicate.ix[:, "sequencingfileforwardname"] = empty_filler
        entries_to_duplicate.ix[:, "datafoldername"] = empty_filler
        entries_to_duplicate.ix[:, "sequencingID"] = [reseq]*resequences.sum()
        entries_to_duplicate.ix[:, '#SampleID'] = [i+"_RSQ" for i in entries_to_duplicate.ix[:, '#SampleID'].tolist()]
        metadata_df = metadata_df.append(entries_to_duplicate, ignore_index=True)

    if idx == 0:
        super_map = metadata_df.copy()
    else:
        super_map = super_map.append(metadata_df, ignore_index=True)
        
super_map.drop(["2ndstepbarcodesequence.1"], axis=1, inplace=True)

sampleIDcheck = np.unique(super_map.ix[:, '#SampleID'].tolist())

print "\nFull metadata df is: {} with {} unique sample names".format( super_map.shape, len(sampleIDcheck))

seqIDs = super_map.sequencingID.unique()

super_map.ix[:, "Demultiplexed"] = [False] * super_map.shape[0]
super_map.ix[:, "DemuxFileRoot"] = [""] * super_map.shape[0]

col_keys = ["Fwd", "Rev", "Idx", "Map", "Barcodes", "Demuxed", "ReadTypes"]
demux_df = pd.DataFrame(index=seqIDs, columns=col_keys)

for sID in seqIDs:
    sid_bool = super_map.sequencingID == sID
    if sID == 'Miseq_data_SarahPreheim_Sept2016':
        super_map.ix[sid_bool, "Demultiplexed"] = [ True ] * sid_bool.sum()
        super_map.ix[sid_bool, "DemuxFileRoot"] = [ i.split("R1")[0] for i in super_map.ix[sid_bool, "sequencingfileforwardname"].tolist() ] 
        super_map.ix[sid_bool, "sequencingfileindexname"] = [""] * sid_bool.sum()
        super_map.ix[sid_bool, "sequencingfilereversename"] = ["R2_001.fastq"] * sid_bool.sum() 
        super_map.ix[sid_bool, "sequencingfileforwardname"] = ["R1_001.fastq"] * sid_bool.sum()
    
    sid_subdf = super_map.ix[sid_bool, :]
        
    files_n = [os.path.basename(i) for i in seqIDtoFileDict[sID]]
    maps_n = [i for i in files_n if ".txt" in i]
    seqs_n = [i for i in files_n if ".fast" in i]

    if sID != 'Miseq_data_SarahPreheim_Sept2016':
        sid_fwd = sid_subdf.sequencingfileforwardname.unique()[0]
        sid_rev = sid_subdf.sequencingfilereversename.unique()[0]
        sid_idx = sid_subdf.sequencingfileindexname.unique()[0]
        sid_map = sid_subdf.mappingfilename.unique()[0]
    else:
        sid_fwd = "*R1_001.fastq"
        sid_rev = "*R2_001.fastq"
        sid_idx = ""
        sid_map = ""

    demuxed_bool = sid_subdf.Demultiplexed.unique()[0]
    print "\nSequence ID: {}".format(sID)
    print "\tDemultiplexed?: {}".format(demuxed_bool)

    if not demuxed_bool:
        bcode_file_name = os.path.abspath("../data/" + sID + "_barcodes.txt")
        barcode_cols = set(['#SampleID', '2ndstepbarcodesequence'])
        not_barcodes = set(list(super_map.columns)) - barcode_cols
        barcode_data = sid_subdf.drop(list(not_barcodes), axis=1)
        barcode_data.ix[:, "2ndstepbarcodesequence"] = barcode_data.ix[:, "2ndstepbarcodesequence"].apply(rev_comp_col)
        barcode_data.to_csv(bcode_file_name, sep="\t", index=False, header=False)
        print "\tBarcode File: {}".format(bcode_file_name)

    detectors = []
    candidates = [sid_fwd, sid_rev, sid_idx, sid_map, bcode_file_name, demuxed_bool, "PE"]    
    for idx, col_k, candi in zip(range(7), col_keys, candidates):
        if candi in seqs_n or candi in maps_n:
            detectors.append(True)
            this_file = [i for i in files_n if candi in i]
            assert len(this_file) == 1
            demux_df.ix[sID, col_k] = this_file[0]
        elif col_k == "Barcodes" and not demuxed_bool:
            demux_df.ix[sID, col_k] = bcode_file_name
        elif col_k == "Demuxed":
            demux_df.ix[sID, col_k] = candi
        elif col_k == "ReadTypes":
            demux_df.ix[sID, col_k] = candi
        else:
            detectors.append(False)
            demux_df.ix[sID, col_k] = candi

    print "Files Expected:"
    print "\t Fwd file: {} ( Exists: {})".format(sid_fwd, detectors[0])
    print "\t Rev file: {} ( Exists: {})".format(sid_rev, detectors[1])
    print "\t Idx file: {} ( Exists: {})".format(sid_idx, detectors[2])
    print "\t Map files: {} ( Exists: {})".format(sid_map, detectors[3])
    print "Files discovered:"
    print "\t Maps: {}".format(len(maps_n))
    print "\t Seqs: {}".format(len(seqs_n)) 

    if sID == "sprehei1_123382":
        potential_fwd = [i for i in seqs_n if "_R1_" in i][0]
        potential_rev = [i for i in seqs_n if "_R2_" in i][0]
        potential_idx = [i for i in seqs_n if "_I1_" in i][0]
        fwd_path = [i for i in files_n if potential_fwd in i][0]
        rev_path = [i for i in files_n if potential_rev in i][0]
        idx_path = [i for i in files_n if potential_idx in i][0]
        demux_df.ix[sID, "Fwd"] = fwd_path
        demux_df.ix[sID, "Rev"] = rev_path
        demux_df.ix[sID, "Idx"] = idx_path


seqIDs2 = ['esakows1_132789', 'Keith_Maeve1_138650', 'Miseq_data_SarahPreheim_Sept2016', 'sprehei1_122704', 'sprehei1_123382']
checkHead = [True, True, False, True, True]
fixHead = [False, False, False, True, False]
check_srs = pd.Series(checkHead, index=seqIDs2)
fix_srs = pd.Series(fixHead, index=seqIDs2)
demux_df.loc[:, "CheckHeaders"] = check_srs
demux_df.loc[:, "FixHeaders"] = fix_srs
demux_df.to_csv("../data/mapping_file.tsv", sep="\t")

