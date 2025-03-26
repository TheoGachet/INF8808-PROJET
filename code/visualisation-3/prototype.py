import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_lollipop_figure(df):
    fig = make_subplots(
        rows=3, cols=2,
        shared_yaxes=False,  # ✅ Chaque colonne a ses propres ordonnées
        subplot_titles=[
            "Nombre moyen d’athlètes (1945–1991)", "Nombre moyen d’athlètes (1992–2020)",
            "Nombre moyen de médailles (1945–1991)", "Nombre moyen de médailles (1992–2020)",
            "Médailles par athlète (1945–1991)", "Médailles par athlète (1992–2020)"
        ]
    )

    metrics = [
        ('Athletes', 'Nombre moyen d’athlètes'),
        ('Medals', 'Nombre moyen de médailles'),
        ('Ratio', 'Médailles par athlète')
    ]
    periods = ['1945-1991', '1992-2020']

    for i, (metric, _) in enumerate(metrics):
        for j, period in enumerate(periods):
            row, col = i + 1, j + 1

            df_period = df[df['Period'] == period]
            df_period = df_period[~df_period[f"{metric}_Host"].isna()].sort_values("Team").reset_index(drop=True)

            y_pos = df_period.index  # valeurs numériques
            countries = df_period["Team"]  # noms des pays

            away_vals = df_period[f"{metric}_Away"]
            host_vals = df_period[f"{metric}_Host"]

            # Ajout de chaque paire de points + segment
            for y, away, host in zip(y_pos, away_vals, host_vals):
                color = 'black' if host >= away else 'blue'

                fig.add_trace(go.Scatter(
                    x=[away, host],
                    y=[y, y],
                    mode='lines',
                    line=dict(color=color),
                    showlegend=False
                ), row=row, col=col)

                fig.add_trace(go.Scatter(
                    x=[away],
                    y=[y],
                    mode='markers',
                    marker=dict(color='green', size=8),
                    name='À l’extérieur',
                    showlegend=(i == 0 and j == 0)  # ✅ Une seule fois
                ), row=row, col=col)

                fig.add_trace(go.Scatter(
                    x=[host],
                    y=[y],
                    mode='markers',
                    marker=dict(color='red', size=8),
                    name='À domicile',
                    showlegend=(i == 0 and j == 0)  # ✅ Une seule fois
                ), row=row, col=col)

            # Affichage des pays uniquement pour la colonne de gauche
            if j == 0:
                fig.update_yaxes(
                    tickvals=y_pos,
                    ticktext=countries,
                    row=row, col=col
                )
            else:
                fig.update_yaxes(
                    showticklabels=False,
                    row=row, col=col
                )

    fig.update_layout(
        height=900,
        title="Comparaison des performances des pays organisateurs des JO",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
            title=None
        ),
        margin=dict(t=100)
    )

    return fig
