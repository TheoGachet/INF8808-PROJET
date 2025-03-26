import plotly.graph_objects as go
from plotly.subplots import make_subplots

def create_lollipop_figure(df):
    fig = make_subplots(
        rows=3, cols=2, shared_yaxes=False,
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

    added_legends = {'away': False, 'host': False}

    for j, period in enumerate(periods):  # Colonnes
        df_period = df[(df['Period'] == period) & (df['Athletes_Host'] > 0)].copy()
        df_period = df_period.sort_values("Team")
        y_labels = df_period['Team'].tolist()
        y_pos = list(range(len(y_labels)))

        for i, (metric, _) in enumerate(metrics):  # Lignes
            away_vals = df_period[f"{metric}_Away"].tolist()
            host_vals = df_period[f"{metric}_Host"].tolist()
            row, col = i + 1, j + 1

            for y_idx, (y, away, host) in enumerate(zip(y_labels, away_vals, host_vals)):
                color = 'black' if host >= away else 'blue'

                fig.add_trace(go.Scatter(
                    x=[away, host],
                    y=[y_idx, y_idx],
                    mode='lines',
                    line=dict(color=color),
                    showlegend=False
                ), row=row, col=col)

                fig.add_trace(go.Scatter(
                    x=[away],
                    y=[y_idx],
                    mode='markers',
                    marker=dict(color='green', size=8),
                    name='À l’extérieur',
                    showlegend=not added_legends['away']
                ), row=row, col=col)
                added_legends['away'] = True

                fig.add_trace(go.Scatter(
                    x=[host],
                    y=[y_idx],
                    mode='markers',
                    marker=dict(color='red', size=8),
                    name='À domicile',
                    showlegend=not added_legends['host']
                ), row=row, col=col)
                added_legends['host'] = True

            # Afficher les ticks seulement pour les graphiques de gauche
            fig.update_yaxes(
                tickvals=list(range(len(y_labels))),
                ticktext=y_labels if col == 1 else [''] * len(y_labels),
                row=row,
                col=col
            )

    fig.update_layout(
        height=950,
        title="Comparaison des performances des pays organisateurs des JO",
        margin=dict(t=100),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        )
    )

    return fig
