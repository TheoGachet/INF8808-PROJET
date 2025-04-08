'''
    Provides the template for the tooltips.
'''


def get_bubble_hover_template():
    '''
        Sets the template for the hover tooltips.
        
        Contains four labels, followed by their corresponding
        value and units where appropriate, separated by a
        colon : country, population, GDP and CO2 emissions.

        The labels' font is bold and the values are normal weight

        returns:
            The content of the tooltip
    '''
    # TODO : Generate tooltip
    hover_template = (
        "<span style='font-family:Inter;'><b>Country: </b> %{customdata[0]}<br>"
        "<b>Continent: </b> %{customdata[2]}<br>"
        "<b>Climate: </b> %{customdata[3]}<br>"
        "<b>Average Population: </b> %{customdata[1]:,}<br>"
        "<b>GDP per Capita: </b> %{x:,} $ (USD)<br>"
        "<b>Medals per Olympic Games: </b> %{y:,}</span><extra></extra>"
    )
    return hover_template