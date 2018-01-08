#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:25:38 2017

This is the front end setup tool for a mostly DADA2 
16S pipeline. Its purpose is to read in a mapping file
containing sequence files in many different states of process
and to create a custom shell script for each that can be 
submitted to MARCC or AWS potentially allowing each file 
or set of files to be processed in parallel.

It uses a BBMap script for demultiplexing (`filterbyname.sh`)

The first step is to read in a writable directory for the
outputs and intermediate files. This can be provided on 
the commanad line. 

The second step is to read in a readable directory that contains
multiple different folders for each sequencing run to analyze. 

The third step is to read in the mapping file for each sequencing 
run. 

 - a prefix called the seqID which represents the sequencing 
   run and is the name of the subfolder in which the sequence 
   files are contained
 - a paired or single end flag ("PE" or "SE")
 - the name of the forward reads or the common suffix among 
   all forward reads in the 
 - the name of the reverse reads or the common suffix among
   all the reverse reads
 - the name of the index file if there is one
 - a demultiplexing boolean flag ("T" or "F")
 - the file path of a list of barcode sequences and sample names
 - a boolean if you want the scripts to check sequence header formatting
   matches between files (required for demultiplexing)
 - a boolean if you want the scripts to remove the last two chars of 
   all sequence headers ( makes older sequencing files compatible with
   demuxing script)



@author: Keith Arora-Williams
"""

import argparse, sys, os
import pandas as pd
from script_creator_funcs import *

descript_string = ("This is the front end setup tool for a mostly DADA2 "
                   "16S pipeline. Its purpose is to read in a mapping "
                   "file containing sequence files in many different "
                   "states of process and to create a custom shell "
                   "script for each that can be submitted to MARCC or "
                   "AWS potentially allowing each file or set of files "
                   "to be processed in parallel.\n\n\tExample Usage:\n\t"
                   "python script_creator.py -i $IN_DIR -o $OUT_DIR -m "
                   "../mapping_file.tsv")

parser = argparse.ArgumentParser(description = descript_string)

m_help = ("Path to a mapping file of the format specified in the README "
          "under the heading 'Meta-Map Format'")

t_help = ("Path to a trimming params file of the format specified in the"
          " README under the heading 'Trimming Spec File'. NOTE: either "
          " `-m` or `-t` must be specified for script to work")

parser.add_argument('-m', action='store', dest='meta_map',
                       help=m_help)

parser.add_argument('-t', action='store', dest='trim_specs',
                    help=t_help)

reqd_args = parser.add_argument_group('Required argument flags')

i_help = ("Path to a readable directory that contains multiple different"
          " folders for each sequencing run to analyze")
o_help = ("Path to a writable directory for the outputs and intermediate"
          " files.")

reqd_args.add_argument('-i', action='store', dest='read_dir', 
                       help=i_help, required=True)
reqd_args.add_argument('-o', action='store', dest='write_dir',
                       help=o_help, required=True)

args = parser.parse_args()

reqd_types = ["input directory", "output directory"]
reqd_args = [args.read_dir, args.write_dir]

print "\nInput Checks\n------------"
for this_arg, arg_t in zip(reqd_args, reqd_types):
    print_name = os.path.basename(this_arg)
    if os.path.exists(this_arg):
        print "`{}` is a valid path for the {}".format(print_name, arg_t)
    else:
        sys.exit("`{}` is an invalid path to a {}\n".format(this_arg, arg_t))

opt_types = ["Meta Map", "Trim Spec"]
opt_objs = [args.meta_map, args.trim_specs]
jobs_ = 0

for cmd_type, this_arg in zip(opt_types, opt_objs):
    if (this_arg and cmd_type == "Meta Map"):
        print "Creating scripts for demultiplexing"
        task = "Demux"
        jobs_ += 1
    elif (this_arg and cmd_type == "Trim Spec"):
        print "Creating scripts for trimming"
        jobs_ += 1 
        task = "Trim"

if jobs_ != 1:
    sys.exit("Need to specify a single task")

if task == "Demux":
    meta_map_df = pd.read_csv(args.meta_map, sep="\t")

    # default designations
    seqIDs = meta_map_df.ix[:, meta_map_df.columns[0]].tolist()
    inPaths = [os.path.join(args.read_dir, i) for i in seqIDs]
    outPaths = [os.path.join(args.write_dir, i) for i in seqIDs]
    map(safe_mkdir, outPaths)

    row_list = [meta_map_df.ix[idx, :].tolist() for idx in xrange(len(seqIDs))]
    packing_list = zip(outPaths, row_list, inPaths)
    script_list = map(write_demux_and_qual_assess, packing_list)

    meta_script_path = os.path.join(args.write_dir, "meta_script.sh")
    with open(meta_script_path, "w") as msp_fh:
        for sL in script_list:
            msp_fh.write("sbatch " + sL + "\n")
elif task == "Trim":
   trim_df = pd.read_csv(args.trim_specs, sep=",")
   print trim_df.SeqID.unique()
