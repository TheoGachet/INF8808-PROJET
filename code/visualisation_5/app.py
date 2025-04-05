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
            html.H1("Visualisation 5 (TODO: changer ce titre)", style={"textAlign": "center"}),
        ]),
        dcc.Dropdown(
            id='dropdown-pays',
            options=[{'label': p, 'value': s} for (s, p) in pays_disponibles],
            value=pays,  # Valeur par défaut
            placeholder="Select a country",
            style={'width': '50%', 'margin': '0 auto'}
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