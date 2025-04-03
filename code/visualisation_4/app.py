import dash
from dash import dcc, html, Input, Output
from init import get_output
from preprocess import load_csv  # utilisé pour charger le CSV des disciplines

app = dash.Dash(__name__)
app.title = "Projet INF8808 - Visualisation Textuelle"

app.layout = html.Div([
    html.H1("Visualisation 4 - Athlètes par Pays"),
    
    html.Div([
        html.Label("Sélectionner le type de Jeux:"),
        dcc.RadioItems(
            id='season-radio',
            options=[{'label': s, 'value': s} for s in ["Summer", "Winter"]],
            value='Summer',
            labelStyle={'display': 'inline-block', 'margin-right': '10px'}
        ),
    ], style={'margin-bottom': '20px'}),
    
    html.Div([
        html.Label("Sélectionner une discipline:"),
        dcc.Dropdown(
            id='discipline-dropdown',
            options=[],  # options mises à jour par le callback
            value=None
        ),
    ], style={'width': '50%', 'margin-bottom': '20px'}),
    
    html.Hr(),
    html.Div(id='output-text', style={'whiteSpace': 'pre-line', 'fontFamily': 'monospace'})
])

# Callback pour mettre à jour la liste des disciplines en fonction de la saison sélectionnée.
@app.callback(
    [Output('discipline-dropdown', 'options'),
     Output('discipline-dropdown', 'value')],
    [Input('season-radio', 'value')]
)
def update_discipline_dropdown(season):
    # Charger le CSV des disciplines correspondant à la saison (par exemple disciplines_summer.csv)
    filename = f"disciplines_{season.lower()}.csv"
    df_disc = load_csv(filename)
    # On utilise la colonne "discipline" (en minuscules)
    disciplines = sorted(df_disc["discipline"].dropna().unique())
    options = [{'label': d, 'value': d} for d in disciplines]
    # Sélectionne la première discipline par défaut, si disponible
    value = options[0]['value'] if options else None
    return options, value

# Callback pour mettre à jour l'affichage en fonction de la saison et de la discipline sélectionnées.
@app.callback(
    Output('output-text', 'children'),
    [Input('season-radio', 'value'),
     Input('discipline-dropdown', 'value')]
)
def update_output(season, discipline):
    if not season or not discipline:
        return "Veuillez sélectionner un type de Jeux et une discipline."
    return get_output(season, discipline)

if __name__ == '__main__':
    app.run_server(debug=True)
