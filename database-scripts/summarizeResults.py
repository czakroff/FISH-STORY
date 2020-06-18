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
spark = SparkSession.builder.appName("WolfResults").getOrCreate()

#Ingest results fasta as Spark Dataframe
fasta_path = "wolf_results.fasta"
sdf_results = spark.createDataFrame(pd.DataFrame(fasta_to_dicts(fasta_path)))

#Store results to reads in PostgreSQL database
psql_url = os.environ.get('PSQL_URL')
results_table = "wolf_results"
psql_user = os.environ.get('PSQL_USER')
psql_pass = os.environ.get('PSQL_PASS')

sdf.write \
    .format("jdbc") \
    .option("url", psql_url) \
    .option("dbtable", results_table) \
    .option("user", psql_user) \
    .option("password", psql_pass) \
    .save()
    
#Close Spark session
spark.stop()