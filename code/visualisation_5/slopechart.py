import plotly.express as px

import visualisation_5.preprocess as preprocess
import visualisation_5.hover_template as hover_template

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
                title=str(full_pays + " points with and without multi-medalists athletes"),
                hover_data={"Year": True, "Type" : True}
                )

    fig.update_layout(
        height = 700,
        font=dict(family="Inter"),  # Définir la police "Inter"
        font_size=14,  # Définir la taille du texte à 14)
        margin=dict(l=600, r=600, t=100, b=0),
        plot_bgcolor = 'lightgrey', 

        xaxis=dict(type='category'),
        xaxis_showgrid=False,  
        yaxis_showgrid=False,
        xaxis_title="",

        yaxis2=dict(
            title="Secondary Axis",
            overlaying="y",
            side="right",
            showgrid=False
        ),

        legend=dict(
            x=1.5,
            y=0.5,
            xanchor="center",
            yanchor="bottom"
            ),

        title=dict(text=fig.layout.title.text, x=0.5),
        )
    
    fig.update_xaxes(tickmode="array",
                 tickvals=["With", "Without"], 
                 ticktext=["With multi medalists", "Without multi medalists"] 
                )

    for trace in fig.data:
        trace.hovertemplate = hover_template.get_hovertemplate(pays)
    
    # fig.data[0].line.color = "red"

    fig.update_traces(line=dict(width=2))

    fig.update_layout()
    
    return fig
