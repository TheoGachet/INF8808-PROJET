import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def create_multiple_heatmaps(data):
    sports = list(data.keys())  # Liste des sports
    num_sports = len(sports)  # Nombre total de sports

    # Définition du nombre de colonnes et lignes pour les subplots
    cols = 4  # Nombre de colonnes (modifiable)
    rows = 4  # Nombre de lignes (modifiable)

    # Création de la figure avec sous-graphiques
    fig = make_subplots(
        rows = rows,
        cols = cols,
        subplot_titles = sports,  # Titres des sous-graphiques
        horizontal_spacing = 0.15,
        vertical_spacing = 0.15
    )

    # Parcours de chaque sport pour créer les heatmaps
    for i, sport in enumerate(sports):
        df = pd.DataFrame(data[sport])  # Convertir en DataFrame

        # Position du subplot (ligne et colonne)
        row = (i // cols) + 1
        col = (i % cols) + 1

        heatmap = go.Heatmap(
            z = df.values,
            x = df.columns,  # Années
            y = df.index,  # Pays
            xgap = 5,  # Espacement horizontal entre les cases
            ygap = 5,   # Espacement vertical entre les cases
            colorscale = "Blues",
            colorbar = dict(
                x = 0.15 + (col - 1) * 0.29,  # Décale la légende à droite de chaque heatmap
                y = 0.93 - (row - 1) * (1.15 / rows),  # Aligne la légende avec chaque subplot
                len = 0.2  # Ajuste la hauteur de la barre de couleurs
            )
        )

        # Ajout du heatmap au subplot correspondant
        fig.add_trace(heatmap, row=row, col=col)

    # Mise à jour de la mise en page globale
    fig.update_layout(
        height = rows * 450,  # Ajustement de la hauteur en fonction du nombre de lignes
        width = cols * 450,  # Augmentation de la largeur pour bien afficher les légendes
        showlegend = False  # Désactiver la légende globale
    )

    return fig