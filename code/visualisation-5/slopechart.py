import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash
from dash.dependencies import Input, Output

import preprocess
import hover_template

pays = "USA"

def viz_5(df, pays):
    ## Preprocess:
    df_years = preprocess.rejet_annees(df, 1991, ete=True)
    years = sorted(df_years["Year"].unique())
    df_points = preprocess.points(df_years)
    df_without = preprocess.data_without(df_points)
    df_final = preprocess.pays_points(df_points, df_without)
    usefull_df = preprocess.get_usefull_dataframe(df_final, pays, years)

    ## Figure:
    fig = px.line(usefull_df, x="Type", y="Points", color="Year",
                color_discrete_sequence=px.colors.sequential.Blues[1:],
                markers=True,
                title=str("Slopechart des points de " + pays + " avec et sans leurs athlètes multi-médaillés")
                )

    fig.update_traces(line=dict(width=2),
                    hovertemplate=hover_template.get_hovertemplate(pays))

    fig.update_layout(xaxis=dict(type='category'),  # Forcer l'axe X en catégorie
                    width=700, height=700,  
                    xaxis_showgrid=False,  
                    yaxis_showgrid=False,
                    plot_bgcolor = 'lightgrey')
    
    return fig
