# INF8808 - Projet de session

## Description

Ce projet vise à explorer et analyser les performances des pays aux Jeux Olympiques d'été et d'hiver, à travers diverses visualisations interactives.  
Chaque visualisation met en lumière un aspect différent des données olympiques : répartition géographique, évolution temporelle, focus par discipline, etc.  
L'application finale regroupe toutes les visualisations dans une interface unique, en utilisant Python, Dash, Plotly et Pandas.

## Structure du projet

Le projet est organisé en plusieurs dossiers :

- **`data/`** : Contient toutes les données CSV utilisées pour les visualisations, ainsi que quelques scripts de traitement intermédiaire (`data_athletes.py`, `data_pays.py`, etc.).
- **`docs/`** : Regroupe le plan du projet, des exemples fournis par le cours, ainsi que des documents d'inspiration pour la réalisation des visualisations.
- **`project/`** : Cœur du projet contenant l'ensemble du code source.
  - **`visualisation_1/`** à **`visualisation_5/`** : Chaque sous-dossier correspond à une visualisation indépendante, avec son propre prétraitement, ses propres graphiques et ses propres templates Dash.
- **`assets/`** : Contient les ressources statiques partagées, notamment les fichiers CSS (`styles.css`) et les images (`home_image.png`).
- **Fichiers racine** :
  - **`app.py`** et **`server.py`** : Point d'entrée principal pour lancer l'application globale.
  - **`Procfile`** : Fichier nécessaire pour le déploiement sur des plateformes comme Heroku.
  - **`requirements.txt`** : Liste des dépendances Python nécessaires au bon fonctionnement du projet.

## Lancement de l'application

Pour exécuter l'application en local :

1. Cloner le dépôt :
   ```bash
   git clone <url_du_repo>
   cd INF8808-PROJET-main
   ```

2. Créer un environnement virtuel et installer les dépendances :
   ```bash
   python -m venv venv
   source venv/bin/activate  # (ou `venv\Scripts\activate` sous Windows)
   pip install -r requirements.txt
   ```

3. Lancer l'application :
   ```bash
   python app.py
   ```

L'application est également disponible sur `https://olympic-games-team16-ce8602bed91e.herokuapp.com/#viz4-section` dans votre navigateur.

## Technologies utilisées

- Python 3.10+
- Dash
- Plotly
- Pandas
- Circlify
- Gunicorn (pour déploiement)

## Notes complémentaires

- Les données sont filtrées pour ne considérer que les Jeux Olympiques depuis 1992.
- Les visualisations utilisent différentes techniques : cartes interactives, diagrammes en bulles proportionnelles, slope charts, lolipop charts, etc.
- Le projet respecte une séparation claire entre le prétraitement des données, la création des figures et le layout des pages.
- Chaque visualisation a été développée de manière modulaire pour faciliter l'intégration finale.