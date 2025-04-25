import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import visualisation_1.hover_template as hover
import os

# Charger le fichier CSV contenant les codes et noms des pays
path = os.path.join("data", 'Countries_codes_names.csv')
country_codes = pd.read_csv(path, sep=';')  # Lecture du fichier CSV avec les codes et noms des pays


def create_multiple_heatmaps(data):
    # Obtenir la liste des sports à partir des clés du dictionnaire `data`
    sports = list(data.keys())
    # num_sports = len(sports)  # Nombre total de sports

    # Définir le nombre de colonnes et de lignes pour les sous-graphiques
    cols = 4  # Nombre de colonnes (modifiable)
    rows = 4  # Nombre de lignes (modifiable)

    # Créer une figure avec des sous-graphiques
    fig = make_subplots(
        rows=rows,
        cols=cols,
        subplot_titles=[f"<b>{sport}</b>" for sport in sports],  # Ajouter les titres des sous-graphiques en gras
        horizontal_spacing=0.15,  # Espacement horizontal entre les sous-graphiques
        vertical_spacing=0.10,  # Espacement vertical entre les sous-graphiques
    )

    # Parcourir chaque sport pour créer les heatmaps
    for i, sport in enumerate(sports):
        if sport == "Host_Countries":  # Ignorer la clé "Host_Countries"
            continue
        df = pd.DataFrame(data[sport])  # Convertir les données du sport en DataFrame

        # Calculer la position du subplot (ligne et colonne)
        row = (i // cols) + 1
        col = (i % cols) + 1

        # Calculer le total des médailles par pays (inclut "Others")
        df['Total'] = df.sum(axis=1, numeric_only=True)

        # Trier les pays par total de médailles (y compris "Others")
        df = df.sort_values(by='Total', ascending=False)

        # S'assurer que "Others" est toujours en dernier
        if "Others" in df.index:
            df = pd.concat([df.drop(index="Others"), pd.DataFrame([df.loc["Others"]])])

        # Supprimer la colonne "Total" après le tri
        df.drop(columns=['Total'], inplace=True)

        # Inverser l'ordre des pays pour afficher le pays avec le plus de médailles en haut
        df = df.loc[df.index[::-1]]

        # Mapper les codes des pays aux noms complets
        country_mapping = dict(zip(country_codes['Code'], country_codes['Name']))
        y_labels = [country_mapping.get(code, code) for code in df.index]  # Générer les noms complets des pays

        # Créer une heatmap pour le sport courant
        heatmap = go.Heatmap(
            z=df.values,  # Valeurs des médailles
            x=df.columns,  # Années
            y=y_labels,  # Noms des pays
            xgap=5,  # Espacement horizontal entre les cases
            ygap=5,  # Espacement vertical entre les cases
            colorscale="Blues",  # Palette de couleurs
            colorbar=dict(
                x=0.15 + (col - 1) * 0.29,  # Position horizontale de la barre de couleurs
                y=0.91 - (row - 1) * (1.10 / rows),  # Position verticale de la barre de couleurs
                len=0.22  # Hauteur de la barre de couleurs
            ),
            hovertemplate=hover.get_hover_template(sport)  # Modèle d'informations pour le survol
        )

        # Ajouter la heatmap au subplot correspondant
        fig.add_trace(heatmap, row=row, col=col)

        # Ajouter des annotations pour les pays hôtes
        for year in df.columns:
            if year in data["Host_Countries"]:  # Vérifier si l'année est dans les pays hôtes
                host_country = data["Host_Countries"][year]
                if host_country in df.index:  # Vérifier si le pays hôte est dans les données
                    y_index = df.index.get_loc(host_country)  # Obtenir l'index du pays hôte

                    # Définir la taille du rectangle
                    size_x = 1.8
                    size_y = 0.5

                    # Ajouter un rectangle rouge autour du pays hôte
                    fig.add_shape(
                        type="rect",
                        x0=int(year) - size_x,  # Début de l'année avec une marge
                        x1=int(year) + size_x,  # Fin de l'année avec une marge
                        y0=y_index - size_y,  # Début du pays avec une marge
                        y1=y_index + size_y,  # Fin du pays avec une marge
                        xref=f"x{i+1}",  # Référence à l'axe x du subplot
                        yref=f"y{i+1}",  # Référence à l'axe y du subplot
                        line=dict(color="red", width=2),  # Style du rectangle
                    )

    # Ajouter une légende pour le rectangle rouge (pays organisateur)
    fig.add_trace(
        go.Scatter(
            x=[None],  # Valeur fictive pour la légende
            y=[None],
            mode="markers",
            marker=dict(
                size=12,
                color="red",
                symbol="square-open"  # Carré non rempli
            ),
            name="Host Country",  # Name in the legend
        )
    )

    # Mettre à jour la position de la légende pour qu'elle soit affichée en haut
    fig.update_layout(
        legend=dict(
            orientation="h",  # Légende horizontale
            yanchor="bottom",
            y=1.05,  # Position au-dessus des heatmaps
            xanchor="center",
            x=0.5  # Centrer la légende
        )
    )

    # Mettre à jour la mise en page globale
    fig.update_layout(
        font=dict(family="Inter"),  # Définir la police "Inter"
        font_size=14,  # Définir la taille du texte à 14
        height=rows * 370,  # Ajuster la hauteur en fonction du nombre de lignes
        width=cols * 370,  # Ajuster la largeur pour bien afficher les légendes
        showlegend=True,  # Activer la légende globale
    )

    return fig  # Retourner la figure finale