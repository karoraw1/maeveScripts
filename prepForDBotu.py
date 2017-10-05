#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
1 Read a file containing a list of directories, one on each line
2 
2 Create a hash table of sequence lengths
3 Print their distribution
4 Trims them down to the minimum length 
5 Writes them out into new files


writes it back out again with modified headers
"""

from __future__ import print_function
from Bio import SeqIO
import sys, os
from collections import Counter

## Fetch command line argument
#for idx, arg in enumerate(sys.argv):
#    if arg == "-i":
#        fn = sys.argv[idx+1]

fn = "input_file.test"

# Ensure file exists and read each line into a list
if os.path.exists(fn):
    with open(fn, "r") as dir_list_h:
        dir_list = dir_list_h.read().split("\n")
    dir_list = list(filter(None, dir_list))
else:
    sys.exit("Input file {} not detected".format(fn))

# Make a new list of files from list of directories
file_list = []
for dir_ in dir_list:
    file_list += [ os.path.join(dir_, f) for f in os.listdir(dir_) if ".fast" in f]

report_1 = "{} files detected in {} directories".format(len(file_list), len(dir_list))
print(report_1, file=sys.stdout)

seq_lengths = Counter()

# First we trim everything 
for seq_file in file_list:
    if seq_file.endswith(".fastq"):
        fast_sequences = SeqIO.parse(open(seq_file, "r"), 'fastq')
    else:
        fast_sequences = SeqIO.parse(open(seq_file, "r"), 'fasta')
    
    for fast_ in fast_sequences:
        name, sequence = fast_.id, str(fast_.seq)
        seq_lengths[len(sequence)] += 1

sys.exit()

seq_cnt = Counter()

sys.exit()

with open(fn2, "w") as of_:
    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        name = ">Seq_" + name
        print(name, file=of_)
        print(sequence, file=of_)

