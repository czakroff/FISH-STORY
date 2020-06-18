#!/usr/bin/env python

'''
Written for Insight Data Engineering Fellowship
Version 1.0: Wolf tutorial test 
Casey Zakroff; Jun 17, 2020
'''

### Libraries
import os
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession

#Local Libraries
from proc_utils import *

###Create and configure Spark session
spark = SparkSession.builder.appName("WolfTest").getOrCreate()

###Read in data from PostgreSQL database
sdf = spark.read \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://ip-10-0-0-11:5682/wolf") \
    .option("dbtable", "wolfdata") \
    .option("user", "db_select") \
    .option("password", "x15jh7") \
    .load()

#Convert to pandas
df = sdf.select("*").toPandas()

###Write to local fastQ
fwd_path = "wolf_tutorial/wolftest_F.fastq"
rev_path = "wolf_tutorial/wolftest_R.fastq"
 
pandas_to_fastQ(df, fwd_path, rev_path)

#ObiTools3 OS calls
os.system("obi import --quality-solexa wolf_tutorial/wolftest_F.fastq wolf/reads1")
os.system("obi import --quality-solexa wolf_tutorial/wolftest_R.fastq wolf/reads2")
os.system("obi import --ngsfilter wolf_tutorial/wolf_diet_ngsfilter.txt wolf/ngsfile")
os.system("obi alignpairedend -R wolf/reads2 wolf/reads1 wolf/aligned_reads")
os.system("obi grep -a mode:alignment wolf/aligned_reads wolf/good_sequences")
os.system("obi ngsfilter -t wolf/ngsfile -u wolf/unidentified_sequences wolf/good_sequences wolf/identified_sequences")
os.system("obi uniq -m sample wolf/identified_sequences wolf/dereplicated_sequences")
os.system("obi annotate -k COUNT -k MERGED_sample wolf/dereplicated_sequences wolf/cleaned_metadata_sequences")
os.system("obi grep -p \"len(sequence)>=80 and sequence['COUNT']>=10\" wolf/cleaned_metadata_sequences wolf/denoised_sequences")
os.system("obi clean -s MERGED_sample -r 0.05 -H wolf/denoised_sequences wolf/cleaned_sequences")
os.system("obi import v05_refs.fasta.gz wolf/v05_refs")
os.system("obi import --taxdump taxdump.tar.gz wolf/taxonomy/my_tax")
os.system("obi grep --require-rank=species --require-rank=genus --require-rank=family --taxonomy wolf/taxonomy/my_tax wolf/v05_refs wolf/v05_refs_clean")
os.system("obi uniq --taxonomy wolf/taxonomy/my_tax wolf/v05_refs_clean wolf/v05_refs_uniq")
os.system("obi grep --require-rank=family --taxonomy wolf/taxonomy/my_tax wolf/v05_refs_uniq wolf/v05_refs_uniq_clean")
os.system("obi build_ref_db -t 0.97 --taxonomy wolf/taxonomy/my_tax wolf/v05_refs_uniq_clean wolf/v05_db_97")
os.system("obi ecotag -m 0.97 --taxonomy wolf/taxonomy/my_tax -R wolf/v05_db_97 wolf/cleaned_sequences wolf/assigned_sequences")
os.system("obi stats -c SCIENTIFIC_NAME wolf/assigned_sequences")
os.system("obi align -t 0.95 wolf/assigned_sequences wolf/aligned_assigned_sequences")
os.system("obi export --fasta-output wolf/assigned_sequences -o wolf_results.fasta")

#Ingest results fasta as Spark Dataframe

#Join results to reads in PostgreSQL database

#Close Spark session
spark.stop()