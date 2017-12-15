# -*- coding: utf-8 -*-

import pandas as pd

summary_file = "Sampling_processing_worksheet_120117.xlsx"
summary_sheet = pd.read_excel(summary_file)

# These are some initial questions that need filling in
## "13 samples have ?? as there short name"
## "How do you translate BioSampleID into Sample ID into information?"
## "Shouldn't controls get sample dates?"
## "What is going on with 266 - 285"
## "I need to enter my data"
## "I need to find samples that I qubited but didn't sequence"
## Changed sample names on index 520 to 563 (they all had June 1st as the date) 

new_data = "../data/sequencing_metadata_v2.csv"
new_df = pd.read_csv(new_data)
new_df_cmp = new_df.ix[:, ["Date", "Sample String", 'Station']]
sum_df_cmp = summary_sheet.ix[:, ["Short sample name","DateMMDDYY", "StationName"]]
sum_df_cmp = sum_df_cmp[sum_df_cmp.DateMMDDYY.notnull()]
sum_df_cmp.DateMMDDYY = sum_df_cmp.DateMMDDYY.astype(int).astype(str)

def transform_date(mmddyy):
    mm, dd, yy = mmddyy.split("/")
    return mm+dd+yy
    
new_df_cmp = new_df_cmp[new_df_cmp.Date.notnull()]
new_df_cmp.Date = new_df_cmp.Date.apply(transform_date)
    
                        
new_new_idx = ["New"+str(i) for i in new_df_cmp.index]
new_sum_idx = ["Old"+str(k) for k in sum_df_cmp.index]
new_df_cmp.index = new_new_idx
sum_df_cmp.index = new_sum_idx

sum_cols = sum_df_cmp.columns.tolist()
sum_cols = [sum_cols[1], sum_cols[0], sum_cols[-1]]
sum_df_cmp = sum_df_cmp[sum_cols]
sum_df_cmp.columns = new_df_cmp.columns

def dedot(cbnum):
    cb = cbnum.split(".")
    return cb[0]+cb[1]

new_df_cmp.Station = new_df_cmp.Station.apply(dedot)
mix_df = pd.concat([sum_df_cmp, new_df_cmp])
sorted_mix = mix_df.sort_values(["Date", "Station"])




