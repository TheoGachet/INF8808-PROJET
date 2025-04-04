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
            html.H1(
                "Nombre de médailles gagnés par pays selon les éditions",  # Titre principal
                style={'textAlign': 'center'}  # Centrer le texte
            ),
            html.Div(
                html.P(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt " \
                    "ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco " \
                    "laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in " \
                    "voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat " \
                    "non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
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