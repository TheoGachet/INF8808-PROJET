import dash
from dash import html, dcc, Input, Output
import preprocess_ete_hiver
import lolipop

app = dash.Dash(__name__)
app.title = 'TP3 | INF8808'

# Initial load
df = preprocess_ete_hiver.load_csv("all_athlete_games.csv")
df_filtered = preprocess_ete_hiver.preprocess_data(df, season="Summer")  # default is Summer
fig = lolipop.create_lollipop_figure(df_filtered, season="Summer")  # <-- season added

app.layout = html.Div([
    html.Header([
        html.H1("Visualization of Olympic Performances", style={"textAlign": "center"}),
    ]),
    html.Div([
        html.H2("Comparison of Host Countries' Olympic Performances", style={"textAlign": "center"}),
        html.Div([
            dcc.RadioItems(
                id='season-filter',
                options=[
                    {"label": "Summer Olympics", "value": "Summer"},
                    {"label": "Winter Olympics", "value": "Winter"}
                ],
                value="Summer",
                labelStyle={'display': 'inline-block', 'margin': '0 10px'},
                inputStyle={"margin-right": "5px"}
            )
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        dcc.Graph(id='lollipop-graph', figure=fig)
    ])
])


@app.callback(
    Output('lollipop-graph', 'figure'),
    Input('season-filter', 'value')
)
def update_figure(selected_season):
    df_filtered = preprocess_ete_hiver.preprocess_data(df, season=selected_season)
    fig = lolipop.create_lollipop_figure(df_filtered, season=selected_season)  # <-- season added here too
    return fig

if __name__ == "__main__":
    app.run(debug=True)
