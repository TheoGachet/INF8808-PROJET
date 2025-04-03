# j'ai utilisé le TP3 comme base pour ajouter une visualisation dessusc

import dash
from dash import html, dcc, callback
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Import de la visualisation 1 (vide pour l’instant)
# from init import get_figure as viz1_get_figure
import visualisation_1.preprocess as preprocess
import visualisation_1.heatmap as heatmap

# app = dash.Dash(__name__)
# app.title = "Projet INF8808"

data = preprocess.convert_data('Summer')

# empty_fig = viz1_get_figure()

# Ajout du bouton pour changer de saison
# app.layout = html.Div([
#     html.Header([
#         html.H2(
#             "Nombre de médailles gagnés par pays selon les éditions",
#             style={'textAlign': 'center'}
#         )
#     ]),
#     html.Main([
#         dcc.RadioItems(
#             id='season-toggle',
#             options=[
#                 {'label': 'Summer Olympics', 'value': 'Summer'},
#                 {'label': 'Winter Olympics', 'value': 'Winter'}
#             ],
#             value='Summer',
#             style={'textAlign': 'center', 'margin': '10px 0', 'display': 'flex', 'justify-content': 'center', 'gap': '20px'}
#         ),
#         dcc.Graph(
#             id='viz1-graph',
#             figure=heatmap.create_multiple_heatmaps(data),
#             config=dict(
#                 scrollZoom=False,
#                 showTips=False,
#                 showAxisDragHandles=False,
#                 doubleClick=False,
#                 displayModeBar=False
#             )
#         )
#     ])
# ])

def get_figure_html():
    return html.Div([
        html.Div([
            html.H2(
                "Nombre de médailles gagnés par pays selon les éditions",
                style={'textAlign': 'center'}
            )
        ]),
        html.Div([
            dcc.RadioItems(
                id='season-toggle',
                options=[
                    {'label': 'Summer Olympics', 'value': 'Summer'},
                    {'label': 'Winter Olympics', 'value': 'Winter'}
                ],
                value='Summer',
                style={'textAlign': 'center', 'margin': '10px 0', 'display': 'flex', 'justify-content': 'center', 'gap': '20px'}
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

# def get_callbacks_output():
#     return [Output('viz1-graph', 'figure')]

# def get_callbacks_input():
#     return [Input('season-toggle', 'value')]

# Callback pour changer entre les saisons
@callback(
    Output('viz1-graph', 'figure'),
    [Input('season-toggle', 'value')]
    )
def update_figure(selected_season):
    # Replace this with the logic to update the figure based on the selected season
    data = preprocess.convert_data(selected_season)
    return heatmap.create_multiple_heatmaps(data)

    # if __name__ == "__main__":
    #     app.run_server(debug=True)
