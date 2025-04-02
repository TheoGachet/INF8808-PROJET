# j'ai utilisé le TP3 comme base pour ces fichiers

import plotly.graph_objects as go

def get_figure():
    """
    Placeholder pour la Visualisation 4.
    """
    # Création d'une figure vide avec Plotly
    fig = go.Figure()
    
    # Ajout d'une annotation au centre de la figure
    fig.add_annotation(
        text="Visualisation 1 non implémentée",  # Texte affiché dans l'annotation
        xref="paper", yref="paper",  # Références pour positionner l'annotation par rapport à la figure
        x=0.5, y=0.5,  # Position de l'annotation (au centre de la figure)
        showarrow=False,  # Pas de flèche pour l'annotation
        font=dict(size=16)  # Taille de la police du texte
    ) 
    
    # Mise à jour de la mise en page de la figure
    fig.update_layout(
        xaxis=dict(visible=False),  # Cache l'axe des x
        yaxis=dict(visible=False),  # Cache l'axe des y
        plot_bgcolor="rgba(0,0,0,0)",  # Définit un fond transparent pour la zone de tracé
        paper_bgcolor="rgba(0,0,0,0)"  # Définit un fond transparent pour la figure
    )
    
    # Retourne l'objet figure créé avec les annotations et le style définis
    return fig
