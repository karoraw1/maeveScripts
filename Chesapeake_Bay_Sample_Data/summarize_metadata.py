# -*- coding: utf-8 -*-

import pandas as pd

summary_file = "Sampling_processing_worksheet_120117.xlsx"
summary_sheet = pd.read_excel(summary_file)

print "13 samples have ?? as there short name"
print "How do you translate BioSampleID into Sample ID into information?"
print "Shouldn't controls get sample dates?"
print "What is going on with 266 - 285"
print "I need to enter my data"
print "I need to find samples that I qubited but didn't sequence"

print summary_sheet.isnull().sum()
