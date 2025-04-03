# preprocess.py
import pandas as pd
import os

def load_csv(filename):
    """
    Charge un fichier CSV depuis le dossier 'data'.
    """
    path = os.path.join("data", filename)
    return pd.read_csv(path)
