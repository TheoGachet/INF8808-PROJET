import dash
from dash import html, dcc, Dash
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output

import preprocess
import slopechart

df = preprocess.load_csv("all_athlete_games.csv")

pays = "USA"
season = "ete"
fig = slopechart.viz_5(df, pays, season)

pays_disponibles = preprocess.pays_dispo

app = dash.Dash(__name__)
app.title = "Projet INF8808"

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-pays',
        options=[{'label': p, 'value': s} for (s, p) in pays_disponibles],
        value=pays,  # Valeur par défaut
        placeholder="Select a country",
        style={'width': '50%', 'margin': '0 auto'}
    ),
    dcc.RadioItems(
        id='season-toggle',
        options=[
            {'label': 'Summer', 'value': 'ete'},
            {'label': 'Winter', 'value': 'hiver'}
        ],
        value='ete',
        inline=True,
        style={'textAlign': 'center', 'margin': '10px 0'}
    ),
    dcc.Graph(
        id='slopechart'
    )
], style={'textAlign': 'center'})  # Centrer tout le contenu

@app.callback(
    Output('slopechart', 'figure'),
    [Input('dropdown-pays', 'value'),
     Input('season-toggle', 'value')]
)
def update_slopechart(pays, season):
    fig = slopechart.viz_5(df, pays, season)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)