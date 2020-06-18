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

#Local Libraries
from ingest_utils import *

###Create and configure Spark session

# Enable Arrow-based columnar data transfers
spark = SparkSession.builder.appName("WolfIngest").getOrCreate()

###Ingest FastQ to Spark

#Set path to paired fastQ files
fwd_path = "/home/ubuntu/wolf_tutorial/wolf_F.fastq"
rev_path = "/home/ubuntu/wolf_tutorial/wolf_R.fastq"

#Build pandas dataframe
columns = ['SRA','read_F','read_R','qual_F','qual_R']
df = pd.DataFrame([], columns = columns)

#Convert fastq to pandas dataframe
fastQ_to_pandas(fwd_path, rev_path, df)

#Convert pandas dataframe to spark dataframe
sdf = spark.createDataFrame(df)

###Store in PostgreSQL database
psql_url = os.environ.get('PSQL_URL')
psql_table = "wolfdata"
psql_user = os.environ.get('PSQL_USER')
psql_pass = os.environ.get('PSQL_PASS')

sdf.write \
    .format("jdbc") \
    .mode("overwrite") \
    .option("url", psql_url) \
    .option("dbtable", psql_table) \
    .option("user", psql_user) \
    .option("password", psql_pass) \
    .save()

#Close Spark session
spark.stop()