# import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import (
    Input,
    Output,
    State,
    callback,
    dash_table,
    dcc,
    html,
    no_update,
    register_page,
)

from charts.chart_layouts import ann_exc_plot
from data import create_download_button, universal_data_download
from data.downloads import CHART_REGISTRY
from utils.query_data import df_dv, scen_aliases, var_dict
from utils.tools import common_pers, make_summary_df, month_list

register_page(
    __name__,
    name="Contractor Summary",
    top_nav=True,
    path="/contractor_summary",
    order=5,
)

b = []

# Determine the table order
# Descriptive stuff goes first
table_order = [
    {"name": "Type", "id": "type"},
    {"name": "Description", "id": "description"},
    {"name": "B-Part", "id": "bpart"},
]

# Scenarios go next
table_order.extend(
    [
        {"name": s, "id": s, "type": "numeric", "format": {"specifier": ",.0f"}}
        for s in scen_aliases
        if s not in ["description", "index", "type"]
    ]
)

typefilter_dict = {
    "table_a_btn": "Delivery - TA",
    "a21_btn": "Delivery - IN",
    "a56_btn": "Delivery - CO",
}

opt = [{"label": k, "value": v} for k, v in common_pers.items()]

DWNLD_BUTTON_ID = "contractor-specific-exceedance"


def layout(**kwargs):
    global b
    global exp_tbl
    b = []
    s = str(kwargs.get("type", "table_a_btn"))
    typefilter = typefilter_dict[s]

    for i in var_dict:
        if var_dict[i]["type"] == typefilter:
            b.append(i)
    exp_tbl = make_summary_df(
        scen_aliases, df_dv, var_dict, bparts=b, start_yr=1922, end_yr=2021
    )
    graph_div = dcc.Graph(id="contractor-exceedance-graph")

    layout = dbc.Container(
        class_name="m-2",
        children=[
            dcc.Download(id="download-response-contractor"),
            # dcc.Markdown("# ![](/assets/cs3_icon_draft.png) CalSim 3 Summary Table"),
            dcc.RangeSlider(
                1922,
                2021,
                1,
                value=[1922, 2015],
                marks={i: "{}".format(i) for i in range(1922, 2021, 5)},
                pushable=False,
                id="slider-yr-range",
            ),
            dcc.Dropdown(
                options=opt,
                id="dropdown_common_pers_csum",
                placeholder="Select the Averaging Period (Contract Years)",
            ),
            html.Div(id="output-container-range-slider_2"),
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
                            "textOverflow": "ellipsis",
                            "overflow": "hidden",
                            "textAlign": "left",
                        },
                    ),
                    graph_div,
                    html.Div(
                        className="m-3",
                        children=create_download_button(DWNLD_BUTTON_ID, graph_div),
                    ),
                ]
            ),
        ],
    )
    return layout


# Update Summary Table
@callback(
    Output(component_id="exp_tbl", component_property="data"),
    Input(component_id="slider-yr-range", component_property="value"),
)
def update_table(slider_yr_range):
    df_tbl = make_summary_df(
        scen_aliases,
        df_dv,
        var_dict,
        bparts=b,
        start_yr=slider_yr_range[0],
        end_yr=slider_yr_range[1],
    )
    data = df_tbl.to_dict(orient="records")
    return data


# Write out the range slider selections
@callback(
    Output("output-container-range-slider_2", "children"),
    Input("slider-yr-range", "value"),
)
def read_slider(value) -> tuple:
    return str("Average Period: "), value[0], str("-"), value[1]


# Update range slider with common period selection
@callback(
    Output("slider-yr-range", "value"),
    Input("dropdown_common_pers_csum", "value"),
)
def slider(dropdown_val):
    startyr, endyr = 1922, 2021
    if isinstance(dropdown_val, str):
        startyr = int(dropdown_val.split("-")[0])
        endyr = int(dropdown_val.split("-")[-1])

    return startyr, endyr


# Return plot for selected contractor
@callback(
    Output("contractor-exceedance-graph", "figure"),
    Input("exp_tbl", "active_cell"),
    prevent_initial_call=True,
)
def show_contractor_data(click_data):
    if click_data is None:
        return "Click on a cell"
    else:
        b = exp_tbl.loc[click_data["row"]]["bpart"]
        fig = ann_exc_plot(
            df_dv,
            b,
            monthchecklist=month_list,
            yearwindow="Calendar Year",
        )
        # We need to re-register the figure when it's updated
        CHART_REGISTRY[DWNLD_BUTTON_ID] = lambda *_: fig
        return fig


@callback(
    output=Output("download-response-contractor", "data"),
    inputs=[Input(DWNLD_BUTTON_ID, "n_clicks")],
    state=[State("exp_tbl", "active_cell")],
    prevent_initial_call=True,
)
def contractor_data_download(inputs, state):
    if state is None:
        return no_update
    else:
        b = exp_tbl.loc[state["row"]]["bpart"]
    return universal_data_download(csv_name=f"exceedance-{b}.csv")
