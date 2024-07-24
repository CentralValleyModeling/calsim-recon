# import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import yaml
from dash import (Dash, Input, Output, callback, dash_table, dcc, html,
                  register_page)

from utils.query_data import df_dv, scen_aliases, var_dict
from utils.tools import (cfs_taf, convert_cm_nums, convert_wyt_nums,
                         load_data_mult, make_ressum_df, make_summary_df,
                         month_list, month_map, wyt_list)

register_page(
    __name__,
    name="Summary Table",
    top_nav=True,
    path="/summary",
    order=4,
)

summary_text = (
    """This page provides annual averages for key system variables. """,
    """Types include upstream river flows, Delta inflow """,
    """and outflows, exports, and deliveries.""",
    html.Br(),
    html.Br(),
)

exp_tbl = make_summary_df(
    scen_aliases,
    df_dv,
    var_dict,
    bparts=[
        "C_LWSTN",
        "D_LWSTN_CCT011",
        "C_WKYTN",
        "C_KSWCK",
        "C_SAC097",
        "C_FTR059",
        "C_FTR003",
        "C_YUB006",
        "C_SAC083",
        "C_NTOMA",
        "C_AMR004",
        #   '----'
        "DELTAINFLOWFORNDOI",
        #    '----'
        "NDOI",
        # 
        "C_CAA003",
        "C_CAA003_SWP",
        "C_CAA003_CVP",
        "C_CAA003_WTS",
        "C_DMC000",
        "C_DMC000_CVP",
        "C_DMC000_WTS",
        #    '----',
        "SWP_TA_TOTAL",
        "SWP_IN_TOTAL",
        "SWP_CO_TOTAL",
        "CVPTOTALDEL",
    ],
)

# Determine the table order
# Descriptive stuff goes first
table_order = [
    {"name": "Type", "id": "type"},
    {"name": "Description", "id": "description"},
    {"name": "B-Part", "id": "bpart"},
    {"name": "Year Type", "id": "year"},
]

# Scenarios go next
table_order.extend(
    [
        {"name": s, "id": s, "type": "numeric", "format": {"specifier": ",.0f"}}
        for s in scen_aliases
        if s not in ["description", "index", "type"]
    ]
)


def layout():
    layout = dbc.Container(
        class_name="m-2",
        children=[
            dcc.Markdown("# Summary Table"),
            html.A(summary_text),
            dbc.Row(
                [
                    dcc.Markdown("#### "),
                    dash_table.DataTable(
                        id="exp_tbl",
                        columns=table_order,
                        data=exp_tbl.to_dict(orient="records"),
                        style_header={
                            "backgroundColor": "rgb(200, 200, 200)",
                            "fontWeight": "bold",
                        },
                        style_cell={
                            "width": "{}%".format(len(exp_tbl.columns)),
                            # 'width': '1000px',
                            "textOverflow": "ellipsis",
                            "overflow": "hidden",
                            "textAlign": "left",
                        },
                    ),
                ]
            ),
        ],
    )
    return layout


layout()
