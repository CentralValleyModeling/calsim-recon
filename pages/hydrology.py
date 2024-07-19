import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dcc, html, register_page

from charts.chart_layouts import CardWidget, card_bar_plot_cy, card_mon_plot
from data import load_markdown, universal_data_download
from utils.query_data import df_sv

register_page(
    __name__,
    name="Hydrology",
    top_nav=True,
    path="/hydrology",
    order=1,
)

# Cards

eight_ri_card_ann = CardWidget(
    "Eight River Index",
    button_id=None,
    button_label=None,
    chart=card_bar_plot_cy(df_sv, b_part="8RI"),
    text="",
)

sac_four_ri_card_ann = CardWidget(
    "Sacramento River Runoff",
    button_id=None,
    button_label=None,
    chart=card_bar_plot_cy(df_sv, b_part="SAC4"),
    text="",
)

sjr_four_ri_card_ann = CardWidget(
    "San Joaquin River Runoff",
    button_id=None,
    button_label=None,
    chart=card_bar_plot_cy(df_sv, b_part="SJR4"),
    text="",
)

orov_inflow_card_ann = CardWidget(
    "Oroville Reservoir Inflow",
    button_id=None,
    button_label=None,
    chart=card_bar_plot_cy(df_sv, b_part="OROVI"),
    text="",
)

eight_ri_card_mon = CardWidget(
    "Eight River Index",
    button_id=None,
    button_label=None,
    chart=card_mon_plot(df_sv, b_part="8RI", yaxis_title="Eight River Index (TAF)"),
    text=load_markdown("page_text/hydrology-8ri.md"),
)

sac_four_ri_card_mon = CardWidget(
    "Sacramento River Runoff",
    button_id=None,
    button_label=None,
    chart=card_mon_plot(
        df_sv, b_part="SAC4", yaxis_title="Sacramento River Runoff (TAF)"
    ),
    text=load_markdown("page_text/hydrology-sacramento-4ri.md"),
)

sjr_four_ri_card_mon = CardWidget(
    "San Joaquin River Runoff",
    button_id=None,
    button_label=None,
    chart=card_mon_plot(
        df_sv, b_part="SJR4", yaxis_title="San Joaquin River Runoff (TAF)"
    ),
    text=load_markdown("page_text/hydrology-san-joaquin-4ri.md"),
)

orov_inflow_card_mon = CardWidget(
    "Oroville Reservoir Inflow - All Years",
    button_id=None,
    button_label=None,
    chart=card_mon_plot(
        df_sv,
        b_part="OROVI",
        wyt=[1, 2, 3, 4, 5],
        yaxis_title="Oroville Reservoir Inflow (TAF)",
    ),
    text="""All Years (Sacramento Valley Index)""",
)

orov_inflow_card_drier_mon = CardWidget(
    "Oroville Reservoir Inflow - Drier Years",
    button_id=None,
    button_label=None,
    chart=card_mon_plot(
        df_sv, b_part="OROVI", wyt=[4, 5], yaxis_title="Oroville Reservoir Inflow (TAF)"
    ),
    text="""Dry and Critical years (Sacramento Valley Index)""",
)

orov_inflow_card_wetter_mon = CardWidget(
    "Oroville Reservoir Inflow - Wetter Years",
    button_id=None,
    button_label=None,
    chart=card_mon_plot(
        df_sv, b_part="OROVI", wyt=[1, 2], yaxis_title="Oroville Reservoir Inflow (TAF)"
    ),
    text="""Wet and Above Normal years (Sacramento Valley Index)""",
)


def layout():
    layout = dbc.Container(
        class_name="m-2",
        children=[
            dcc.Download(id="download-response-hydrology"),
            dbc.Col(
                [
                    html.H3(["Hydrology Comparison"]),
                    dbc.Row(
                        [
                            dbc.Col(eight_ri_card_ann.create_card(height="25rem")),
                            dbc.Col(sac_four_ri_card_ann.create_card(height="25rem")),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(sjr_four_ri_card_ann.create_card(height="25rem")),
                            dbc.Col(orov_inflow_card_ann.create_card(height="25rem")),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                eight_ri_card_mon.create_card(
                                    registry_id="monthly-8RI",
                                )
                            ),
                            dbc.Col(
                                sac_four_ri_card_mon.create_card(
                                    registry_id="monthly-sacramento-4RI",
                                )
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                sjr_four_ri_card_mon.create_card(
                                    registry_id="monthly-san-joaquin-4RI",
                                )
                            ),
                            dbc.Col(
                                orov_inflow_card_mon.create_card(
                                    registry_id="monthly-oroville-inflow",
                                )
                            ),
                        ]
                    ),
                    dbc.Row(
                        [
                            dbc.Col(
                                orov_inflow_card_drier_mon.create_card(
                                    registry_id="monthly-oroville-inflow-dry",
                                )
                            ),
                            dbc.Col(
                                orov_inflow_card_wetter_mon.create_card(
                                    registry_id="monthly-oroville-inflow-wet",
                                )
                            ),
                        ]
                    ),
                ],
            ),
        ],
    )
    return layout


# Callbacks
@callback(
    Output("download-response-hydrology", "data"),
    Input("monthly-8RI", "n_clicks"),
    Input("monthly-sacramento-4RI", "n_clicks"),
    Input("monthly-san-joaquin-4RI", "n_clicks"),
    Input("monthly-oroville-inflow", "n_clicks"),
    Input("monthly-oroville-inflow-dry", "n_clicks"),
    Input("monthly-oroville-inflow-wet", "n_clicks"),
    prevent_initial_call=True,
)
def home_data_download(*args):
    return universal_data_download()
