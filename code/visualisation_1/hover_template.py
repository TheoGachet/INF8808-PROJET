def get_hover_template(sport):
    template = (f"<b style='font-family:Inter;'>{sport}</b>" + 
                "<br><b style='font-family:Inter;'>Country:</b> %{y}" + 
                "<br><b style='font-family:Inter;'>Year:</b> %{x}" + 
                "<br><b style='font-family:Inter;'>Medals:</b> %{z}<extra></extra>")
    # Retourne le modèle de survol formaté pour afficher les informations sur le sport, le pays, l'année et les médailles
    return template