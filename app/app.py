#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Written for Insight Data Engineering Fellowship
Version 1.2: Wolf data through Gunicorn
Casey Zakroff; Jun 22, 2020
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

###Data preparation

#Get data from local table
path = '/home/ubuntu/summaryData.csv'
df = pd.read_csv(path)

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

server = app.server

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
    app.run_server(host='0.0.0.0', debug=True)