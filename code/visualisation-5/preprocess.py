import pandas as pd
import numpy as np
import os

def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    """
    path = os.path.join("data", filename)

    return pd.read_csv(path)

data = load_csv("all_athlete_games.csv")


def rejet_annee(data, annee_inf):
    """
    Rejette les lignes dont la valeur de la colonne "Year" est inférieure à `annee_inf`.
    ---
    Arguments:
        -`data`: DataFrame
        -`annee_inf`: int: Année minimale à conserver
    
    Returns:
        -`data`: DataFrame sans les lignes rejetées
    """
    data["Year"] = data["Year"].astype("Int64")

    return data[data["Year"] >= annee_inf]

def points(data):
    """
    Ajoute une colonne "Medals" et une colonne "Points" au dataframe.
    ---
    Arguments:
        -`data`: DataFrame
    
    Returns:
        -`data`: DataFrame avec les nouvelles colonnes
    """

    # Remplissage de la colonne Medals avec des 0 et 1:
    data.loc[data["Medal"].isin(["Gold", "Silver", "Bronze"]), "Medals"] = 1
    data["Medals"] = data["Medals"].fillna(0).astype(int)

    # Création de la colonne Points:
    data["Points"]=np.nan

    data.loc[data["Medal"]=="Gold", "Points"]=3
    data.loc[data["Medal"]=="Silver", "Points"]=2
    data.loc[data["Medal"]=="Bronze", "Points"]=1
    data["Points"] = data["Points"].fillna(0).astype(int)

    return data

def data_without(data):
    df_medals_count = data.groupby(["Name", "Year"])["Medals"].sum().reset_index()
    athletes_to_keep = df_medals_count[df_medals_count["Medals"] < 2]["Name"]
    data_without = data[data["Name"].isin(athletes_to_keep)]

    return data_without


def pays_points(data_with, data_without):
    """
    Retourne le nombre de points par pays et par année.
    ---
    Arguments:
        -`data`: DataFrame

    
    Returns:
        -`df_points`: DataFrame
    """
    df_points_with = data_with.groupby(['NOC','Year'])[['Points', "Medals"]].sum().reset_index()
    df_points_with.columns = ['Country','Year','Points with', "Medals with"]

    df_points_without = data_without.groupby(['NOC','Year'])[['Points', "Medals"]].sum().reset_index()
    df_points_without.columns = ['Country','Year','Points without', "Medals without"]
    
    df_merged = pd.merge(df_points_with, df_points_without, on=['Country','Year'], how='outer')

    return df_merged

def classement_pays(data, year, pays):
    """
    Retourne le classement des pays par nombre de points, lors de l'année spécifiée.
    ---
    Arguments:
        -`data`: DataFrame
    
    Returns:
        -`df_classement`: DataFrame
    """
    data = data[data['Year'] == year]
    df_classement = data.groupby(['Country'])[["Points with", "Medals with"]].sum().reset_index()
    df_classement = df_classement.sort_values(by=['Points with', "Medals with"], ascending=[False, True])
    df_classement["Rank with"] = np.arange(1, len(df_classement) + 1)


    # Modifier la case qui contient les "Points with" du pays précisé
    df_classement.loc[df_classement['Country'] == pays, 'Points with'] = data.loc[data['Country'] == pays, 'Points without'].values[0]
    df_classement.loc[df_classement['Country'] == pays, 'Medals with'] = data.loc[data['Country'] == pays, 'Medals without'].values[0]
    df_classement.sort_values(by=['Points with', "Medals with"], ascending=[False, True])
    df_classement["Rank without"] = np.arange(1, len(df_classement) + 1)

data = rejet_annee(data, 1991)
data_point_with = points(data)
data_point_without = data_without(data_point_with)

df_pays = pays_points(data_point_with, data_point_without).sort_values(by=["Year", "Points with"], ascending=False)
df_classement = classement_pays(df_pays, 2020, "FRA")
