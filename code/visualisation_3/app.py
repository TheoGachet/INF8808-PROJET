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
            ], style={'textAlign': 'center', 'margin': '20px 20px'}),
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