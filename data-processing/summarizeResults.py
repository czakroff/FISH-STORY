#!/usr/bin/env python

'''
Written for Insight Data Engineering Fellowship
Version 1.1: Wolf tutorial test 
Casey Zakroff; Jun 18, 2020
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
spark = SparkSession.builder.appName("WolfResults").getOrCreate()

###Ingest results fasta as Spark Dataframe
fasta_path = "wolf_results.fasta"

#Set schema
mySchema = StructType([ StructField("BEST_IDENTITY", LongType(), True)\
                       ,StructField("BEST_MATCH_IDS", StringType(), True)\
                       ,StructField("BEST_MATCH_TAXIDS", StringType(), True)\
                       ,StructField("COUNT", IntegerType(), True)\
                       ,StructField("ID_STATUS", BooleanType(), True)\
                       ,StructField("MERGED_sample", StringType(), True)\
                       ,StructField("SCIENTIFIC_NAME", StringType(), True)\
                       ,StructField("TAXID", StringType(), True)\
                       ,StructField("obiclean_head", BooleanType(), True)\
                       ,StructField("cobiclean_headcount", IntegerType(), True)\
                       ,StructField("obiclean_internalcount", IntegerType(), True)\
                       ,StructField("obiclean_samplecount", IntegerType(), True)\
                       ,StructField("obiclean_status", StringType(), True)\
                       ,StructField("read_ID", StringType(), True)])

#Make Spark dataframe
sdf_results = spark.createDataFrame(pd.DataFrame(fasta_to_dicts(fasta_path)), schema=mySchema)

###Store results to reads in PostgreSQL database

#Set psql variables
psql_url = os.environ.get('PSQL_URL')
results_table = "wolf_results"
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