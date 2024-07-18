import dash_bootstrap_components as dbc
from dash import html, register_page

from charts.chart_layouts import CardWidget, card_bar_plot_cy, card_mon_plot
from pages.styles import GLOBAL_MARGIN
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
    text="Eight River Index is the sum of Sacramento River Runoff and San Joaquin River Runoff",
)

sac_four_ri_card_mon = CardWidget(
    "Sacramento River Runoff",
    button_id=None,
    button_label=None,
    chart=card_mon_plot(
        df_sv, b_part="SAC4", yaxis_title="Sacramento River Runoff (TAF)"
    ),
    text="""Sacramento River Runoff is the sum of Sacramento River at Bend Bridge, 
                        Feather River inflow to Lake Oroville, Yuba River at Smartville, 
                        and American River inflow to Folsom Lake.""",
)

sjr_four_ri_card_mon = CardWidget(
    "San Joaquin River Runoff",
    button_id=None,
    button_label=None,
    chart=card_mon_plot(
        df_sv, b_part="SJR4", yaxis_title="San Joaquin River Runoff (TAF)"
    ),
    text="""San Joaquin River Runoff is the sum of Stanislaus River inflow to New Melones
                        Lake, Tuolumne River inflow to New Don Pedro Reservoir, Merced River inflow
                        to Lake McClure, and San Joaquin River inflow to Millerton Lake""",
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
# Layout


def layout():
    layout = html.Div(
        [
            html.H2(["Hydrology Comparison"]),
            # dcc.RangeSlider(1922, 2021, 1, value=[1922, 2021],
            #        marks={i: '{}'.format(i) for i in range(1922,2021,5)},
            #        pushable=False,
            #        id='hydrology-range-slider'
            # ),
            # dcc.Checklist(options = wyt_list,
            #        value = wyt_list,
            #        inline=True,
            #        id = 'wytchecklist-bar',
            #        inputStyle={"margin-right": "5px","margin-left": "30px"},
            # ),
            # html.Div(id='hydrology-range-slider-output'),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            eight_ri_card_ann.create_card(height="25rem"),
                        ]
                    ),
                    dbc.Col(
                        [
                            sac_four_ri_card_ann.create_card(height="25rem"),
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            sjr_four_ri_card_ann.create_card(height="25rem"),
                        ]
                    ),
                    dbc.Col(
                        [
                            orov_inflow_card_ann.create_card(height="25rem"),
                        ]
                    ),
                ]
            ),
            html.Hr(),
            eight_ri_card_mon.create_card(height="35rem"),
            sac_four_ri_card_mon.create_card(height="35rem"),
            sjr_four_ri_card_mon.create_card(height="35rem"),
            orov_inflow_card_mon.create_card(height="35rem"),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            orov_inflow_card_drier_mon.create_card(height="35rem"),
                        ]
                    ),
                    dbc.Col(
                        [
                            orov_inflow_card_wetter_mon.create_card(height="35rem"),
                        ]
                    ),
                ]
            ),
        ],
        style=GLOBAL_MARGIN,
    )
    return layout


# Callbacks
