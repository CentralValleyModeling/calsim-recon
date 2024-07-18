from urllib.parse import urlencode

import dash_bootstrap_components as dbc
from dash import ALL, Input, Output, callback, callback_context, html, register_page, dcc

from charts.chart_layouts import CardWidget, card_bar_plot_cy, card_mon_exc_plot
from pages.styles import GLOBAL_MARGIN
from utils.query_data import df_dv

register_page(__name__, name="Home", top_nav=True, path="/")

dcr_cover_path = "assets/final_dcr_2023_cover.png"

title_text = (
    """Welcome to the Delivery Capability Report Results Console (ReCon), an 
    interactive tool designed to complement the insights provided in the 2023 
    Delivery Capability Report. ReCon allows you to explore and visualize key 
    outputs of the DCR 2023 CalSim 3 models, providing a dynamic and engaging 
    way to understand delivery performance and capabilities.""",
    html.Br(),
    html.Br(),
    """The California Department of Water Resources released the Final State Water 
    Project Delivery Capability Report for 2023 that presents a new and enhanced 
    analysis of current and future expectations for the State Water Project water 
    supply. The report is a key tool for water managers, including groundwater 
    sustainability agencies, to help plan and manage future water supply and plan 
    for climate resilience projects""",
    html.Br(),
    html.Br(),
    """Comments and questions can be emailed to CVMsupport@water.ca.gov""",
)

tablea_text = """Excluding Butte County,Yuba City, and Plumas County FCWCD.
                Table A Water is an exhibit to the SWP's water supply contracts. The
                maximum Table A amount is the basis for apportioning water supply and
                costs to the SWP contractors. The current combined maximum Table A amount is 4,173 TAF/year. 
                Of the combined maximum Table A amount, 4,133 TAF/year is the SWP's maximum
                Table A water available for delivery from the Delta."""

a21_text = """Article 21 Water is water that SWP contractors may receive on intermittent,
            interruptible basis in addition to their Table A water, if they request it. Article
            21 water is used by many SWP contractors to help meet demands when
            allocations are less than 100 percent. The availability and delivery of Article
            21 water cannot impact the Table A allocation of the any contractor's water,
            nor can it negatively impact normal SWP operations."""

