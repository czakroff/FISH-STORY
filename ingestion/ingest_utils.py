#!/usr/bin/env python

'''
Ingestion Utilities

This mini-library contains a method for converting fastQ files into pandas
dataframes as part of ingestion into Spark.

Written for Insight Data Engineering Fellowship
Version 2.1: Functional pipeline
Casey Zakroff; Jun 23, 2020
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
#       	columns = ['SRA','readNum','length,'read_F','read_R','qual_F','qual_R']
#				SRA = ID of SRA (sequencing run) file
#				readNum = ID of read
#				length = length of read
#				read_F = Forward nucleotide sequence
#				read_R = Reverse nucleotide sequence
#				qual_F = Quality score of forward nucleotide sequence 
#				qual_R = Quality score of reverse nucleotide sequence
#
# Return: none. Manipulates contents of pre-existing pandas dataframe.
#
def fastQ_to_pandas(fwd_path, rev_path, df):
	#Set required variables
	row = []
	read = True
	i = 0

	#Open forward and reverse fastQ files
	with open(fwd_path) as fwd:
		with open(rev_path) as rev: 
			#Read in line from forward file
			for line_f in fwd:
				#Read in line from reverse file
				line_r = next(rev)
            
            	#Check if the line is a read header
				if (line_f[0] == '@') & read:
					#If it is a header line, split it into the required information
					ID_str = line_f.split(' ')
					row.append(ID_str[0][1:11])
					row.append(ID_str[1])
					row.append(ID_str[2][-4:-1])
				#Check if line is a quality header (repeat of read header) and skip if so
				elif (line_f[0] == '+') & read:
					#Shift flag for next lines
					read = False
				#Check if line is a read and add to row of dataframe	
				elif read:
        			row.append(line_f[:-1])
            		row.append(line_r[:-1])
            	#Otherwise add quality line to row of dataframe
				else:
            		row.append(line_f[:-1])
            		row.append(line_r[:-1])
            		
            		#Add row to dataframe
            		df.loc[i] = row
            		#Shift flag for next lines
            		read = True
            		#Reset row and increment counter
            		row = []
            		i += 1