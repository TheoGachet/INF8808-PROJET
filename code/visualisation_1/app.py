# j'ai utilisé le TP3 comme base pour ajouter une visualisation dessusc

import dash
from dash import html, dcc, callback
import plotly.graph_objects as go
from dash.dependencies import Input, Output

# Import de la visualisation 1 (vide pour l’instant)
from visualisation_1.init import get_figure as viz1_get_figure
import visualisation_1.preprocess as preprocess
import visualisation_1.heatmap as heatmap


# Prétraitement des données pour la saison "Summer"
data = preprocess.convert_data('Summer')

# Création d'une figure vide pour la visualisation 1
empty_fig = viz1_get_figure()

# Définition de la mise en page de l'application
def get_viz_1_html():
    return html.Div([
        # En-tête de l'application
        html.Div([
            html.H2(
                "Who Rules the Podium ? Medal Count by Country Through the Years",  # Titre principal
                style={'textAlign': 'center', # Centrer le texte
                       'fontFamily': 'Playfair Display',
                       'color': '#000000'}
            ),
            html.Div(
                html.P([
                    "Every four years, the Olympic Games bring together the best athletes from around the world. But behind the medals and records lies another competition — one between nations, strategy, and sometimes... opportunity. ",
                    html.Br(), html.Br(),
                    "Have certain countries historically dominated the same sports over and over again ? Are powerhouses like the USA, China, or Russia unbeatable in specific disciplines ? And what happens when a country hosts the Olympics — do they influence the list of sports to improve their chances of winning more medals ? ",
                    html.Br(), html.Br(),
                    "Adding new sports, removing old ones, or adjusting event formats can sometimes raise eyebrows. Is it coincidence, or a clever tactic to tip the balance in favor of the host nation ? ",
                    html.Br(), html.Br(),
                    "This visualization explores decades of Olympic history to uncover patterns of dominance, national specialties, and the possible impact of hosting the Games. ",
                    html.Br(), html.Br(),
                    "Let’s see what the data reveals."],
                    style={
                        'textAlign': 'justify',  # Justifier le texte
                        'fontFamily': 'Inter',
                    }
                ),
                className="viz-description"
            )
        ]),
        # Contenu principal de l'application
        html.Div([
            # Bouton radio pour basculer entre les saisons
            dcc.RadioItems(
                id='season-toggle',  # Identifiant pour le composant
                options=[
                    {'label': 'Summer Olympics', 'value': 'Summer'},  # Option pour les Jeux d'été
                    {'label': 'Winter Olympics', 'value': 'Winter'}   # Option pour les Jeux d'hiver
                ],
                value='Summer',  # Valeur par défaut
                labelStyle={'display': 'inline-block', 'margin': '0 10px',"fontFamily": "Inter"},
                style={
                    'textAlign': 'center',  # Centrer le composant
                    'margin': '10px 0',  # Marges
                    'display': 'flex',  # Disposition en flexbox
                    'justify-content': 'center',  # Centrer horizontalement
                    'gap': '20px'  # Espacement entre les options
                }
            ),
            # Graphique pour afficher les visualisations
            dcc.Graph(
                id='viz1-graph',  # Identifiant pour le graphique
                figure=heatmap.create_multiple_heatmaps(data),  # Génération initiale du graphique
                config=dict(
                    scrollZoom=False,  # Désactiver le zoom avec la molette
                    showTips=False,  # Désactiver les infobulles
                    showAxisDragHandles=False,  # Désactiver les poignées de glissement des axes
                    doubleClick=False,  # Désactiver le double-clic
                    displayModeBar=False  # Masquer la barre d'outils
                )
            )
        ],
        className="centered"
        )
    ])

# Définition du callback pour mettre à jour le graphique en fonction de la saison sélectionnée
@callback(
    Output('viz1-graph', 'figure'),  # Mise à jour de la figure du graphique
    [Input('season-toggle', 'value')]  # Entrée : valeur sélectionnée dans le bouton radio
)
def update_figure(selected_season):
    # Prétraitement des données pour la saison sélectionnée
    data = preprocess.convert_data(selected_season)
    # Génération du graphique mis à jour
    return heatmap.create_multiple_heatmaps(data)