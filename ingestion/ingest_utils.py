#!/usr/bin/env python

'''
Ingestion Utilities

This mini-library contains a method for converting fastQ files into pandas
dataframes as part of ingestion into Spark.

Written for Insight Data Engineering Fellowship
Version 1.1: Functional pipeline
Casey Zakroff; Jun 18, 2020
'''

### Libraries
import numpy as np
import pandas as pd

### fastQ_to_pandas
# This method takes a paired set of fastQ files and compiles them into a simplified
# pandas dataframe.
#
# Arguments: 
# 		fwd_path: A path string to the fastQ file of forward reads.
#       rev_path: A path string to the fastQ file of reverse reads.
#		df: An empty pandas dataframe with 5 columns in the form:
#       	columns = ['SRA','read_F','read_R','qual_F','qual_R']
#				SRA = ID of SRA (sequencing run) file
#				read_F = Forward nucleotide sequence
#				read_R = Reverse nucleotide sequence
#				qual_F = Quality score of forward nucleotide sequence 
#				qual_R = Quality score of reverse nucleotide sequence
#
# Return: none. Manipulates contents of pre-existing pandas dataframe.
#
def fastQ_to_pandas(fwd_path, rev_path, df):
    row = []
    read = True
    i = 0

    with open(fwd_path) as fwd:
        with open(rev_path) as rev: 
            for line_f in fwd:
                line_r = next(rev)
            
                if (line_f[0] == '@') & read:
                    row.append(line_f)
                elif (line_f[0] == '+') & read:
                    read = False
                elif read:
                    row.append(line_f)
                    row.append(line_r)
                else:
                    row.append(line_f)
                    row.append(line_r)
                    df.loc[i] = row
                    read = True
                    row = []
                    i += 1