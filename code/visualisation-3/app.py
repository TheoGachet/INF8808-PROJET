# j'ai utilisé le TP3 comme base pour ajouter une visualisation dessusc

import dash
from dash import html, dcc
import plotly.graph_objects as go

import preprocess
import lolipop

app = dash.Dash(__name__)
app.title = 'TP3 | INF8808'

df = preprocess.load_csv("all_athlete_games.csv")
df = preprocess.preprocess_data(df)
fig = lolipop.create_lollipop_figure(df)



app.layout = html.Div([
    html.Header([
        html.H1("Visualisation des performances aux JO"),
        html.H2("Visualisation 3")
    ]),
    html.Main([
        dcc.Graph(
            id='lollipop-graph',
            figure=fig,
            config=dict(
                scrollZoom=False,
                showTips=False,
                showAxisDragHandles=False,
                doubleClick=False,
                displayModeBar=False
            )
        )
    ])
])

if __name__ == "__main__":
    app.run(debug=True)
