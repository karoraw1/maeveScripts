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
 - 


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
                   "to be processed in parallel.")

parser = argparse.ArgumentParser(description = descript_string)

reqd_args = parser.add_argument_group('Required argument flags')

i_help = ("Path to a readable directory that contains multiple different"
          " folders for each sequencing run to analyze")
o_help = ("Path to a writable directory for the outputs and intermediate"
          " files.")
m_help = ("Path to a mapping file of the format specified in the README "
          "under the heading 'Meta-Map Format'")

reqd_args.add_argument('-i', action='store', dest='read_dir', 
                       help=i_help, required=True)
reqd_args.add_argument('-o', action='store', dest='write_dir',
                       help=o_help, required=True)
reqd_args.add_argument('-m', action='store', dest='meta_map',
                       help=m_help, required=True)

args = parser.parse_args()

arg_types = ["input directory", "output directory", "meta mapping file\n"]
arg_list = [args.read_dir, args.write_dir, args.meta_map]

print "\nInput Checks\n------------"
for this_arg, arg_t in zip(arg_list, arg_types):
    print_name = os.path.basename(this_arg)
    if os.path.exists(this_arg):
        print "`{}` is a valid path for the {}".format(print_name, arg_t)
    else:
        sys.exit("`{}` is an invalid path to a {}\n".format(this_arg, arg_t))


meta_map_df = pd.read_csv(args.meta_map, sep="\t")

# default designations
seqIDs = meta_map_df.ix[:, meta_map_df.columns[0]].tolist()
inPaths = [os.path.join(args.read_dir, i) for i in seqIDs]
outPaths = [os.path.join(args.write_dir, i) for i in seqIDs]
for i in outPaths:
    print i
map(safe_mkdir, outPaths)

row_list = [meta_map_df.ix[idx, :].tolist() for idx in xrange(len(seqIDs))]
packing_list = zip(outPaths, row_list, inPaths)



#def write_demux_and_qual_assess(paths_and_row):
#    base_out, row_entry, base_in  = paths_and_row
#    sid, fwd, rev, idxF, map_, bcode, demux_bool, readType = row_entry
#    OutScriptPath = os.path.join(base_out, sid+"_step1.sh")
#    # not demuxed
#    with open("pipeline_1.sh", "r") as p1_fh:
#        p1_text = p1_fh.read().split("\n")
#
#    if not demux_bool:
#        fwd_path = path_or_file(base_in, fwd, False)
#        rev_path = path_or_file(base_in, rev, False)
#        idx_path = path_or_file(base_in, idxF, False)
#        bcode_path = path_or_file(base_path, bcode, False)
#    else:
#        fwd_path = path_or_file(base_in, fwd, True)
#        rev_path = path_or_file(base_in, rev, True)
#        del p1_text[29:42]
#        del p1_text[5:8]
#        p1_text[4] = p1_text[4].split("=")[0]+"=0:15:00"
#        p1_text[-1] = p1_text[27]
#        p1_text[26] = "ln $FWD_PATH $DEMUX_DIR"
#        p1_text[27] = "ln $REV_PATH $DEMUX_DIR"
#        
#    rep_strs = ["^SID^","^F^","^R^","^I^","^B^", "^OP^"]
#    
#    return


