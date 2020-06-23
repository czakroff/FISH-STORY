#!/usr/bin/env python

'''
Written for Insight Data Engineering Fellowship
Version 2.1: Functional Pipeline
Casey Zakroff; Jun 23, 2020
'''

### Libraries
import os
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession

#Local Libraries
from proc_utils import *

###Create and configure Spark session
spark = SparkSession.builder.appName("FishProcess").getOrCreate()

###Read in data from PostgreSQL database

#psql parameters
psql_url = os.environ.get('PSQL_URL')
source_table = "SRR8649743"
psql_user = os.environ.get('PSQL_USER')
psql_pass = os.environ.get('PSQL_PASS')

#Read data as Spark dataframe
sdf = spark.read \
    .format("jdbc") \
    .option("url", psql_url) \
    .option("dbtable", source_table ) \
    .option("user", psql_user) \
    .option("password", psql_pass) \
    .load()

#Convert Spark dataframe to pandas
df = sdf.select("*").toPandas()

###Write to local fastQ

#paths to write new fastQ files
fwd_path = "/home/ubuntu/SRR8649743_1.fastq"
rev_path = "/home/ubuntu/SRR8649743_2.fastq"
 
#write new fastQ files
pandas_to_fastQ(df, fwd_path, rev_path)

###ObiTools3 OS calls

#Import sequences and metadata (tag/multiplex)
os.system("obi import --quality-solexa /home/ubuntu/SRR8649743_1.fastq fish/reads1")
os.system("obi import --quality-solexa /home/ubuntu/SRR8649743_2.fastq fish/reads2")
os.system("obi import --ngsfilter /home/ubuntu/fish_ngsfilter.txt fish/ngsfile")

#Align paired reads into singular read; Remove unaligned reads
os.system("obi alignpairedend -R fish/reads2 fish/reads1 fish/aligned_reads")
os.system("obi grep -a mode:alignment fish/aligned_reads fish/good_sequences")

#Assign tags to reads
os.system("obi ngsfilter -t fish/ngsfile -u fish/unidentified_sequences fish/good_sequences fish/identified_sequences")

#Dereplicate reads into unique sequences
os.system("obi uniq -m sample fish/identified_sequences fish/dereplicated_sequences")

#Denoise sequences
os.system("obi annotate -k COUNT -k MERGED_sample fish/dereplicated_sequences fish/cleaned_metadata_sequences")
os.system("obi grep -p \"len(sequence)>=80 and sequence['COUNT']>=10\" fish/cleaned_metadata_sequences fish/denoised_sequences")
os.system("obi clean -s MERGED_sample -r 0.05 -H fish/denoised_sequences fish/cleaned_sequences")

#Build reference database
os.system("obi import v05_refs.fasta.gz fish/v05_refs")
os.system("obi import --taxdump taxdump.tar.gz fish/taxonomy/my_tax")

#Clean the reference database
os.system("obi grep --require-rank=species --require-rank=genus --require-rank=family --taxonomy fish/taxonomy/my_tax fish/v05_refs fish/v05_refs_clean")
os.system("obi uniq --taxonomy fish/taxonomy/my_tax fish/v05_refs_clean fish/v05_refs_uniq")
os.system("obi grep --require-rank=family --taxonomy fish/taxonomy/my_tax fish/v05_refs_uniq fish/v05_refs_uniq_clean")
os.system("obi build_ref_db -t 0.97 --taxonomy fish/taxonomy/my_tax fish/v05_refs_uniq_clean fish/v05_db_97")

#Assign sequences to taxa
os.system("obi ecotag -m 0.97 --taxonomy fish/taxonomy/my_tax -R fish/v05_db_97 fish/cleaned_sequences fish/assigned_sequences")

#Align sequences
os.system("obi align -t 0.95 fish/assigned_sequences fish/aligned_assigned_sequences")

#Export results in fasta file
os.system("obi export --fasta-output fish/assigned_sequences -o fish_results.fasta")

###Close Spark session
spark.stop()