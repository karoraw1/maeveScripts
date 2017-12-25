#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:25:38 2017

@author: login
"""

import pandas as pd
import numpy as np
import os

new_master_f = '../data/Sampling_processing_worksheet_121217.xlsx'
print "Metadata sheet exists:", os.path.exists(new_master_f)


base_data_path = '/data/sprehei1/Raw_data_group/'

sheets = ['esakows1_132789',
          'Keith_Maeve1_138650',
          'Miseq_data_SarahPreheim_Sept2016',
          'sprehei1_122704']

reseq_files = ['sprehei1_123382']

data_dirs = os.listdir(base_data_path)

for i in (sheets+reseq_files):
    for j in data_dirs:
        if i in j:
            print "{} detected".format(i)

#metadata_df = pd.read_excel(new_master_f)
#print "\tShape is:", metadata_df.shape
