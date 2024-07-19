import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html, register_page

from charts.chart_layouts import a21_dry_wet_barplot
from data import create_download_button, universal_data_download
from utils.query_data import df_dv, scen_aliases
from utils.tools import common_pers

register_page(
    __name__,
    name="Article 21",
    top_nav=True,
    path="/a21_dry_wet_periods",
    order=3,
)
DWNLD_DRY_ID = "article-21-dry-years"
DWNLD_WET_ID = "article-21-wet-years"


def layout():
    drypers = [
        "Six Year Drought (1929-1934)",
        "Single Dry Year (1977)",
        "Two-Year Drought (1976-1977)",
        "Six Year Drought (1987-1992)",
        "Single Dry Year (2014)",
        "Two-Year Drought (2014-2015)",
    ]

    wetpers = [
        "Single Wet Year (1983)",
        "Single Wet Year (1998)",
        "Two Year Wet Sequence (1982-1983)",
        "Four Year Wet Sequence (1980-1983)",
        "Six Year Wet Sequence (1978-1983)",
        "Ten Year Wet Sequence (1978-1987)",
        "Single Wet Year (2017)",
    ]

    dry_pers = a21_dry_wet_barplot(
        df_dv,
        common_pers,
        bpart="SWP_IN_TOTAL",
        scens=scen_aliases,
        perlist=drypers,
    )

    button_download_dry = create_download_button(DWNLD_DRY_ID, dry_pers)
    wet_pers = a21_dry_wet_barplot(
        df_dv,
        common_pers,
        bpart="SWP_IN_TOTAL",
        scens=scen_aliases,
        perlist=wetpers,
    )

    button_download_wet = create_download_button(DWNLD_WET_ID, wet_pers)

    dry_div = dbc.Row(
        [
            html.H3("Article 21 Deliveries during dry periods"),
            dcc.Graph(figure=dry_pers),
            button_download_dry,
        ],
        class_name="m-3",
    )
    wet_div = dbc.Row(
        [
            html.H3("Article 21 Deliveries during wet periods"),
            dcc.Graph(figure=wet_pers),
            button_download_wet,
        ],
        class_name="m-3",
    )
    layout = dbc.Container(
        class_name="m-2",
        children=[
            dcc.Download(id="download-response-article-21"),
            dbc.Col([dry_div, wet_div]),
        ],
    )
    return layout


@callback(
    Output("download-response-article-21", "data"),
    Input(DWNLD_DRY_ID, "n_clicks"),
    Input(DWNLD_WET_ID, "n_clicks"),
    prevent_initial_call=True,
)
def home_data_download(*args):
    return universal_data_download()
