#!/usr/bin/env python

'''
Written for Insight Data Engineering Fellowship
Version 1.1: Wolf tutorial test 
Casey Zakroff; Jun 18, 2020
'''

### Libraries
import numpy as np
import pandas as pd

#wolf version: Converts fastQ files to pandas dataframe
def pandas_to_fastQ(df, fwd_path, rev_path):

	#Create writeable files
    with open(fwd_path, 'w') as fwd:
        with open(rev_path, 'w') as rev:
        
        	#loop down table, writing rows to file 
            for i in range(0,len(df)):
                fwd.write(df.loc[i,'SRA'])
                rev.write(df.loc[i,'SRA'])
                
                fwd.write(df.loc[i,'read_F'])
                rev.write(df.loc[i,'read_R'])
                
                fwd.write('+\n')
                rev.write('+\n')
                
                fwd.write(df.loc[i,'qual_F'])
                rev.write(df.loc[i,'qual_R'])

#Convert fasta to dicts
def fasta_to_dicts(fasta_path):
    dict_list = list()
    tuples = []

    with open(fasta_path) as result:
        for line in result:
            if (line[0] == '>'):
                split_line = line.split(';')
                
                for i in range(0,len(split_line)-1):
                    #ID
                    if i == 0:
                        tuples.append(('read_ID',split_line[0][1:]))
                        
                    #Other data fields
                    else:
                        fields = split_line[i].split('=')
                        tuples.append((fields[0][1:],fields[1]))
                        
                dict_list.append(dict(tuples))
                tuples = []
                
    return dict_list
