
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for TP4.
'''
import json

import dash
import dash_html_components as html
import dash_core_components as dcc

import pandas as pd

import preprocess
import bubble

app = dash.Dash(__name__)
app.title = 'TP4 | INF8808'

df_2000 = pd.json_normalize(data, '2000')
df_2015 = pd.json_normalize(data, '2015')

df_2000 = preprocess.round_decimals(df_2000)
df_2015 = preprocess.round_decimals(df_2015)

gdp_range = preprocess.get_range('GDP', df_2000, df_2015)
co2_range = preprocess.get_range('CO2', df_2000, df_2015)

df = preprocess.combine_dfs(df_2000, df_2015)
df = preprocess.sort_dy_by_yr_continent(df)

fig = bubble.get_plot(df, gdp_range, co2_range)
fig = bubble.update_animation_hover_template(fig)
fig = bubble.update_animation_menu(fig)
fig = bubble.update_axes_labels(fig)
fig = bubble.update_template(fig)
fig = bubble.update_legend(fig)

fig.update_layout(height=600, width=1000)
fig.update_layout(dragmode=False)

app.layout = html.Div(className='content', children=[
    html.Header(children=[
        html.H1('GDP vs. CO2 emissions'),
        html.H2('In countries around the world')
    ]),
    html.Main(className='viz-container', children=[
        dcc.Graph(className='graph', figure=fig, config=dict(
            scrollZoom=False,
            showTips=False,
            showAxisDragHandles=False,
            doubleClick=False,
            displayModeBar=False
            ))
    ])
])
