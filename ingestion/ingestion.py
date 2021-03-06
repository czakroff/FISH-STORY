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
from ingest_utils import *

###Create and configure Spark session

#Build Spark Session
spark = SparkSession.builder.appName("FishIngest").getOrCreate()

###Make FastQ
os.system("fasterq-dump SRR8649743")

###Ingest FastQ to Spark

#Set path to paired fastQ files
fwd_path = "/home/ubuntu/SRR8649743_1.fastq"
rev_path = "/home/ubuntu/SRR8649743_2.fastq"

#Build pandas dataframe
columns = ['SRA','readNum','length','read_F','read_R','qual_F','qual_R']
df = pd.DataFrame([], columns = columns)

#Convert fastq to pandas dataframe
fastQ_to_pandas(fwd_path, rev_path, df)

#Convert pandas dataframe to spark dataframe
sdf = spark.createDataFrame(df)

###Store in PostgreSQL database
psql_url = os.environ.get('PSQL_URL')
psql_table = "SRR8649743"
psql_user = os.environ.get('PSQL_USER')
psql_pass = os.environ.get('PSQL_PASS')

sdf.write \
    .format("jdbc") \
    .option("url", psql_url) \
    .option("dbtable", psql_table) \
    .option("user", psql_user) \
    .option("password", psql_pass) \
    .save()

#Close Spark session
spark.stop()