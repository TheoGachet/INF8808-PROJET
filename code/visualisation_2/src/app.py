
# -*- coding: utf-8 -*-

'''
    File name: app.py
    Author: Olivia Gélinas
    Course: INF8808
    Python Version: 3.8

    This file contains the source code for TP4.
'''

from dash import callback
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output

import plotly.graph_objects as go

import visualisation_2.src.preprocess as preprocess
import visualisation_2.src.bubble as bubble
from pathlib import Path
import os
import pandas as pd 

DATA_FOLDER = Path(os.path.abspath(__file__)).parent
PATH_PROCESSED_NON_SEASONAL_DATA = DATA_FOLDER / "vis_2_processed_data_1.csv"
PATH_PROCESSED_SEASONAL_DATA = DATA_FOLDER / "vis_2_processed_data_2.csv"

# create fig for first graph without seasons
def generate_fig(df, graph_id: int = 1):
    df["Population"] = pd.to_numeric(df["Population"] , errors="coerce")
    df["nb_medals"] = pd.to_numeric(df["nb_medals"] , errors="coerce")
    df["PIB_per_Capita"] = pd.to_numeric(df["PIB_per_Capita"] , errors="coerce")

    df = preprocess.round_decimals(df)
    if graph_id == 1:
        df = preprocess.sort_dy_by_yr_continent(df)
    else:
        df = preprocess.sort_dy_by_yr_climate(df)

    fig = bubble.get_plot(df, graph_id)
    fig = bubble.update_animation_hover_template(fig)
    fig = bubble.update_animation_menu(fig)
    fig = bubble.update_axes_labels(fig)
    fig = bubble.update_template(fig)
    fig = bubble.update_legend(fig)

    fig.update_layout(height=650, width=650)
    fig.update_layout(dragmode=False)

    return fig

non_sesonal_df = preprocess.get_df(PATH_PROCESSED_NON_SEASONAL_DATA)
seasonal_df = preprocess.get_df(PATH_PROCESSED_SEASONAL_DATA)
fig1 = generate_fig(non_sesonal_df, 1)
fig2 = generate_fig(seasonal_df, 2)

def update_figure(selected_seasons):
    # Filter the dataframe based on checkbox selection
    if len(selected_seasons) == 2:
        filtered_df = non_sesonal_df
    else:
        print(selected_seasons)
        filtered_df = seasonal_df[seasonal_df['Season'] == selected_seasons[0]]
    
    filtered_df = preprocess.sort_dy_by_yr_climate(filtered_df)

    # Rebuild the figure with the filtered data
    fig = bubble.get_plot(filtered_df, 2)
    fig = bubble.update_animation_hover_template(fig)
    fig = bubble.update_animation_menu(fig)
    fig = bubble.update_axes_labels(fig)
    fig = bubble.update_template(fig)
    fig = bubble.update_legend(fig)
    fig.update_layout(height=600, width=650)

    return fig

callback(
    Output('bubble-graph-2', 'figure'),
    Input('viz2-season-filter', 'value')
)(update_figure)

def get_viz_2_html():
    return html.Div(className='content', children=[
        html.Div(children=[
            html.H1('Total Medals / PIB per Capita ($ USD)', style={'textAlign': 'center'}),
            html.Div(
                html.P(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt " \
                    "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco " \
                    "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in " \
                    "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat " \
                    "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                ),
                className="viz-description"
            )
        ]),

        html.Div(className='viz-container', style={'display': 'flex', 'justifyContent': 'center', 'gap': '40px'}, children=[
            
            # First graph only
            dcc.Graph(className='graph', figure=fig1, config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )),

            # Second graph + checkboxes
            html.Div(style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'}, children=[
                # Checkboxes underneath
                html.Div([
                    dcc.Checklist(
                        id='viz2-season-filter',
                        options=[
                            {'label': 'Hiver', 'value': 'Winter'},
                            {'label': 'Été', 'value': 'Summer'}
                        ],
                        value=['Winter', 'Summer'],
                        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
                        inputStyle={'margin-right': '6px'}
                    )
                ], style={'marginBottom': '20px', 'textAlign': 'center'}),

                dcc.Graph(id='bubble-graph-2', className='graph', figure=fig2, config=dict(
                    scrollZoom=False,
                    showTips=False,
                    showAxisDragHandles=False,
                    doubleClick=False,
                    displayModeBar=False
                )),
            ])
        ])
    ])
