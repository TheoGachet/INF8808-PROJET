import dash
from dash import html, dcc, Dash, callback
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output

import visualisation_5.preprocess as preprocess
import visualisation_5.slopechart as slopechart

df = preprocess.load_csv("all_athlete_games.csv")

pays = "USA"
season = "ete"
fig = slopechart.viz_5(df, pays, season)

pays_disponibles = preprocess.pays_dispo

def get_viz_5_html():
    return html.Div([
        html.Div([
            html.H1("Vizualisation 5: Points scored by the countries with and withiout the multi-medalist athletes", style={"textAlign": "center"}),
            html.Div(
                html.P(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt " \
                    "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco " \
                    "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in " \
                    "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat " \
                    "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
                ),
                className="viz-description"
            ),
        ]),
        html.Div(
            dcc.Dropdown(
                id='dropdown-pays',
                options=[{'label': p, 'value': s} for (s, p) in pays_disponibles],
                value=pays,
                placeholder="Select a country",
                style={"width": "200px", 'margin': '20px 20px', 'textAlign': 'center'},
            ),
            className='centered'
        ),
        dcc.RadioItems(
            id='viz5-season-toggle',
            options=[
                {'label': 'Summer Olympics', 'value': 'ete'},
                {'label': 'Winter Olympics', 'value': 'hiver'}
            ],
            value='ete',
            inline=True,
            style={'textAlign': 'center', 'margin': '10px 0'}
        ),
        dcc.Graph(
            id='slopechart'
        )
    ], style={'textAlign': 'center'})  # Centrer tout le contenu

@callback(
    Output('slopechart', 'figure'),
    [Input('dropdown-pays', 'value'),
     Input('viz5-season-toggle', 'value')]
)
def update_slopechart(pays, season):
    fig = slopechart.viz_5(df, pays, season)
    return fig