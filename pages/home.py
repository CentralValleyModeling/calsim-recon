from urllib.parse import urlencode

import dash_bootstrap_components as dbc
import pandas as pd
from dash import (
    ALL,
    Input,
    Output,
    callback,
    callback_context,
    dcc,
    html,
    no_update,
    register_page,
)
from plotly.graph_objects import Figure

from charts.chart_layouts import CardWidget, card_bar_plot_cy, card_mon_exc_plot
from data import CHART_REGISTRY, load_markdown
from utils.query_data import df_dv

register_page(__name__, name="Home", top_nav=True, path="/")

dcr_cover_path = "assets/final_dcr_2023_cover.png"


ta_card = CardWidget(
    "Total SWP Table A and Carryover Deliveries",
    button_id="table_a_btn",
    button_label="View by Contractor",
    button_id2="ta_wet_dry",
    button_label2="Wet and Dry Periods",
    chart=card_bar_plot_cy(
        df_dv,
        b_part="SWP_TA_CO_SOD",
        wyt=[1, 2, 3, 4, 5],
        startyr=1922,
        endyr=2021,
    ),
    text=load_markdown("page_text/card-table-a.md"),
)
a21_card = CardWidget(
    "SWP Article 21 Deliveries",
    button_id="a21_btn",
    button_label="View by Contractor",
    chart=card_bar_plot_cy(df_dv, b_part="SWP_IN_TOTAL"),
    text=load_markdown("page_text/card-article-21.md"),
)
a56_card = CardWidget(
    "SWP Carryover Deliveries",
    button_id="a56_btn",
    button_label="View by Contractor",
    chart=card_bar_plot_cy(df_dv, b_part="SWP_CO_SOD"),
    text=load_markdown("page_text/card-carryover.md"),
)
exp_card = CardWidget(
    "Total Banks SWP Exports",
    button_id="C_CAA003_SWP",
    button_label="Details",
    chart=card_bar_plot_cy(df_dv, b_part="C_CAA003_SWP"),
)
orovl_sep_card = CardWidget(
    "Oroville End-of-September Storage",
    button_id="S_OROVL",
    button_label="Details",
    chart=card_mon_exc_plot(df_dv, b_part="S_OROVL", monthchecklist=["Sep"]),
)
orovl_may_card = CardWidget(
    "Oroville End-of-May Storage",
    button_id="S_OROVL",
    button_label="Details",
    chart=card_mon_exc_plot(df_dv, b_part="S_OROVL", monthchecklist=["May"]),
)
sluis_card = CardWidget(
    "San Luis SWP End-of-September Storage",
    button_id="S_SLUIS_SWP",
    button_label="Details",
    chart=card_mon_exc_plot(df_dv, b_part="S_SLUIS_SWP", monthchecklist=["Sep"]),
)
swp_alloc_card = CardWidget(
    "SWP May Allocation",
    button_id=None,
    button_label=None,
    chart=card_mon_exc_plot(df_dv, b_part="PERDV_SWP_MWD1", monthchecklist=["May"]),
)

add_resources_card = dbc.Card(
    [
        dbc.CardBody(
            [
                html.H4("Additional Resources", className="card-title"),
                html.A(
                    "The DCR Report and Models",
                    href="https://water.ca.gov/Library/Modeling-and-Analysis/"
                    + "Central-Valley-models-and-tools/CalSim-3/DCR",
                    target="_blank",
                    style={"marginTop": "10px"},
                ),
                html.Br(),
                html.Br(),
                html.A(
                    "Central Valley Modeling GitHub",
                    href="https://github.com/CentralValleyModeling",
                    target="_blank",
                    style={"marginTop": "10px"},
                ),
                html.Br(),
                html.Br(),
                html.A(
                    "Climate Adjusted Historical Documentation",
                    href="https://data.cnra.ca.gov/dataset/"
                    + "state-water-project-delivery-capability-report-dcr-2023/"
                    + "resource/ad861b0b-c0aa-4578-8af0-54485e751ca8",
                    target="_blank",
                    style={"marginTop": "10px"},
                ),
                html.Br(),
                html.Br(),
                html.A(
                    "Risk-Informed Future Climate Scenario Documentation",
                    href="https://data.cnra.ca.gov/dataset/"
                    + "state-water-project-delivery-capability-report-dcr-2023/"
                    + "resource/dffe00a6-017c-4765-affe-36b045c24969",
                    target="_blank",
                    style={"marginTop": "10px"},
                ),
                html.Br(),
            ]
        ),
    ],
    style={
        # "height": "400px",
        # "width": "400px",
        "backgroundColor": "#f8f9fa",
        "border": "0",
    },
)


