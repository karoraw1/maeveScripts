#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 12:34:08 2017

@author: login
"""

import pandas as pd
import numpy as np

wq_data = "data/WaterQualityParamsByStation2016.tsv"
md_data = 'data/sequencingMetadata.csv'

wq_df = pd.read_csv(wq_data, sep="\t", parse_dates=[8, 9], 
                    infer_datetime_format=True)

kept_cols = ['Station', 'SampleDate', 'SampleTime', 'TotalDepth', 
             'UpperPycnocline', u'LowerPycnocline', u'Depth', u'Parameter', 
             'MeasureValue']
             
# index by station & date (either day or week) & depth (?)

md_df = pd.read_csv( md_data, index_col=0, parse_dates=[16])


# 
