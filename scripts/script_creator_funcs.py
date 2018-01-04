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

#with open("pipeline_1.sh", "r") as p1_fh:
#    p1_text = p1_fh.read().split("\n")

def safe_mkdir(a_path):
    if not os.path.exists(a_path):
        os.mkdir(a_path)
        print "Made {} output directory".format(os.path.basename(a_path))
    else:
        print "{} output directory exists".format(os.path.basename(a_path))


def path_or_file(dirname, basename, glob_bool):
    if glob_bool:
        do something
    else:
        local_file = os.path.abspath(basename)
        full_path = basename
        subfolder_convention = os.path.join(dirname, basename)
        possible_files = np.array([local_file, full_path, subfolder_convention])
        existing_file_possibilities = np.array([os.path.exists(pf) for pf in possible_files])
        assert existing_file_possibilities.sum() == 1
        return possible_files[existing_file_possibilities][0]
        