def layout():
    layout = dbc.Container(
        id="home-container",
        class_name="my-3",
        children=[
            dbc.Row(
                id="home-introduction",
                children=[
                    dbc.Col(
                        id="dcr-cover-image",
                        class_name="col-md-3 d-none d-lg-block my-1",  # Image goes away
                        children=[
                            html.Img(src=dcr_cover_path, className="img-fluid"),
                        ],
                    ),
                    dbc.Col(
                        id="home-introduction-text",
                        class_name="col-md-6 my-1",
                        children=[load_markdown("page_text/site-introduction.md")],
                    ),
                    dbc.Col(
                        id="home-introduction-links",
                        class_name="col-md",
                        children=[
                            add_resources_card,
                        ],
                    ),
                ],
                # style={"background-color": "#FFFFFF"},
            ),
            html.Hr(),
            dbc.Col(
                id="home-cards",
                className="d-grid gap-2",
                children=[
                    dbc.Row(
                        id="home-cards-row-0",
                        children=[
                            dbc.Col(
                                class_name="col-md-6", children=[ta_card.create_card()]
                            ),
                            dbc.Col(
                                class_name="col-md-6", children=[a21_card.create_card()]
                            ),
                        ],
                    ),
                    dbc.Row(
                        id="home-cards-row-1",
                        children=[
                            dbc.Col(
                                class_name="col-md-6",
                                children=[a56_card.create_card()],
                            ),
                            dbc.Col(
                                class_name="col-md-6",
                                children=[exp_card.create_card()],
                            ),
                        ],
                    ),
                    dbc.Row(
                        id="home-cards-row-2",
                        children=[
                            dbc.Col(
                                class_name="col-md-6",
                                children=[
                                    orovl_sep_card.create_card(
                                        register_download="oroville-sept-exceedance",
                                    )
                                ],
                            ),
                            dbc.Col(
                                class_name="col-md-6",
                                children=[
                                    orovl_may_card.create_card(
                                        register_download="oroville-may-exceedance",
                                    )
                                ],
                            ),
                        ],
                    ),
                    dbc.Row(
                        id="home-cards-row-3",
                        children=[
                            dbc.Col(
                                class_name="col-md-6",
                                children=[
                                    sluis_card.create_card(
                                        register_download="sluis-exceedance",
                                    )
                                ],
                            ),
                            dbc.Col(
                                class_name="col-md-6",
                                children=[
                                    swp_alloc_card.create_card(
                                        register_download="swp-alloc-exceedance"
                                    )
                                ],
                            ),
                        ],
                    ),
                ],
                # style={"background-color": "#FFFFFF"},
            ),
            html.Div(
                id="output-div",
                children=[
                    dcc.Download(id="download-response"),
                ],
            ),
        ],
    )
    return layout


# Define the generalized callback for the first button in the card
@callback(
    Output("url", "href"),
    Output("url", "refresh"),
    Input({"type": "dynamic-btn", "index": ALL}, "n_clicks"),
)
def button_1_action(n_clicks):
    ctx = callback_context
    if not ctx.triggered or all(click is None for click in n_clicks):
        return "/", False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        button_index = eval(button_id)["index"]
        url_params = urlencode({"type": button_index})

        print(button_index)

        if button_index == "ta_wet_dry":
            return "/dry_wet_periods", True

        if button_index in ("C_CAA003_SWP", "S_OROVL", "S_SLUIS_SWP"):
            return f"/drilldown?{url_params}", True
        else:
            return f"/contractor_summary?{url_params}", True


def find_figure_in_div(obj: html.Div) -> Figure | None:
    for o in obj.children:
        if isinstance(o, Figure):
            return o
        elif isinstance(o, dcc.Graph):
            return o.figure
        elif hasattr(o, "children"):
            fig = find_figure_in_div(o)
            if fig is not None:
                return fig
    return None  # Nothing found


def create_dataframe_from_fig(fig: Figure) -> pd.DataFrame:
    frames = list()
    for data in fig.data:
        if data["mode"] == "lines":
            df = pd.DataFrame(
                data={data["name"]: data["y"], "X": data["x"]},
            )
            df = df.set_index("X")
            frames.append(df)
        else:
            raise NotImplementedError(
                f"figure trace mode not supported: {data['mode']}"
            )
    return pd.concat(frames, axis=1, join="outer").sort_index()


@callback(
    Output("download-response", "data"),
    Input("oroville-sept-exceedance", "n_clicks"),
    Input("oroville-may-exceedance", "n_clicks"),
    Input("sluis-exceedance", "n_clicks"),
    Input("swp-alloc-exceedance", "n_clicks"),
    prevent_initial_call=True,
)
def universal_data_download(*args):
    _id = callback_context.triggered_id
    if _id not in CHART_REGISTRY:
        print(f"Button(id={_id}) is not registered in the CHART_REGISTRY")
        return no_update
    div = CHART_REGISTRY[_id]()
    fig = find_figure_in_div(div)
    if fig is None:
        print(f"Could not find a Figure in Div for Button(id={_id})")
        return no_update
    df = create_dataframe_from_fig(fig)
    return dcc.send_data_frame(df.to_csv, f"{_id}.csv")
