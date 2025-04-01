'''
    Provides the templates for the tooltips in the lollipop charts.
'''

def get_host_years_by_country(season):
    # Summer Olympics
    summer_map = {
        '1945-1991': {
            "United Kingdom": [1948],
            "Finland": [1952],
            "Australia": [1956],
            "Italy": [1960],
            "Japan": [1964],
            "Mexico": [1968],
            "Germany": [1972],
            "Canada": [1976],
            "Russia": [1980],
            "United States": [1984],
            "South Korea": [1988]
        },
        '1992-2020': {
            "Spain": [1992],
            "United States": [1996],
            "Australia": [2000],
            "Greece": [2004],
            "China": [2008],
            "United Kingdom": [2012],
            "Brazil": [2016],
            "Japan": [2020]
        }
    }

    # Winter Olympics
    winter_map = {
        '1945-1991': {
            "Switzerland": [1948],
            "Norway": [1952],
            "Italy": [1956],
            "United States": [1960, 1980],
            "Austria": [1964, 1976],
            "France": [1968],
            "Japan": [1972],
            "Bosnia and Herzegovina": [1984],
            "Canada": [1988]
        },
        '1992-2020': {
            "France": [1992],
            "Norway": [1994],
            "Japan": [1998],
            "United States": [2002],
            "Italy": [2006],
            "Canada": [2010],
            "Russia": [2014],
            "South Korea": [2018]
        }
    }

    return summer_map if season == "Summer" else winter_map


def get_hover_template(metric_label, is_host):
    """
    Returns a hover template string for host or away points.

    Args:
        metric_label (str): Label of the metric (e.g., 'athletes', 'medals')
        is_host (bool): True if the point is for a host value, False for away

    Returns:
        str: A valid Plotly hovertemplate
    """
    if is_host:
        template = (
            "<span style='font-family:Roboto Slab'><extra></extra><br>"
            "<b>Country</b>: %{customdata[0]}<br>"
            "<b>" + metric_label.capitalize() + "</b>: %{x}<br>"
            "<b>Home editions</b>: %{customdata[1]}"
        )
    else:
        template = (
            "<span style='font-family:Roboto Slab'><extra></extra><br>"
            "<b>Country</b>: %{customdata[0]}<br>"
            "<b>" + metric_label.capitalize() + "</b>: %{x}<br>"
        )
    return template
