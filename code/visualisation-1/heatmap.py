import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import hover_template as hover


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
        if sport == "Host_Countries":
            continue
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
            ),
            hovertemplate=hover.get_hover_template(sport)  # Ajout des informations manquantes
        )

        # Ajout du heatmap au subplot correspondant
        fig.add_trace(heatmap, row=row, col=col)

        # Ajouter des annotations pour les pays hôtes
        for year in df.columns:
            if year in data["Host_Countries"]:
                host_country = data["Host_Countries"][year]
                if host_country in df.index:
                    y_index = df.index.get_loc(host_country)

                    # Définir la taille du rectangle
                    size_x = 1.8
                    size_y = 0.5
                    
                    fig.add_shape(
                        type="rect",
                        x0=int(year) - size_x,  # Début de l'année avec une marge
                        x1=int(year) + size_x,  # Fin de l'année avec une marge
                        y0=y_index - size_y,  # Début du pays avec une marge
                        y1=y_index + size_y,  # Fin du pays avec une marge
                        xref=f"x{i+1}",
                        yref=f"y{i+1}",
                        line=dict(color="red", width=2),
                    )

    # Mise à jour de la mise en page globale
    fig.update_layout(
        height = rows * 370,  # Ajustement de la hauteur en fonction du nombre de lignes
        width = cols * 370,  # Augmentation de la largeur pour bien afficher les légendes
        showlegend = False  # Activer la légende globale
    )

    return fig