import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html, register_page

from charts.chart_layouts import ta_dry_wet_barplot
from data import create_download_button, load_markdown, universal_data_download
from utils.query_data import df_dv, scen_aliases
from utils.tools import common_pers

register_page(
    __name__,
    name="Table A",
    top_nav=True,
    path="/dry_wet_periods",
    order=2,
)


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

dry_pers = ta_dry_wet_barplot(
    df_dv,
    common_pers,
    bpart="SWP_TA_CO_SOD",
    scens=scen_aliases,
    perlist=drypers,
)
wet_pers = ta_dry_wet_barplot(
    df_dv,
    common_pers,
    bpart="SWP_TA_CO_SOD",
    scens=scen_aliases,
    perlist=wetpers,
)

DWNLD_DRY_ID = "table-a-dry-years"
DWNLD_WET_ID = "table-a-wet-years"


def layout():
    layout = dbc.Container(
        class_name="m-2",
        children=[
            dcc.Download(id="download-response-table-a"),
            dbc.Row(
                class_name="my-2",
                children=[
                    load_markdown("page_text/table-a-dry.md"),
                    dcc.Graph(figure=dry_pers),
                    html.Div(
                        create_download_button(
                            DWNLD_DRY_ID,
                            dry_pers,
                            button_text="Download Dry Period Data",
                        )
                    ),
                ],
            ),
            dbc.Row(
                class_name="my-2",
                children=[
                    load_markdown("page_text/table-a-wet.md"),
                    dcc.Graph(figure=wet_pers),
                    html.Div(
                        create_download_button(
                            DWNLD_WET_ID,
                            wet_pers,
                            button_text="Download Wet Period Data",
                        )
                    ),
                ],
            ),
        ],
    )
    return layout


@callback(
    Output("download-response-table-a", "data"),
    Input(DWNLD_DRY_ID, "n_clicks"),
    Input(DWNLD_WET_ID, "n_clicks"),
    prevent_initial_call=True,
)
def home_data_download(*args):
    return universal_data_download()
