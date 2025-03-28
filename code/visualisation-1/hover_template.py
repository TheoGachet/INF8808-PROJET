def get_hover_template(sport):
    template = f"<b>{sport}</b>" + "<br>Pays: %{y}" + "<br>Année: %{x}" + "<br>Médailles: %{z}<extra></extra>"
    return template