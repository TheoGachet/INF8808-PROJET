# j'ai utilisé le TP3 comme base pour ajouter une visualisation dessusc

import dash
from dash import html, dcc
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Import de la visualisation 1 (vide pour l’instant)
from init import get_figure as viz1_get_figure
import preprocess
import heatmap
import seasons

app = dash.Dash(__name__)
app.title = "Projet INF8808"

data = preprocess.convert_data()

empty_fig = viz1_get_figure()

# Ajout du bouton pour changer de saison
app.layout = html.Div([
    html.Header([
        html.H1("Projet INF8808"),
        html.H2("Visualisation 1")
    ]),
    html.Main([
        dcc.RadioItems(
            id='season-toggle',
            options=[
                {'label': 'Été', 'value': 'été'},
                {'label': 'Hiver', 'value': 'hiver'}
            ],
            value='été',
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(
            id='viz1-graph',
            figure=heatmap.create_multiple_heatmaps(data),
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

# Callback pour changer entre les saisons
@app.callback(
    Output('viz1-graph', 'figure'),
    [Input('season-toggle', 'value')]
)
def update_figure(selected_season):
    # Replace this with the logic to update the figure based on the selected season
    return heatmap.create_multiple_heatmaps(data)

if __name__ == "__main__":
    app.run_server(debug=True)
