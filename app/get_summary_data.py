#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Written for Insight Data Engineering Fellowship
Version 1.0: Wolf data through Gunicorn
Casey Zakroff; Jun 22, 2020
'''

###Libraries

import numpy as np
import pandas as pd
import psycopg2
import os

###Pull data from PostgreSQL

#Set psql variables
psql_user = os.environ.get('PSQL_USER')
psql_pass = os.environ.get('PSQL_PASS')
psql_ip = os.environ.get('PSQL_IP')
psql_port = os.environ.get('PSQL_PORT')

#Connect to psql database
connection = psycopg2.connect(user = psql_user,
                              password = psql_pass,
                              host = psql_ip,
                              port = psql_port,
                              database = 'wolf')
cursor = connection.cursor()

#Pull columns from results
cursor.execute("SELECT column_name \
			   FROM information_schema.columns \
			   WHERE table_schema = 'public' \
			   AND table_name   = 'wolf_results';")	   
columns = cursor.fetchall()

#Decompose tuples
columns = list(i[0] for i in columns)

#Pull results data
cursor.execute("SELECT * \
               FROM wolf_results;")              
results = cursor.fetchall()

#Build pandas dataframe
df = pd.DataFrame(results,columns = columns)

for i in range(0,len(df.dtypes)):
	if str(df.dtypes[i]) == 'O':
		df[columns[i]] = df[columns[i].astype(str)
			
#Print dataframe as local csv
df.to_csv('/home/ubuntu/summaryData.csv')

#Close database connection
cursor.close()
connection.close()