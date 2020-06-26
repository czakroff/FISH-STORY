#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Written for Insight Data Engineering Fellowship
Version 2.0: Prototype with Mock Data
Casey Zakroff; Jun 26, 2020
'''

###Libraries
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import pandas as pd
import os

###Data preparation

#Get mock data from local table
pie_df = pd.read_csv('/home/ubuntu/ID_UID.csv')
line_df = pd.read_csv('/home/ubuntu/Num_Sp.csv')
list_df = pd.read_csv('/home/ubuntu/Sp_Id.csv')

line = px.line(line_df, x="Year", y="Num_Sp", title="Number of Species by Year")

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
        Version 2.0: Mock Data Prototype
    '''),

	html.Div(
		dcc.Graph(
			id='line',
			figure=line
        )
    ),
    
    html.Div([
    	generate_table(list_df, 100)
    ], className="five columns"),
    
    html.Div([
    	dcc.Graph(id='pie-graph'),	
		dcc.Slider(
        	id='year--slider',
        	min=pie_df['Year'].min(),
        	max=pie_df['Year'].max(),
        	value=pie_df['Year'].max(),
        	marks={str(year): str(year) for year in pie_df['Year'].unique()},
        	step=None)
    ], className="six columns")
])

@app.callback(
	Output('pie-graph', 'figure'),
	[Input('year--slider', 'value')])
def update_pie(year_value):
	dff = pie_df[pie_df['Year'] == year_value]

	pie = px.pie(dff, values=[int(dff['ID']),int(dff['UID'])], names=['Identified', 'Unidentified'], title='Proportion of Reads Identified')
	  
	return pie

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True)