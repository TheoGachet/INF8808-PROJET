import plotly.express as px

import preprocess
import hover_template

pays_disponibles = preprocess.pays_dispo


def viz_5(df, pays, season):
    ## Preprocess:
    df_years = preprocess.rejet_annees(df, 1991, ete=(season == "ete"))
    years = sorted(df_years["Year"].unique())
    df_points = preprocess.points(df_years)
    df_without = preprocess.data_without(df_points)
    df_final = preprocess.pays_points(df_points, df_without)
    usefull_df = preprocess.get_usefull_dataframe(df_final, pays, years)

    _, full_pays = preprocess.is_value_in_tuples(pays, pays_disponibles)

    ## Figure:
    fig = px.line(usefull_df, x="Type", y="Points", color="Year",
                color_discrete_sequence=px.colors.sequential.Blues[1:],
                markers=True,
                title=str("Nombre de points de " + full_pays + " avec et sans leurs athlètes multi-médaillés"),
                hover_data={"Year": True, "Type" : True}
                )

    fig.update_layout(
        xaxis_title="",
        yaxis_title="Nombre de points",
        )
    
    fig.update_xaxes(tickmode="array",
                 tickvals=["With", "Without"], 
                 ticktext=["Avec les multi-médaillés", "Sans les multi-médaillés"] 
                )

    for trace in fig.data:
        trace.hovertemplate = hover_template.get_hovertemplate(pays)

    fig.update_traces(line=dict(width=2))

    fig.update_layout(xaxis=dict(type='category'),
                    width=700, height=700,  
                    xaxis_showgrid=False,  
                    yaxis_showgrid=False,
                    plot_bgcolor = 'lightgrey')
    
    return fig
