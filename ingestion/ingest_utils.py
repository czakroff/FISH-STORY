#!/usr/bin/env python

'''
Written for Insight Data Engineering Fellowship
Version 1.0: Wolf tutorial test 
Casey Zakroff; Jun 17, 2020
'''

### Libraries
import numpy as np
import pandas as pd

#Converts fastQ files to pandas dataframe
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