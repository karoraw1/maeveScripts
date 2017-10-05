#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
1 Read a file containing a list of directories, one on each line
2 Performs various operations on them
    "-count": Enumerate all sequence length 
    "-trim": Trim down and remove short/long sequences
             The argument for this task is formatted like "L#1H#2"
             #1 = the truncation length (anything lower is discarded)
             #2 = the cutoff for sequences deemed too long
    "-trim-out": Newly trimmed (fasta) files written here 
                 Required if "-trim" is specified
                 The new file names are everything up to the first period "." + "trunc" + ".fasta" 

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

# Prepare variables for command line arguments
count_flag, trim_flag, fn = False, False, None
trim_out_dir = None

# Fetch command line argument
for idx, arg in enumerate(sys.argv):
    if arg == "-i":
        fn = sys.argv[idx+1]
    if arg == "-count":
        count_flag = True
    if arg == "-trim":
        trim_flag = True
        trim_lims = sys.argv[idx+1]
        t_low, t_high = trim_lims.split("H")
        trim_target, upper_bound = int(t_low[1:]), int(t_high)        
    if arg == "-trim-out":
        trim_out_dir = sys.argv[idx+1]

if trim_flag and not trim_out_dir:
    sys.exit("No trimming output directory specified")
else:
    if os.path.exists(trim_out_dir):
        sys.exit("Output directory exists already")
    else:
        os.mkdir(trim_out_dir)

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

# This is where we open the files are parse them in whatever way was specified

for seq_file in file_list:
    if seq_file.endswith(".fastq"):
        fast_sequences = SeqIO.parse(open(seq_file, "r"), 'fastq')
    else:
        fast_sequences = SeqIO.parse(open(seq_file, "r"), 'fasta')
    
    if count_flag:
        for fast_ in fast_sequences:
            seq_lengths[len(fast_)] += 1
        print("Processed {}".format(seq_file))

    if trim_flag:

???

if count_flag:
    for length_, count_ in seq_lengths.items():
        print("{}: {}".format(length_, count_))

sys.exit()

seq_cnt = Counter()

sys.exit()

with open(fn2, "w") as of_:
    for fasta in fasta_sequences:
        name, sequence = fasta.id, str(fasta.seq)
        name = ">Seq_" + name
        print(name, file=of_)
        print(sequence, file=of_)

