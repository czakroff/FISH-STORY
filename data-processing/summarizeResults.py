#!/usr/bin/env python

'''
Written for Insight Data Engineering Fellowship
Version 2.0: Functional Pipeline
Casey Zakroff; Jun 22, 2020
'''

### Libraries
import os
import numpy as np
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.types import *

#Local Libraries
from proc_utils import *

###Create and configure Spark session
spark = SparkSession.builder.appName("FishResults").getOrCreate()

###Ingest results fasta as Spark Dataframe

#Ingest results into pandas
fasta_path = "fish_results.fasta"
df_results = pd.DataFrame(fasta_to_dicts(fasta_path))

#Cast datatypes
df_results["read_ID"] = df_results["read_ID"].astype(str)
df_results["obiclean_samplecount"] = df_results["obiclean_samplecount"].astype(int)
df_results["BEST_MATCH_TAXIDS"] = df_results["BEST_MATCH_TAXIDS"].astype(str)
df_results["COUNT"] = df_results["COUNT"].astype(int)
df_results["obiclean_internalcount"] = df_results["obiclean_internalcount"].astype(int)
df_results["SCIENTIFIC_NAME"] = df_results["SCIENTIFIC_NAME"].astype(str)
df_results["ID_STATUS"] = df_results["ID_STATUS"].astype(str)
df_results["MERGED_sample"] = df_results["MERGED_sample"].astype(str)
df_results["BEST_IDENTITY"] = df_results["BEST_IDENTITY"].astype(float)
df_results["obiclean_headcount"] = df_results["obiclean_headcount"].astype(int)
df_results["BEST_MATCH_IDS"] = df_results["BEST_MATCH_IDS"].astype(str)
df_results["TAXID"] = df_results["TAXID"].astype(str)
df_results["obiclean_status"] = df_results["obiclean_status"].astype(str)
df_results["obiclean_head"] = df_results["obiclean_head"].astype(str)

#Set schema
results_schema = StructType([ StructField("read_ID", StringType(), True)\
                             ,StructField("obiclean_samplecount", IntegerType(), True)\
                             ,StructField("BEST_MATCH_TAXIDS", StringType(), True)\
                             ,StructField("COUNT", IntegerType(), True)\
                             ,StructField("obiclean_internalcount", IntegerType(), True)\
                             ,StructField("SCIENTIFIC_NAME", StringType(), True)\
                             ,StructField("ID_STATUS", StringType(), True)\
                             ,StructField("MERGED_sample", StringType(), True)\
                             ,StructField("BEST_IDENTITY", DoubleType(), True)\
                             ,StructField("obiclean_headcount", IntegerType(), True)\
                             ,StructField("BEST_MATCH_IDS", StringType(), True)\
                             ,StructField("TAXID", StringType(), True)\
                             ,StructField("obiclean_status", StringType(), True)\
                             ,StructField("obiclean_head", StringType(), True)])

#Make Spark dataframe
sdf = spark.createDataFrame(df_results, schema = results_schema)

###Store results to reads in PostgreSQL database

#Set psql variables
psql_url = os.environ.get('PSQL_URL')
results_table = "fish_results"
psql_user = os.environ.get('PSQL_USER')
psql_pass = os.environ.get('PSQL_PASS')

#Write to psql database
sdf.write \
    .format("jdbc") \
    .option("url", psql_url) \
    .option("dbtable", results_table) \
    .option("user", psql_user) \
    .option("password", psql_pass) \
    .save()
    
#Close Spark session
spark.stop()