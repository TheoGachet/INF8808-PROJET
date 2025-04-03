import dash
from dash import html
from visualisation_1.app import get_figure_html

app = dash.Dash(__name__)
app.title = "Projet INF8808"

app.layout = html.Div([
    html.Main([
        html.Div([
            html.Div([
                html.H1(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
                    className="section-title"
                ),
                html.P(
                    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, " \
                    "sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. " \
                    "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat",
                    className="section-title"
                )
                ],
                className="section-column start p-40"    
            ),
            html.Div([
                html.H1(
                    "IMAGE",
                    className="section-title"
                )
                ],
                className="section-column center"    
            ),
            ], 
            className="section-row"
        ),
        get_figure_html()
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)
