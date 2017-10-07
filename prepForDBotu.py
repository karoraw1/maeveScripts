#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Arguments for Various Operations 

    "-i": path to a text file containing a directory on each line 
          required for all other arguments

    "-count": Enumerate all sequence lengths

    "-trim": Trim down and remove short/long sequences
             The argument for this task is formatted like "L#1H#2"
             #1 = the truncation length (anything lower is discarded)
             #2 = the cutoff for sequences deemed too long
    "-trim-out": Newly trimmed (fasta) files written here 
                 Required if "-trim" is specified
                 The new file names are everything up to the first period "." + "trunc" + ".fasta" 

    "-collect": Collects all unique sequences across files (assumes truncation)
                Provide file name for writing as argument
                Requires "-i" to be truncation directory

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
        seq_lengths = Counter()
        print("Calculating sequence lengths: "+repr(count_flag))
    if arg == "-trim":
        trim_flag = True
        trim_lims = sys.argv[idx+1]
        t_low, t_high = trim_lims.split("H")
        trim_target, upper_bound = int(t_low[1:]), int(t_high)
        print("Trimming down to {}, discarding over {}".format(trim_target, upper_bound))
    if arg == "-trim-out":
        trim_out_dir = sys.argv[idx+1]
        trim_files = []


# Test: Trimming arguments both specified & not forcing overwrite
if trim_flag:
    if not trim_out_dir:
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
for idx, dir_ in enumerate(dir_list):
    file_list += [ os.path.join(dir_, f) for f in os.listdir(dir_) if ".fast" in f]
    # If trimming, create output file names
    if trim_flag:
        for f in os.listdir(dir_):
            if ".fast" in f:
                f_mod = "Dir"+str(idx+1)+"_"+f.split(".")[0]+".trunc.fastq"
                trim_files.append(os.path.join(trim_out_dir, f_mod))

# Report how many files detected in which directories 
report_1 = "{} files detected in {} directories".format(len(file_list), len(dir_list))
print(report_1, file=sys.stdout)

def trunc_records(records, trim_target, upper_bound):
    """Truncates records and discards excessively long sequences

    This is a generator function, the records argument should
    be a list or iterator returning SeqRecord objects.
    """
    for record in records:
        this_len = len(record)
        if this_len < trim_target or this_len > upper_bound:
           continue
        else:
            yield record[:trim_target]


# This is where we open the files are parse them in whatever way was specified
for idx, seq_file in enumerate(file_list):

    if seq_file.endswith(".fastq"):
        fast_sequences = SeqIO.parse(seq_file, 'fastq')
    else:
        fast_sequences = SeqIO.parse(seq_file, 'fasta')
    
    # This is run if we are printing a sequence length histogram(ish)
    if count_flag:
        for fast_ in fast_sequences:
            seq_lengths[len(fast_)] += 1
        print("Processed {}".format(seq_file))


    # This is run if we are truncating to a fixed sequence length
    if trim_flag:
        trimmed_reads = trunc_records(fast_sequences, trim_target, upper_bound)
        count = SeqIO.write(trimmed_reads, trim_files[idx], "fastq")
        print("Truncated {}. \n\tKept {}".format(seq_file, count) )


if count_flag:
    print("Length Report")
    for length_, count_ in seq_lengths.items():
        print("\t{}: {}".format(length_, count_))
