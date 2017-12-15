#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:25:38 2017

@author: login
"""

import pandas as pd
import numpy as np
import os

new_master_f = 'Sampling_processing_worksheet_121217.csv'
print "Metadata sheet exists:", os.path.exists(new_master_f)
metadata_df = pd.read_csv(new_master_f, parse_dates=False)
print "\tShape is:", metadata_df.shape

print metadata_df.columns
