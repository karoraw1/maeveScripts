#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:25:38 2017

@author: login
"""

import copy
import pandas as pd
import numpy as np
import os

write_directory="/home-3/karoraw1@jhu.edu/scratch/16S_Libraries"

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
        metadata_df = metadata_df.append(entries_to_duplicate, ignore_index=True)

    if idx == 0:
        super_map = metadata_df.copy()
    else:
        super_map = super_map.append(metadata_df, ignore_index=True)
        
print "\nFull metadata df is: {}".format( super_map.shape )

seqIDs = super_map.sequencingID.unique()

super_map.ix[:, "Demultiplexed"] = [False] * super_map.shape[0]
super_map.ix[:, "DemuxFileRoot"] = [""] * super_map.shape[0]

for sID in seqIDs:
    sid_bool = super_map.sequencingID == sID
    sid_subdf = super_map.ix[sid_bool, :]
    if sID == 'Miseq_data_SarahPreheim_Sept2016':
        super_map.ix[sid_bool, "Demultiplexed"] = [ True ] * sid_subdf.shape[0]
        super_map.ix[sid_bool, "DemuxFileRoot"] = [ i.split("R1")[0] for i in super_map.ix[sid_bool, "sequencingfileforwardname"].tolist() ] 
        super_map.ix[sid_bool, "sequencingfileindexname"] = [""] * sid_subdf.shape[0]
        super_map.ix[sid_bool, "sequencingfilereversename"] = [""] * sid_subdf.shape[0] 
        super_map.ix[sid_bool, "sequencingfileforwardname"] = [""] * sid_subdf.shape[0]

    sid_fwd = sid_subdf.sequencingfileforwardname.unique()
    sid_rev = sid_subdf.sequencingfilereversename.unique()
    sid_idx = sid_subdf.sequencingfileindexname.unique()
    sid_map = sid_subdf.mappingfilename.unique()
    
    print "\nSequence ID: {}".format(sID)
    print "Files Expected:"
    print "\t Seq files:", (len(sid_fwd) + len(sid_rev))
    print "\t Idx files:", sid_idx
    print "\t Map files:", sid_map
    print "Files discovered:"
    print "\t", [os.path.basename(i) for i in seqIDtoFileDict[sID]]
