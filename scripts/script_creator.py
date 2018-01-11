#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:25:38 2017

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
                   "to be processed in parallel. For demultiplexing, an"
                   " input, output, and meta-map should be provided. ("
                   "-i, -o, -m). For trimming, The output path used in "
                   "the demultiplexing and a trimming spec sheet should "
                   "be provided (-o, -t). For OTU calling, just the "
                   "location of the trimmed data and the meta-map (-o, -"
                   "m)")

parser = argparse.ArgumentParser(description = descript_string)

m_help = ("Path to a mapping file of the format specified in the README "
          "under the heading 'Meta-Map Format'")

t_help = ("Path to a trimming params file of the format specified in the"
          " README under the heading 'Trimming Spec File'.")

i_help = ("Path to a readable directory that contains multiple different"
          " folders for each sequencing run to analyze")

parser.add_argument('-m', action='store', dest='meta_map',
                       help=m_help)

parser.add_argument('-t', action='store', dest='trim_specs',
                    help=t_help)

parser.add_argument('-i', action='store', dest='read_dir', 
                    help=i_help)

reqd_args = parser.add_argument_group('Required argument flags')

o_help = ("Path to a writable directory for the outputs and intermediate"
          " files.")

reqd_args.add_argument('-o', action='store', dest='write_dir',
                       help=o_help, required=True)

args = parser.parse_args()

print "\nInput Checks\n------------"
if (args.meta_map and args.read_dir and args.write_dir):
    task = "Demultiplexing"
elif (args.trim_specs and args.write_dir):
    task = "Trimming"
elif (args.meta_map and args.write_dir):
    task = "Call OTUS"

print "Script type set to `{}`".format(task)

if task == "Demultiplexing":
    meta_map_df = pd.read_csv(args.meta_map, sep="\t")

    # default designations
    seqIDs = meta_map_df.ix[:, meta_map_df.columns[0]].tolist()
    inPaths = [os.path.join(args.read_dir, i) for i in seqIDs]
    outPaths = [os.path.join(args.write_dir, i) for i in seqIDs]
    map(safe_mkdir, outPaths)

    row_list = [meta_map_df.ix[idx, :].tolist() for idx in xrange(len(seqIDs))]
    packing_list = zip(outPaths, row_list, inPaths)
    script_list = map(write_demux_and_qual_assess, packing_list)
    make_meta_script(args.write_dir, "meta_script_d.sh", script_list)

elif task == "Trimming":

    trim_df = pd.read_csv(args.trim_specs, sep=",")
    seqIDs = trim_df.SeqID.unique()
    grouped_args = [(sID, args.write_dir, args.trim_specs) for sID in seqIDs]
    script_list = map(trim_and_qual_assess, grouped_args)
    make_meta_script(args.write_dir, "meta_script_t.sh", script_list)

elif task == "Call OTUS":
    print "Reading in Map"
    meta_map_df = pd.read_csv(args.meta_map, sep="\t")
    seqIDs = meta_map_df.ix[:, meta_map_df.columns[0]].tolist()
    grouped_args = []
    for sID in seqIDs:
        print "\tPrepped for {}".format(sID) 
        sID_bool = meta_map_df.ix[:, meta_map_df.columns[0]] == sID
        sID_rt = meta_map_df.ix[sID_bool, "ReadTypes"].values[0]
        sID_tfs1 = meta_map_df.ix[sID_bool, "TrimmedFileSuffix1"].values[0]
        sID_tfs2 = meta_map_df.ix[sID_bool, "TrimmedFileSuffix2"].values[0]
        if sID_rt == "PENO":
            # for non-overlapping single end, we process both independently 
            # and append the direction to the sample name
            sID_ss = "_filt"
        else:
            # for paired end, we use the forward read
            sID_ss = sID_tfs1.split(".")[0]

        grouped_args.append( ((sID, args.write_dir, sID_tfs1, 
                              sID_tfs2, sID_ss, os.getcwd()), sID_rt ))

    script_list = map(analysis_pipeline, grouped_args)
    make_meta_script(args.write_dir, "meta_script_a.sh", script_list)
else:
    sys.exit("No task specified. See arg pairings for each possible task")


