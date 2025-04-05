# j'ai utilisé le TP3 comme base pour ces fichiers

import plotly.graph_objects as go

def get_figure():
    """
    Placeholder pour la Visualisation 4.
    """
    fig = go.Figure()
    fig.add_annotation(
        text="Visualisation 4 non implémentée",
        xref="paper", yref="paper",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=16)
    ) 
    fig.update_layout(
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig
