# j'ai utilisé le TP3 comme base pour ajouter une visualisation dessus

import dash
from dash import html, dcc
import plotly.graph_objects as go

# Import de la visualisation 5 (vide pour l’instant)
from init import get_figure

app = dash.Dash(__name__)
app.title = "Projet INF8808"

fig = get_figure()

app.layout = html.Div([
    html.Header([
        html.H1("Projet INF8808"),
        html.H2("Visualisation 5")
    ]),
    html.Main([
        dcc.Graph(
            id='viz1-graph',
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
    app.run_server(debug=True)
