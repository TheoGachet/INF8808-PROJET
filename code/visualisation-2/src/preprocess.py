"""
    use the "get_data()" function to 
"""

from pathlib import Path
import os
import pandas as pd
import csv

DATA_FOLDER = Path(os.path.abspath(__file__)).parent.parent.parent.parent / "data"
PATH_ATHLETE_GAMES = DATA_FOLDER / "all_athlete_games.csv"
PATH_REGIONS = DATA_FOLDER / "all_regions.csv"
PATH_PIB_PER_CAPITA = DATA_FOLDER / "WEO_database_Apre2024.csv" # data from this website: https://www.imf.org/en/Publications/WEO/weo-database/2024/April/download-entire-database
PATH_COUNTRIES_PER_CONTINENT = DATA_FOLDER / "WEO_database_Apre2024.csv" # data from this website: https://worldpopulationreview.com/country-rankings/list-of-countries-by-continent

def get_df(path: Path) -> pd.DataFrame:
    with open(path) as data_file:
        data = list(csv.reader(data_file))
    df = pd.DataFrame(data[1:], columns=data[0])

def get_athlete_games() -> pd.DataFrame:
    return get_df(PATH_ATHLETE_GAMES)

def get_regions() -> pd.DataFrame:
    return get_df(PATH_REGIONS)







def round_decimals(my_df):
    '''
        Rounds all the numbers in the dataframe to two decimal points

        args:
            my_df: The dataframe to preprocess
        returns:
            The dataframe with rounded numbers
    '''
    # TODO : Round the dataframe
    my_df["GDP"] = my_df["GDP"].round(2)
    my_df["CO2"] = my_df["CO2"].round(2)
    return my_df


def get_range(col, df1, df2):
    '''
        An array containing the minimum and maximum values for the given
        column in the two dataframes.

        args:
            col: The name of the column for which we want the range
            df1: The first dataframe containing a column with the given name
            df2: The first dataframe containing a column with the given name
        returns:
            The minimum and maximum values across the two dataframes
    '''
    # TODO : Get the range from the dataframes
    min_value = min(df1[col].min(), df2[col].min())
    max_value = max(df1[col].max(), df2[col].max())
    return [min_value, max_value]


def combine_dfs(df1, df2):
    '''
        Combines the two dataframes, adding a column 'Year' with the
        value 2000 for the rows from the first dataframe and the value
        2015 for the rows from the second dataframe

        args:
            df1: The first dataframe to combine
            df2: The second dataframe, to be appended to the first
        returns:
            The dataframe containing both dataframes provided as arg.
            Each row of the resulting dataframe has a column 'Year'
            containing the value 2000 or 2015, depending on its
            original dataframe.
    '''
    # TODO : Combine the two dataframes
    df1["Year"] = 2000
    df2["Year"] = 2015
    return pd.concat([df1, df2], ignore_index=True)


def sort_dy_by_yr_continent(my_df):
    '''
        Sorts the dataframe by year and then by continent.

        args:
            my_df: The dataframe to sort
        returns:
            The sorted dataframe.
    '''
    # TODO : Sort the dataframe
    return my_df.sort_values(["Year", "Continent"])
