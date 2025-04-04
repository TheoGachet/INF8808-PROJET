def get_hover_template(sport):
    template = f"<b>{sport}</b>" + "<br>Pays: %{y}" + "<br>Année: %{x}" + "<br>Médailles: %{z}<extra></extra>"
    # Retourne le modèle de survol formaté pour afficher les informations sur le sport, le pays, l'année et les médailles
    return template