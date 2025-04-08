'''
    This file contains the code for the bubble plot.
'''

import plotly.express as px
import math

import visualisation_2.src.hover_template as hover_template


def get_plot(df, graph_id: int = 1):
    '''
        Generates the bubble plot.

        The x and y axes are log scaled, and there is
        an animation between the data for years 2000 and 2015.

        The discrete color scale (sequence) to use is Set1 (see : https://plotly.com/python/discrete-color/)

        The markers' maximum size is 30 and their minimum
        size is 6.

        Args:
            df: The dataframe to display
        Returns:
            The generated figure
    '''
    # TODO : Define figure with animation
    # To scale markers between the desired max and min sizes (since no min_size param exists in px.scatter)
    min, max = df['Population'].min(), df['Population'].max()
    df['marker_size'] = 3 + ((df['Population'] - min) / (max - min)) * (200 - 3)

    fig = px.scatter(
        df,
        x="PIB_per_Capita",
        y="nb_medals",
        animation_frame="Year_Group",
        size="marker_size",
        size_max=50,
        color="continent" if graph_id == 1 else "Climate",
        color_discrete_sequence=px.colors.qualitative.Set1,
        log_x=True,
        log_y=True,
        custom_data=["Region", "Population", "continent", "Climate"]
    )

    return fig


def update_animation_hover_template(fig):
    '''
        Sets the hover template of the figure,
        as well as the hover template of each
        trace of each animation frame of the figure

        Args:
            fig: The figure to update
        Returns:
            The updated figure
    '''

    # TODO : Set the hover template
    fig.update_traces(hovertemplate=hover_template.get_bubble_hover_template())

    for frame in fig.frames:
        for trace in frame.data:
            trace.hovertemplate = hover_template.get_bubble_hover_template()
    return fig


def update_animation_menu(fig, graph_id: int = 1):
    '''
        Updates the animation menu to show the current year, and to remove
        the unnecessary 'Stop' button.

        Args:
            fig: The figure containing the menu to update
        Returns
            The updated figure
    '''
    # TODO : Update animation menu

    # Retirer le menu précédent:
    fig.layout.pop("updatemenus", None)

    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "args": [None, {"frame": {"duration": 500, "redraw": True}, "fromcurrent": False, 'visible': True}],
                        "label": "Animate",
                        "method": "animate"
                    },
                ],
                "direction": "left",
                "pad": {"r": 10, "t": 87},
                "showactive": False,
                "type": "buttons",
                "x": 0.09,
                "xanchor": "right",
                "y": 0.03,
                "yanchor": "top"
            }
        ],
        sliders=[{
            "currentvalue": {
                "prefix": "Data for year: ",
            }
        }]
    )
    return fig


def update_axes_labels(fig):
    '''
        Updates the axes labels with their corresponding titles.

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # TODO : Update labels
    fig.update_xaxes(title="PIB par Capita ($ USD)")
    fig.update_yaxes(title="Médailles par jeux olympiques")
    return fig


def update_template(fig):
    '''
        Updates the layout of the figure, setting
        its template to 'simple_white'

        Args:
            fig: The figure to update
        Returns
            The updated figure
    '''
    # TODO : Update template
    fig.update_layout(template='simple_white')
    return fig


def update_legend(fig):
    '''
        Updated the legend title

        Args:
            fig: The figure to be updated
        Returns:
            The updated figure
    '''
    # TODO : Update legend
    fig.update_layout(legend_title_text="Legende")
    return fig
