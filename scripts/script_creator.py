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
                   "be provided (-o, -t).")

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
if args.meta_map:
    task = "Demultiplexing"
    if not args.read_dir:
        sys.exit("No input directory provided")
elif args.trim_specs:
    task = "Trimming"

print "\tScript type set to {}".format(task)

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

    meta_script_path = os.path.join(args.write_dir, "meta_script_d.sh")
    with open(meta_script_path, "w") as msp_fh:
        for sL in script_list:
            msp_fh.write("sbatch " + sL + "\n")

elif task == "Trimming":

    trim_df = pd.read_csv(args.trim_specs, sep=",")
    seqIDs = trim_df.SeqID.unique()
    grouped_args = [(sID, args.write_dir, args.trim_specs) for sID in seqIDs]

    def trim_and_qual_asses(grouped_args):
        seq_id, base_out, t_stat = grouped_args
        OutScriptPath = os.path.join(base_out, seq_id, "Step2.sh")
        replacements = [seq_id, base_out, t_stat, os.getcwd()]
        repl_matches = ["^SID^", "^OP^", "^T^", "^PWD^"]
        with open("pipeline_2.sh", "r") as p2_fh:
            p2_str = p2_fh.read()
        for in_, out_ in zip(replacements, repl_matches):
             p2_str = p2_str.replace(out_, in_)
        with open(OutScriptPath, "w") as osp_fh:
            osp_fh.write(p2_str)
        return OutScriptPath

    script_list = map(trim_and_qual_asses, grouped_args)

    meta_script_path = os.path.join(args.write_dir, "meta_script_t.sh")

    with open(meta_script_path, "w") as msp_fh:
        for sL in script_list:
            msp_fh.write("sbatch " + sL + "\n")
else:
    sys.exit("No task specified (-t/-m)")

