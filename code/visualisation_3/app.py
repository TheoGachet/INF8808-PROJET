import dash
from dash import html, dcc, Input, Output, callback
import visualisation_3.preprocess_ete_hiver as preprocess_ete_hiver
import visualisation_3.lolipop as lolipop

# Initial load
df = preprocess_ete_hiver.load_csv("all_athlete_games.csv")
df_filtered = preprocess_ete_hiver.preprocess_data(df, season="Summer")  # par défaut été
fig = lolipop.create_lollipop_figure(df_filtered, season="Summer")  # <-- saison ajoutée

def get_viz_3_html():
    return html.Div([
        html.Div([
            html.H1("Visualisation des performances aux JO", style={"textAlign": "center"}),
        ]),
        html.Div([
            html.H2("Comparaison des performances des pays organisateurs des JO", style={"textAlign": "center"}),
            html.Div([
                dcc.RadioItems(
                    id='season-filter',
                    options=[
                        {"label": "Jeux d'été", "value": "Summer"},
                        {"label": "Jeux d'hiver", "value": "Winter"}
                    ],
                    value="Summer",
                    labelStyle={'display': 'inline-block', 'margin': '0 10px'},
                    inputStyle={"margin-right": "5px"}
                )
            ], style={'textAlign': 'center', 'marginBottom': '20px'}),
            dcc.Graph(id='lollipop-graph', figure=fig)
        ])
    ])


@callback(
    Output('lollipop-graph', 'figure'),
    Input('season-filter', 'value')
)
def update_figure(selected_season):
    df_filtered = preprocess_ete_hiver.preprocess_data(df, season=selected_season)
    fig = lolipop.create_lollipop_figure(df_filtered, season=selected_season)  # <-- saison ajoutée ici aussi
    return fig