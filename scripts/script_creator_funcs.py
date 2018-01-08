
#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 19:25:38 2017

This file contains function definitions used in the companion
file `script_creator.py`

@author: Keith Arora-Williams
"""
import numpy as np
import os

def safe_mkdir(a_path):
    if not os.path.exists(a_path):
        os.mkdir(a_path)
        print "Made {} output directory".format(os.path.basename(a_path))
    else:
        print "{} output directory exists".format(os.path.basename(a_path))


def path_or_file(dirname, basename, glob_bool):
    if glob_bool:
        if "/" in basename:
            return basename            
        else:
            return os.path.join(dirname, basename)
    else:
        full_path = basename
        subfolder_convention = os.path.join(dirname, basename)
        if full_path == subfolder_convention:
            return full_path
        else:
            possible_files = np.array([full_path, subfolder_convention])
            existing_file_possibilities = np.array([os.path.exists(pf) for pf in possible_files])
            assert existing_file_possibilities.sum() == 1
            return possible_files[existing_file_possibilities][0]
        

def write_demux_and_qual_assess(paths_and_row):
    """
    This takes in a row of the mapping file and creates
    a custom script in the subdirectory of the main 
    output directory for checking headers & demultiplexing
    """

    base_out_seqid, row_entry, base_in  = paths_and_row
    base_out = os.path.dirname(base_out_seqid)

    sid, fwd, rev, idxF, map_, bcode, demux_bool, readType, chkH, fixH = row_entry
    OutScriptPath = os.path.join(base_out_seqid, sid+"_step1.sh")

    # not demuxed
    with open("pipeline_1.sh", "r") as p1_fh:
        p1_text = p1_fh.read().split("\n")

    # default checks and corrects headers
    if chkH or fixH:
        # headers must be checked if they are to be corrected
        if fixH:
            pass
        # if only checking is required, the copying step is removed
        else:
            p1_text[28:32] = [""]*4
    # if neither are required, the entire preprocessing block is removed
    else:
        p1_text[25:37] = [""]*12
        
    if not demux_bool:
        fwd_path = path_or_file(base_in, fwd, False)
        rev_path = path_or_file(base_in, rev, False)
        idx_path = path_or_file(base_in, idxF, False)
        bcode_path = path_or_file(base_in, bcode, False)
    else:
        fwd_path = path_or_file(base_in, fwd, True)
        rev_path = path_or_file(base_in, rev, True)
        p1_text[25:37] = [""]*12
        p1_text[42:57] = [""]*15
        p1_text[5:8] = [""]*3
        p1_text[4] = p1_text[4].split("=")[0]+"=0:15:00"
        p1_text[-1] = p1_text[27]
        p1_text[42] = "ln -s $FWD_PATH -t $DEMUX_DIR"
        p1_text[43] = "ln -s $REV_PATH -t $DEMUX_DIR"
        p1_text[45] = p1_text[57]
        p1_text[57], p1_text[19], p1_text[23] = "", "", ""

    rep_strs = ["^PWD^", "^SID^", "^F^", "^R^", "^OP^"]
    replacements = [os.getcwd(), sid, fwd_path, rev_path, base_out]
    if not demux_bool:
        rep_strs += ["^B^", "^I^"]
        replacements += [bcode_path, idx_path]
    
    p1_string = "\n".join(p1_text)
    for in_, out_ in zip(replacements, rep_strs):
         p1_string = p1_string.replace(out_, in_)

    with open(OutScriptPath, "w") as osp_fh:
        osp_fh.write(p1_string)

    return OutScriptPath
