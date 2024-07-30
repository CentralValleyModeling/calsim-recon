from collections import namedtuple

import dash_bootstrap_components as dbc
import pandas as pd
import yaml
from dash import Input, Output, callback, dash_table, dcc, html, register_page

# register_page(
#    __name__,
#    #name='Page 2',
#    top_nav=True,
#    path='/study_selection'
# )
scen_dict = (
    {}
)  # Global variable to store scenario pathnames and aliases, as entered by user


def layout():
    layout = dbc.Container(
        class_name="my-3",
        children=[
            dcc.Markdown(
                "# ![](/assets/cs3_icon_draft.png) CalSim 3 Dashboard - Study Selection"
            ),
            dbc.Row(
                [
                    html.Hr(),
                    dcc.Markdown("## Upload Studies to Temporary Database"),
                    dbc.Col(
                        [
                            #                    du.Upload(
                            #                        id='dash-uploader',
                            #                        max_files=30,
                            #                        filetypes=['dss'],
                            #                    ),
                            dash_table.DataTable(
                                id="file-table",
                                columns=[
                                    # {'name': 'Path', 'id': 'pathname'},
                                    {"name": "Filename", "id": "filename"},
                                    {"name": "Alias", "id": "alias", "editable": True},
                                ],
                                data=[],
                                editable=True,
                            ),
                            html.Button(
                                "Refresh Table", id="populate-table", n_clicks=0
                            ),
                            html.Button(
                                "Clear List",
                                id="clear-button",
                                style={"margin-top": "10px"},
                            ),  # Button to clear the list
                            dbc.Row(
                                [
                                    dcc.Input("temp.csv", id="csv-name"),
                                    html.Button(
                                        "Load Studies into CSV",
                                        id="load-studies",
                                        n_clicks=0,
                                    ),
                                ]
                            ),
                            html.Div("", id="dummy-div1"),
                            html.Div(id="table-update-output"),
                            html.Div(id="output-data-upload"),
                        ],
                        width=6,
                    ),
                    dbc.Row(
                        [
                            html.Hr(),
                            dcc.Markdown("## Retrieve Existing CSV Database"),
                        ]
                    ),
                ]
            ),
        ],
    )
    return layout
