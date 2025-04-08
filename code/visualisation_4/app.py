import dash
from dash import dcc, html, Input, Output, callback
from visualisation_4.init import get_output
from visualisation_4.preprocess import load_csv  # utilisé pour charger le CSV des disciplines

def get_viz_4_html():
    return html.Div([
        html.Div([
            html.H1("3. Can Individual Talent Elevate an Entire Nation?", style={'textAlign': 'center', 'marginBottom': '20px'}),
            html.P([
                "Does being the host country boost your performance — or is it just a myth?",
                html.Br(),
                "We compare how countries perform at home versus abroad to reveal if hosting gives athletes a psychological or logistical edge. The results may surprise you.",
            ], style={"textAlign": "justify", "backgroundColor": "#fdfdfd", 'marginBottom': '40px'},
                className="viz-description"
            )
        ]),  # ✅ Parenthèse fermante ajoutée ici pour la première Div

        html.Div([
            html.H2("Where are Olympic Champions from ? A Global Map of Sport Legends", style={"textAlign": "center",'color': '#F4C300', 'marginBottom': '40px'}),
            html.Div(
                html.P([
                    "Behind every Olympic champion, there’s not just talent — there’s also a country, a culture, and sometimes, a system built to create greatness.",
                    html.Br(),html.Br(),
                    "Some nations seem to have an extraordinary ability to produce legendary athletes — those rare competitors who collect medal after medal and leave a lasting mark on Olympic history. But are these sporting icons just isolated cases of individual brilliance? Or do certain countries consistently shape and nurture these exceptional talents?",
                    html.Br(),html.Br(),
                    "This visualization dives into the origins of the most decorated Olympians — athletes who have won more than 5 medals in their career — to uncover which countries truly dominate when it comes to producing greatness.",
                    html.Br(),html.Br(),
                    "Talent might be universal… but is Olympic glory?",
                    ], style={
                        'textAlign': 'justify',
                        'fontFamily': 'Helvetica, sans-serif'
                    }) ,
                className="viz-description"
                
            )
        ]),

        html.Div([
            html.Label("Sélectionner le type de Jeux:"),
            dcc.RadioItems(
                id='season-radio',
                options=[{'label': s, 'value': s} for s in ["Summer", "Winter"]],
                value='Summer',
                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
            ),
        ], style={'margin': '20px 20px'}),

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
    ], className="centered")


# Callback pour mettre à jour la liste des disciplines en fonction de la saison sélectionnée.
@callback(
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
@callback(
    Output('output-text', 'children'),
    [Input('season-radio', 'value'),
     Input('discipline-dropdown', 'value')]
)
def update_output(season, discipline):
    if not season or not discipline:
        return "Veuillez sélectionner un type de Jeux et une discipline."
    return get_output(season, discipline)