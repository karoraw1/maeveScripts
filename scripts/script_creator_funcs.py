
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

def trim_and_qual_assess(grouped_args):
    """
    """
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

def analysis_pipeline(grouped_args_):
    """ 
    """
    replacements, analysis_type = grouped_args_
    str_repl = ["^SID^", "^OP^", "^S1^", "^S2^", "^SS^", "^PWD^"]
    sid = replacements[0]
    OutScriptPath = os.path.join(replacements[1], sid, sid[:16]+"_step3.sh")

    with open("pipeline_3.sh", "r") as p3_fh:
        p3_text = p3_fh.read().split("\n")
    
    if analysis_type == "PENO":
      p3_text[24] = ""
    elif analysis_type == "PEO":
      p3_text[26] = p3_text[28] = ""
    else:
      sys.exit("invalid Read Type entered in Meta-Map")

    p3_tomod = "\n".join(p3_text)

    for real_, placeholder_ in zip(replacements, str_repl):
      p3_tomod = p3_tomod.replace(placeholder_, real_)

    with open(OutScriptPath, "w") as osp_fh:
        osp_fh.write(p3_tomod)

    return OutScriptPath

def make_meta_script(base_, fname, scriptList):
        meta_script_path = os.path.join(base_, fname)
        with open(meta_script_path, "w") as msp_fh:
            for sL in scriptList:
                msp_fh.write("sbatch " + sL + "\n")
        return

def taxa_calls(grouped_args):
    """
    """
    seq_id, base_out = grouped_args[1], grouped_args[2]
    OutScriptPath = os.path.join(base_out, seq_id, "Step4.sh")
    repls = ["^PWD^", "^SID^","^OP^","^RA^","^RS^"]
    
    with open("pipeline_4.sh", "r") as p4_fh:
        p4_str = p4_fh.read()

    for in_, out_ in zip(grouped_args, repls):
         p4_str = p4_str.replace(out_, in_)

    with open(OutScriptPath, "w") as osp_fh:
        osp_fh.write(p4_str)

    return OutScriptPath
