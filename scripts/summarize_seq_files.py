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

new_master_f = '../data/Sampling_processing_worksheet_121217.xlsx'
print "Metadata sheet exists:", os.path.exists(new_master_f)

base_data_path = '/data/sprehei1/Raw_data_group/'

sheets = ['esakows1_132789',
          'Keith_Maeve1_138650',
          'Miseq_data_SarahPreheim_Sept16',
          'sprehei1_122704']

reseq_files = ['sprehei1_123382']
directories = copy.copy(sheets+reseq_files)
directories[2] = 'Miseq_data_SarahPreheim_Sept2016'

seq_pool, map_pool = [], []

for i in directories:
    full_dir_path = os.path.join(base_data_path, i)
    print "DIR: {}".format(i)
    for f in os.listdir(full_dir_path):
        full_file_path = os.path.join(full_dir_path, f)
        if ".fastq" in f:
            seq_pool.append(full_file_path)
        elif ".txt" in f:
            map_pool.append(full_file_path)

for idx, sht in enumerate(sheets):
    metadata_df = pd.read_excel(new_master_f, sheet_name=sht)
    print "Sheet {} has {} cols/rows".format(sht, metadata_df.shape)
    # pick columns with relavent info
    if idx == 0:
        super_map = metadata_df.copy()
    else:
        final_super_map = super_map.append(metadata_df)
        
print "\tShape is: {}", final_super_map.shape
