#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 10:18:46 2017

@author: login
"""

import pandas as pd
import numpy as np
import sys

# write out edited version to this name
new_master_f = 'Sampling_processing_worksheet_121217.csv'

# original sample sheet to edit
master_f = 'Sampling_processing_worksheet_120117.csv'
old_master = pd.read_csv(master_f, parse_dates=False)
new_master = old_master.copy()

# manually filled out record for example
filled_sample = old_master.ix[604, :].copy()

# manually prepared matching records 
matches_f = 'placed_new_vals.csv'
new_df = pd.read_csv(matches_f)
new_df_clean = new_df[new_df.ix[:, 'New Index'].notnull()]
                      
# qpcr values for samples not sequenced
not_seqd_f = '../data/NotSequenced.xlsx'
not_seq_df = pd.read_excel(not_seqd_f)

# qpcr, qubit, cycle number 
seqd_f = '../data/sequencing_metadata_v2.csv'
seqd_df = pd.read_csv(seqd_f, parse_dates=False)

def find_match(new_sample_string, old_df):
    unfilled_match = new_df.ix[ : , 'New Sample String' ] == new_sample_string
    assert unfilled_match.sum() == 1
    corresponding_name = new_df[unfilled_match]['Sample String'].values[0]
    unfilled_rec_num = old_df.ix[ : , 'Short sample name' ] == corresponding_name
    assert unfilled_rec_num.sum() == 1
    unfilled_idx = old_df[unfilled_rec_num].index[0]
    return unfilled_idx
    
    
def find_seqd_match(new_name, seq_df):
    mask = seq_df.ix[:, 'Sample String'] == new_name
    return seq_df[mask].index[0]
    
columns_to_fill_ns = ['Short sample name', 'qPCR date','qPCR ct', 'qPCR ID', 
                      'qubit date', 'qubit ID', 'qubit notes']
columns_to_fill_seq = ['qPCR date', 'qPCR ID', 'qPCR notes', '1st step date',
                       '1st step plate', '1st step cycle notes',
                       'cleanup date', 'cleanup  type', 'cleanup notes',
                       '2nd step date', '2nd step cycle no',
                       '2nd step clean up date', '2nd step clean up initials',
                       'Multiplex date', 'Multiplex initials', 'sequencing date',
                       'sequencing platform', 'sequencing length',
                       'sequencing reads', 'data folder name',
                       'sequencing file forward name', 
                       'sequencing file reverse name',
                       'sequencing file index name']
                       
specific_columns = ['qPCR ct', '1st step cycle number', '2nd step barcode']
specific_data = ['qPCR Cq', 'Cycles', 'Barcode Well ']

qpcr_date = filled_sample['qPCR date']
qpcr_id = filled_sample['qPCR ID']
qubit_date = '7/11/17'
qubit_ID = 'MS'
qi = 'Qubit Initial'
counter = 0

for idx in new_df_clean.index:
    this_n_i = new_df.ix[idx,'New Index']
    # check if ns
    if this_n_i.startswith("NS"):
        counter +=1
        ns_idx = int(this_n_i[2:])-1
        old_name = new_df.ix[idx, 'Sample String']
        qpcr_ct = not_seq_df.ix[ns_idx, 'Ct']
        new_name = new_df.ix[idx, 'New Sample String']
        print "\n", ns_idx, new_name
        assert new_name == not_seq_df.ix[ns_idx, 'Sample String']
        qubit_notes = not_seq_df.ix[ns_idx, 'Qubit']
        
        us_idx = find_match(new_name, old_master)
        
        new_master.ix[us_idx, 'qPCR date'] = qpcr_date
        new_master.ix[us_idx, 'qPCR ID'] = qpcr_id
        new_master.ix[us_idx, 'qPCR ct'] = qpcr_ct
        if not np.isnan(qubit_notes):
            new_master.ix[us_idx, 'qubit date' ] = qubit_date
            new_master.ix[us_idx, 'qubit ID' ] = qubit_ID
            new_master.ix[us_idx, 'qubit notes'] = qubit_notes
        else:
            new_master.ix[us_idx, 'qubit date' ] = old_master.ix[us_idx, 'qubit date' ]
            new_master.ix[us_idx, 'qubit ID' ] = old_master.ix[us_idx, 'qubit ID' ]
            new_master.ix[us_idx, 'qubit notes'] = np.nan
        print new_master.ix[us_idx, columns_to_fill_ns]

    elif this_n_i.startswith("New"):
        counter += 1
        #if counter == 2:
        #    sys.exit()
        old_name = new_df.ix[idx, 'Sample String']
        new_name = new_df.ix[idx, 'New Sample String']
        s_idx = find_seqd_match(new_name, seqd_df)
        print "\n", s_idx, new_name
        us_idx = find_match(new_name, old_master)
        
        assert new_name == seqd_df.ix[s_idx, 'Sample String']
        # fill invariant columns
        for iv_c in columns_to_fill_seq:
            filler = filled_sample[iv_c]
            new_master.ix[us_idx, iv_c] = filler
        # fill specific columns
        for sc, sd in zip(specific_columns, specific_data):
            datum = seqd_df.ix[s_idx, sd]
            print "Cheep", sc, sd, datum
            new_master.ix[us_idx, sc] = datum
        
        if not np.isnan(seqd_df.ix[s_idx, qi]):
            new_master.ix[us_idx, 'qubit date' ] = qubit_date
            new_master.ix[us_idx, 'qubit ID' ] = qubit_ID
            new_master.ix[us_idx, 'qubit notes'] = seqd_df.ix[s_idx, qi]
        

        #print new_master.ix[us_idx, :]
        

forward_name = 'Undetermined_S0_L001_R1_001.fastq.gz'
reverse_name = 'Undetermined_S0_L001_R2_001.fastq.gz'

edit1 = new_master.ix[:, 'sequencing file reverse name'] == forward_name
new_master.ix[edit1, 'sequencing file reverse name'] = reverse_name

mask2 = new_master.ix[:, 'sequencing file reverse name'] == reverse_name
barcodes = sorted(new_master.ix[mask2, '2nd step barcode'].tolist())
print len(np.unique(barcodes))
assert len(np.unique(barcodes)) == 96

new_master.to_csv(new_master_f, index=False)