co_text = """Excluding Butte County,Yuba City, and Plumas County FCWCD.
           A water supply “savings account” for SWP water that is allocated to an 
           SWP contractor in a given year, but not used by the end of the year. 
           Carryover water is stored in the SWP's share of San Luis Reservoir, when 
           space is available, for the contractor to use in the following year."""


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
    text=tablea_text,
)
a21_card = CardWidget(
    "SWP Article 21 Deliveries",
    button_id="a21_btn",
    button_label="View by Contractor",
    chart=card_bar_plot_cy(df_dv, b_part="SWP_IN_TOTAL"),
    text=a21_text,
)
a56_card = CardWidget(
    "SWP Carryover Deliveries",
    button_id="a56_btn",
    button_label="View by Contractor",
    chart=card_bar_plot_cy(df_dv, b_part="SWP_CO_SOD"),
    text=co_text,
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
                    href="https://water.ca.gov/Library/Modeling-and-Analysis/Central-Valley-models-and-tools/CalSim-3/DCR",
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
                    href="https://data.cnra.ca.gov/dataset/state-water-project-delivery-capability-report-dcr-2023/resource/ad861b0b-c0aa-4578-8af0-54485e751ca8",
                    target="_blank",
                    style={"marginTop": "10px"},
                ),
                html.Br(),
                html.Br(),
                html.A(
                    "Risk-Informed Future Climate Scenario Documentation",
                    href="https://data.cnra.ca.gov/dataset/state-water-project-delivery-capability-report-dcr-2023/resource/dffe00a6-017c-4765-affe-36b045c24969",
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
    layout = html.Div(
        [
            html.Hr(),
            dbc.Row(
                [
                    dbc.Col(
                        class_name="col-md-3 d-none d-lg-block my-1",  # Image goes away
                        children=[
                            html.Img(
                                src=dcr_cover_path,
                                className="img-fluid",
                            ),
                        ],
                    ),
                    dbc.Col(
                        class_name="col-md-6 my-1",
                        children=[
                            # html.A(title_text),
                            dcc.Markdown('''
                                         This is the Delivery Capability Report **Re**sults 
                                         **Con**sole (ReCon), an interactive tool designed to complement 
                                         the insights provided in the Delivery Capability Report. 
                                         ReCon allows users to explore and visualize key outputs 
                                         of the DCR 2023 CalSim 3 models, providing a dynamic and 
                                         engaging way to understand delivery performance and capabilities.'''
                                         ),  
                            dcc.Markdown('''
                                         The Delivery Capability Report presents California Department of Water Resources (DWR) 
                                         analysis of the State Water Project (SWP) system and provides important planning information 
                                         for users of SWP water. The analysis provides information about how changing climate, regulatory, 
                                         and operational considerations impact SWP delivery capability.
                                         '''
                                         ),
                          
                            dcc.Markdown('''
                                        **The most salient findings of the DCR 2023 are:**  
                                        * Under existing conditions, the estimated average annual delivery of Tabler A water for this report is 2,202 TAF/year, 119 less than the 2,321 TAF/year estimated for the 2021 Report.
                                        * The likelihood of existing condition SWP Article 21 deliveries being greater than 20 TAF/year has increased by 4 percent relative to the likelihood presented in the 2021 Report.
                                        * Under the climate change scenarios, the estimated average annual delivery of Table A water shown in the three scenarios is 13 percent to 22 percent lower than under existing conditions.
                                         '''
                                         ),
                            dcc.Markdown('''
                                        Comments and questions can be emailed to [CVMsupport@water.ca.gov](mailto:CVMsupport@water.ca.gov)
                                         ''')

                        ],
                    ),
                    dbc.Col(
                        class_name="col-md my-1",
                        children=[
                            add_resources_card,
                        ],
                    ),
                ],
                style={"background-color": "#FFFFFF"},
            ),
            html.Hr(),
            dbc.Col(
                children=[
                    dbc.Row(
                        children=[
                            dbc.Col(
                                class_name="col-md",
                                children=[
                                    ta_card.create_card(),
                                ],
                            ),
                            dbc.Col(
                                class_name="col-md",
                                children=[
                                    a21_card.create_card(),
                                ],
                            ),
                        ],
                        style={"background-color": "#FFFFFF"},
                    ),
                    dbc.Row(
                        children=[
                            dbc.Col(
                                class_name="col-md",
                                children=[
                                    a56_card.create_card(),
                                ],
                            ),
                            dbc.Col(
                                class_name="col-md",
                                children=[
                                    exp_card.create_card(),
                                ],
                            ),
                        ],
                        style={"background-color": "#FFFFFF"},
                    ),
                    dbc.Row(
                        children=[
                            dbc.Col(
                                class_name="col-md",
                                children=[
                                    orovl_sep_card.create_card(),
                                ],
                            ),
                            dbc.Col(
                                class_name="col-md",
                                children=[
                                    orovl_may_card.create_card(),
                                ],
                            ),
                        ],
                        style={"background-color": "#FFFFFF"},
                    ),
                    dbc.Row(
                        children=[
                            dbc.Col(
                                class_name="col-md",
                                children=[
                                    sluis_card.create_card(),
                                ],
                            ),
                            dbc.Col(
                                class_name="col-md",
                                children=[
                                    swp_alloc_card.create_card(),
                                ],
                            ),
                        ],
                        style={"background-color": "#FFFFFF"},
                    ),
                ]
            ),
            html.Hr(),
            html.Div(id="output-div"),
        ],
        # style=GLOBAL_MARGIN,
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
            return f"/dry_wet_periods", True

        if button_index in ("C_CAA003_SWP", "S_OROVL", "S_SLUIS_SWP"):
            return f"/drilldown?{url_params}", True
        else:
            return f"/contractor_summary?{url_params}", True
