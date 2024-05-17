from dash import html
import dash_bootstrap_components as dbc


def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(
                dbc.NavLink(
                    [
                        html.I(className="fa-brands fa-github"),  # Font Awesome Icon
                        " "  # Text beside icon
                    ],
                    href="https://github.com/CentralValleyModeling",
                    target="_blank"
                )

            ),
            dbc.DropdownMenu(
                nav=True,
                in_navbar=True,
                label="Menu",
                align_end=True,
                children=[  # Add as many menu items as you need
                    dbc.DropdownMenuItem("Home", href='/'),
                    dbc.DropdownMenuItem(divider=True),
                    dbc.DropdownMenuItem("Study Selection", href='/study_selection'),
                    dbc.DropdownMenuItem("Heatmap", href='/heatmap'),
                    dbc.DropdownMenuItem("Summary", href='/summary'),
                    dbc.DropdownMenuItem("Drilldown", href='/drilldown'),
                    dbc.DropdownMenuItem("One Pager", href='/onepager'),
                ],
            ),
        ],
        brand='Home',
        brand_href="/",
        # sticky="top",  # Uncomment if you want the navbar to always appear at the top on scroll.
        color="dark",  # Change this to change color of the navbar e.g. "primary", "secondary" etc.
        dark=True,  # Change this to change color of text within the navbar (False for dark text)
    )

    return navbar