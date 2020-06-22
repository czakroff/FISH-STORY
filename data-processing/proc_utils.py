#!/usr/bin/env python

'''
Data Processing Utilities

This mini-library contains methods needed in the Spark processing pipeline of the
DNA reads, generally converting the reads from dataframes to fasta/fastQ or vice versa.

Written for Insight Data Engineering Fellowship
Version 2.0: Functional Pipeline
Casey Zakroff; Jun 22, 2020
'''

### Libraries
import numpy as np
import pandas as pd

### pandas_to_fastQ
# This method takes a pandas dataframe of paired end DNA reads and writes 
# it to forward and reverse fastQ files.
#
# Arguments: 
#       df: A pandas dataframe of DNA reads with 5 columns in the form:
#			columns = ['SRA','readNum','length,'read_F','read_R','qual_F','qual_R']
#				SRA = ID of SRA (sequencing run) file
#				readNum = ID of read
#				length = length of read
#				read_F = Forward nucleotide sequence
#				read_R = Reverse nucleotide sequence
#				qual_F = Quality score of forward nucleotide sequence 
#				qual_R = Quality score of reverse nucleotide sequence
#
# 		fwd_path: A path string to write the fastQ file of forward reads.
#       rev_path: A path string to write the fastQ file of reverse reads.
#		
# Return: none. Writes contents of pre-existing pandas dataframe.
#
def pandas_to_fastQ(df, fwd_path, rev_path):

    #Create writeable files
    with open(fwd_path, 'w') as fwd:
        with open(rev_path, 'w') as rev:
        
            #loop down table, writing rows to file 
            for i in range(0,len(df)):
                ID_string = '@' + df.loc[i,'SRA'] + '.' + df.loc[i,'readNum'] + \
                            ' ' + df.loc[i,'readNum'] + ' length=' + \
                            df.loc[i,'length'] + '\n'
                fwd.write(ID_string)
                rev.write(ID_string)
                
                fwd.write(df.loc[i,'read_F'] + '\n')
                rev.write(df.loc[i,'read_R'] + '\n')
                
                qual_string = '+' + df.loc[i,'SRA'] + '.' + df.loc[i,'readNum'] + \
                              ' ' + df.loc[i,'readNum'] + ' length=' + \
                              df.loc[i,'length'] + '\n'
                fwd.write(qual_string)
                rev.write(qual_string)
                
                fwd.write(df.loc[i,'qual_F'] + '\n')
                rev.write(df.loc[i,'qual_R'] + '\n')

### fasta_to_dicts
# This method takes a fasta file of taxonomic results and compiles it as a list
# of dicts, which is intended to be used to build a pandas dataframe.
#
# Arguments: 
# 		fasta_path: A path string to the fasta file of taxonomic results.
#
# Return: A list of dictionaries containing fields from fasta file.
#
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
