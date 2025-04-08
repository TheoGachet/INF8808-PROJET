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
            html.H2("Tracking Olympic Glory: Points Earned by Country Over the Years", style={"textAlign": "center", "color": "#009F3D", "fontFamily": "Playfair Display"}),
            html.Div(
                html.P(["This slopechart illustrates the evolution of Olympic performance by country across different editions of the Games, using a points-based system rather than the traditional medal count." \
                       " Each country's score is calculated by assigning a fixed number of points to each medal type (e.g., 3 for gold, 2 for silver, 1 for bronze), allowing for a more nuanced comparison of overall performance." \
                        " By focusing on total points instead of just medal total, this visualization highlights countries whose athletic excellence may be underappreciated when only gold medals are considered.",
                        html.Br(), html.Br(),
                        "This approach aims to better reflect the contributions of multi-medal-winning athletes, whose repeated successes can significantly influence their country's standing." \
                         " It also allows us to observe trends over time—revealing periods of dominance, decline, or resurgence in Olympic history.", 
                         html.Br(), html.Br(),
                         "Ultimately, this visualization invites viewers to reconsider how we measure Olympic success and to appreciate the collective and individual efforts that shape a nation’s Olympic legacy."
                ], style={"textAlign": "justify", "fontFamily": "Inter"}
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
            labelStyle={'display': 'inline-block', 'margin': '0 10px', "fontFamily": "Inter"},
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