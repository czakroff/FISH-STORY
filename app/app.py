#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Written for Insight Data Engineering Fellowship
Version 1.1: Wolf tutorial test 
Casey Zakroff; Jun 19, 2020
'''

###Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import numpy as np
import pandas as pd
import psycopg2
import os

###Pull data from PostgreSQL

#Set psql variables
#psql_user = os.environ.get('PSQL_USER')
#psql_pass = os.environ.get('PSQL_PASS')
#psql_ip = os.environ.get('PSQL_IP')
#psql_port = os.environ.get('PSQL_PORT')

#Local version
psql_user = 'db_select'
psql_pass = '3q2xAp'
psql_ip = '44.231.87.150'
psql_port = '5682'

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

#Close database connection
cursor.close()
connection.close()

###Data preparation

#Proportion of Reads Identified
num_id = ['Identified', sum(list(df.loc[df.SCIENTIFIC_NAME != 'nan','COUNT']))]
num_uid = ['Unidentified', sum(list(df.loc[df.SCIENTIFIC_NAME == 'nan','COUNT']))]

id_df = pd.DataFrame([num_id,num_uid], columns=['status','counts'])

fig = px.pie(id_df, values='counts', names='status', title='Proportion of Reads Identified')

#Table of Species Identified
sp = list(set(df.loc[df.SCIENTIFIC_NAME != 'nan', 'SCIENTIFIC_NAME']))
sp = sorted(list(i for i in sp if " " in i))
sp_df = pd.DataFrame(sp, columns = ['Species'])

### Function to make table
def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

###Build Dash App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='FISH-STORY DASHBOARD'),

    html.Div(children='''
        Version 1.0: Wolf Tutorial Test
    '''),

    dcc.Graph(
        id='pie-graph',
        figure=fig
    ),
    
    generate_table(sp_df)
    
])

if __name__ == '__main__':
    app.run_server(debug=True)