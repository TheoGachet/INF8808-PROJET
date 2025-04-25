import visualisation_3.hover_template as hover_template
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from visualisation_3.hover_template import get_host_years_by_country, get_hover_template

def create_lollipop_figure(df, season, top_margin=240):
    host_years_map = get_host_years_by_country(season)

    fig = make_subplots(
        rows=3, cols=2, shared_yaxes=False,
        vertical_spacing=0.13,
        horizontal_spacing=0.03
    )

    # Traces factices pour légende personnalisée avec regroupement
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='black'),
        name='Home advantage',
        legendgroup='lines',
        hoverinfo='skip',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='lines',
        line=dict(color='blue'),
        name='Away advantage',
        legendgroup='lines',
        hoverinfo='skip',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(color='red', size=8),
        name='Home',
        legendgroup='points',
        hoverinfo='skip',
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[None], y=[None],
        mode='markers',
        marker=dict(color='green', size=8),
        name='Away',
        legendgroup='points',
        hoverinfo='skip',
        showlegend=True
    ))

    metrics = [
        ('Athletes', 'Number of Athletes'),
        ('Medals', 'Number of Medals'),
        ('Ratio', 'Number of Medals per Athlete')
    ]
    periods = ['1945-1991', '1992-2020']
    n_rows = len(metrics)

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

                delta = 0.001 if metric == "Ratio" else 1
                if abs(host - away) < delta:
                    away -= 2 * delta
                    host += 2 * delta

                away = float(away) if away is not None else 0
                host = float(host) if host is not None else 0

                fig.add_trace(go.Scatter(
                    x=[away, host],
                    y=[y_idx, y_idx],
                    mode='lines',
                    line=dict(color=color),
                    hoverinfo='skip',
                    showlegend=False
                ), row=row, col=col)

                fig.add_trace(go.Scatter(
                    x=[away],
                    y=[y_idx],
                    mode='markers',
                    marker=dict(color='green', size=8),
                    customdata=[[country]],
                    hovertemplate=hover_template.get_hover_template(label_name, is_host=False),
                    showlegend=False
                ), row=row, col=col)

                fig.add_trace(go.Scatter(
                    x=[host],
                    y=[y_idx],
                    mode='markers',
                    marker=dict(color='red', size=8),
                    customdata=[[country, host_years_str]],
                    hovertemplate=hover_template.get_hover_template(label_name, is_host=True),
                    showlegend=False
                ), row=row, col=col)

            fig.update_yaxes(
                tickvals=list(range(len(y_labels))),
                ticktext=y_labels,
                side="right" if col == 2 else "left",
                row=row,
                col=col
            )

    title_annotations = [
        dict(
            text=f"<b>{label}</b>",
            x=0.5,
            y=1 - (i*1.18 / n_rows) + 0.04,
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=20, family="Roboto Slab"),
            xanchor="center"
        )
        for i, (key, label) in enumerate(metrics)
    ]

    h_spacing = 0.03
    x_left = h_spacing / 2
    x_mid = 0.5
    x_right = 1 - h_spacing / 2

    row_height = 1 / n_rows
    shapes = []

    shapes += [
        dict(
            type='line',
            x0=0.5, x1=0.5,
            y0=0, y1=1,
            xref='paper', yref='paper',
            line=dict(color='lightgray', width=2, dash='dot')
        ),
        dict(
            type='line',
            x0=x_left, x1=x_mid - h_spacing / 2,
            y0=1.08, y1=1.08,
            xref='paper', yref='paper',
            line=dict(color='gray', width=1.5)
        ),
        dict(
            type='line',
            x0=x_mid + h_spacing / 2, x1=x_right,
            y0=1.08, y1=1.08,
            xref='paper', yref='paper',
            line=dict(color='gray', width=1.5)
        )
    ]

    fig.update_layout(
        font=dict(family="Inter"),
        height=950,
        font_size=14,  # Définir la taille du texte à 14)
        margin=dict(t=top_margin),
        annotations=title_annotations + [
            dict(
                text="1945–1991",
                x=(x_left + x_mid) / 2,
                y=1.14,
                xref="paper", yref="paper",
                xanchor="center",
                showarrow=False,
                font=dict(size=16, family="Roboto Slab", color="gray")
            ),
            dict(
                text="1992–2020",
                x=(x_mid + x_right) / 2,
                y=1.14,
                xref="paper", yref="paper",
                xanchor="center",
                showarrow=False,
                font=dict(size=16, family="Roboto Slab", color="gray")
            )
        ],
        shapes=shapes,
        legend=dict(
            title=dict(text="Legend"),
            orientation="v",
            yanchor="top",
            y=1.33,
            xanchor="left",
            x=0,
            tracegroupgap=10
        )
    )

    return fig
    