import visualisation_3.hover_template as hover_template
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from visualisation_3.hover_template import get_host_years_by_country, get_hover_template

def create_lollipop_figure(df,season):
    host_years_map = get_host_years_by_country(season)

    fig = make_subplots(
        rows=3, cols=2, shared_yaxes=False,
        vertical_spacing=0.06,
        horizontal_spacing=0.03,
        subplot_titles=[
            "Nombre moyen d’athlètes (1945–1991)", "Nombre moyen d’athlètes (1992–2020)",
            "Nombre moyen de médailles (1945–1991)", "Nombre moyen de médailles (1992–2020)",
            "Médailles par athlète (1945–1991)", "Médailles par athlète (1992–2020)"
        ]
    )

    metrics = [
        ('Athletes', 'athlètes'),
        ('Medals', 'médailles'),
        ('Ratio', 'médailles par athlète')
    ]
    periods = ['1945-1991', '1992-2020']

    added_legends = {'away': False, 'host': False, 'adv_home': False, 'adv_away': False}

    for j, period in enumerate(periods):
        df_period = df[(df['Period'] == period) & (df['Athletes_Host'] > 0)].copy()
        df_period = df_period.sort_values(f"{metrics[0][0]}_Away", ascending=False)
        y_labels = df_period['Team'].tolist()
        y_pos = list(range(len(y_labels)))

        for i, (metric, label_name) in enumerate(metrics):
            away_vals = df_period[f"{metric}_Away"].tolist()
            host_vals = df_period[f"{metric}_Host"].tolist()
            row, col = i + 1, j + 1

            for y_idx, (country, away, host) in enumerate(zip(y_labels, away_vals, host_vals)):
                color = 'black' if host >= away else 'blue'
                host_years = host_years_map.get(period, {}).get(country, [])
                host_years_str = ", ".join(map(str, host_years)) if host_years else "N/A"

                # Décalage léger pour éviter superposition
                delta = 0.001 if metric == "Ratio" else 1
                if abs(host - away) < delta:
                    away -= 2*delta
                    host += 2*delta 

                away = float(away) if away is not None else 0
                host = float(host) if host is not None else 0

                # Ligne
                fig.add_trace(go.Scatter(
                    x=[away, host],
                    y=[y_idx, y_idx],
                    mode='lines',
                    line=dict(color=color),
                    showlegend=not added_legends['adv_home'] if color == 'black' else not added_legends['adv_away'],
                    name='Avantage domicile' if color == 'black' else 'Avantage à l’extérieur',
                    hoverinfo='skip'
                ), row=row, col=col)
                added_legends['adv_home' if color == 'black' else 'adv_away'] = True

                # Point extérieur
                fig.add_trace(go.Scatter(
                    x=[away],
                    y=[y_idx],
                    mode='markers',
                    marker=dict(color='green', size=8),
                    name='À l’extérieur',
                    customdata = [[country]],
                    hovertemplate=hover_template.get_hover_template(label_name, is_host=False),
                    showlegend=not added_legends['away']
                ), row=row, col=col)
                added_legends['away'] = True

                # Point domicile
                fig.add_trace(go.Scatter(
                    x=[host],
                    y=[y_idx],
                    mode='markers',
                    marker=dict(color='red', size=8),
                    name='À domicile',
                    customdata=[[country, ', '.join(map(str, host_years)) if host_years else 'N/A']],
                    hovertemplate=hover_template.get_hover_template(label_name, is_host=True),
                    showlegend=not added_legends['host']
                ), row=row, col=col)
                added_legends['host'] = True

            # Y axes
            fig.update_yaxes(
                tickvals=list(range(len(y_labels))),
                ticktext=y_labels,
                side="right" if col == 2 else "left",
                row=row,
                col=col
            )

    fig.update_layout(
        height=950,
        margin=dict(t=140),
        legend=dict(
            title=dict(text="Légende"),
            orientation="h",
            yanchor="bottom",
            y=1.05,
            xanchor="center",
            x=0.5
        )
    )

    return fig
