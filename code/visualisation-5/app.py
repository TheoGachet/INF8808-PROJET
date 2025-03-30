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

pays_disponibles = preprocess.sigles_pays

app = dash.Dash(__name__)
app.title = "Projet INF8808"

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown-pays',
        options=[{'label': p, 'value': p} for p in pays_disponibles],
        value=pays,  # Valeur par défaut
        placeholder="Sélectionnez un pays"
    ),
    dcc.RadioItems(
        id='season-toggle',
        options=[
            {'label': 'Été', 'value': 'ete'},
            {'label': 'Hiver', 'value': 'hiver'}
        ],
        value='ete',
        inline=True
    ),
    dcc.Graph(id='slopechart')
])

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