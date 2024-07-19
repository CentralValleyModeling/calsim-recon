import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

FA621 = "https://use.fontawesome.com/releases/v6.2.1/css/all.css"
APP_TITLE = "SWP Delivery Capability Report 2023 Results Console (ReCon)"
CS3_ICON = "assets/cs3_icon_draft.png"


class ReconNavbarBrand(dbc.NavbarBrand):
    def __init__(self, label: str, **kwargs):
        img = html.Img(
            src=str(CS3_ICON),
            height="30px",
        )
        label = dbc.NavbarBrand(label, className="m-0")
        children = dbc.Row(
            [
                dbc.Col(img),
                dbc.Col(label),
            ],
            align="center",
            className="g-2",
        )
        # Update kwargs
        kwargs = {
            "href": "/",
            "children": children,
            "style": {
                "textDecoration": "none",
                "margin": "0",
            },
        } | kwargs
        super().__init__(**kwargs)


app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[
        dbc.themes.SPACELAB,  # Dash Themes CSS
        FA621,  # Font Awesome Icons CSS
    ],
    title=APP_TITLE,
    use_pages=True,
)

pages = [
    dbc.NavItem(dbc.NavLink(page["name"], href=page["relative_path"]))
    for page in dash.page_registry.values()
]

navbar = dbc.NavbarSimple(
    brand=ReconNavbarBrand("SWP DCR 2023 Recon"),
    children=pages,
    color="light",
    dark=False,
    className="mb-0",
)


app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        navbar,
        dash.page_container,
    ],
)

server = app.server

if __name__ == "__main__":
    app.run_server(debug=True)
