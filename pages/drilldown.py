# Imports
from collections import namedtuple

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, dcc, html, register_page

from charts.chart_layouts import ann_exc_plot, mon_exc_plot
from pages.styles import PLOT_COLORS
from utils.query_data import date_map, df_dv, scen_aliases, var_dict
from utils.tools import (
    cfs_taf,
    convert_wyt_nums,
    list_files,
    load_data_mult,
    make_ressum_df,
    make_summary_df,
    month_list,
    monthfilter,
    month_map,
    wyt_list,
)

register_page(
    __name__,
    name="Drilldown",
    top_nav=True,
    path="/drilldown",
    order=6,
)

drilldown_text = (
    """This page allows users to view various plots and metrics on a timeseries.
    The user can choose timeseries by B-Part or by alias using the drop down menus
    or by typing within the text box.""",
    html.Br(),
    """Plots and statistics include: monthly and annual timeseries, 
    monthly and annual probability of non-exceedance curves,
    monthly and annual average.""",
    html.Br(),
    html.Br(),
    """Users have the flexibility to change the year type for annual plots,
    aggregation method for annual timeseries,
    months in the exceedance probability plot,
    water year types for the monthly avearge,
    using the slider and drop down menu.""",
    html.Br(),
    html.Br(),
)

bparts = []
aliases = []

for var in var_dict:
    bparts.append(var)
    aliases.append(var_dict[var]["alias"])


# DataFrames for the summary tables
df_tbl = make_summary_df(scen_aliases, df_dv, var_dict)
df_tbl_res = make_ressum_df(scen_aliases, df_dv, var_dict)


# Layout Starts Here
def layout(**kwargs):
    b = kwargs.get("type", "C_CAA003")
    print(b)
    layout = dbc.Container(
        class_name="my-3",
        children=[
            dbc.Row(
                [
                    html.H1("Drilldown"),
                    html.A(drilldown_text),
                    dbc.Col(
                        [
                            "Select B-Part: ",
                            dcc.Dropdown(
                                bparts, id="b-part", value=b, style={"width": "100%"}
                            ),
                            "Or search by alias: ",
                            dcc.Dropdown(
                                options=aliases,
                                id="alias",
                                value=var_dict[b]["alias"],
                                style={"width": "100%"},
                            ),
                        ],
                        width=6,
                    ),
                ]
            ),
            html.Br(),
            html.Div(id="my-output"),
            dbc.Row(
                [
                    dcc.Markdown("**Timeseries**"),
                    dcc.Graph(id="timeseries-plot"),
                ]
            ),
            dbc.Row(
                [
                    dcc.Markdown("**Annual Timeseries**"),
                    dbc.Col(
                        [
                            html.P(
                                "Select Year Type for Annual Timeseries Plot",
                                className="text-muted mt-1 m-0",
                            ),
                            dcc.Dropdown(
                                options=["Calendar Year", "Water Year"],
                                id="year-type-annual-timeseries",
                                style={"width": "50%"},
                                value="Water Year",
                            ),
                            html.P(
                                "Select Aggregation Method for Annual Timeseries Plot",
                                className="text-muted mt-1 m-0",
                            ),
                            dcc.Dropdown(
                                options=["Mean", "Max", "Min", "Sum"],
                                id="agg-annual-timeseries",
                                style={"width": "50%"},
                                value="Mean",
                            ),
                        ]
                    ),
                    dcc.Graph(id="annual-timeseries-plot"),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Markdown("**Monthly Exceedance**"),
                            dcc.Checklist(
                                options=month_list,
                                value=month_list,
                                inline=True,
                                id="monthchecklist-exc",
                                inputStyle={
                                    "margin-right": "5px",
                                    "margin-left": "5px",
                                },
                            ),
                            dcc.Graph(id="exceedance-plot"),
                        ],
                        align="center",
                    ),
                    dbc.Col(
                        [
                            dcc.Markdown("**Monthly Average**"),
                            dcc.Checklist(
                                options=wyt_list,
                                value=wyt_list,
                                inline=True,
                                id="wytchecklist-bar",
                                inputStyle={
                                    "margin-right": "5px",
                                    "margin-left": "30px",
                                },
                            ),
                            dcc.Graph(id="bar-plot"),
                        ]
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Markdown("**Annual Exceedance**"),
                            dcc.Dropdown(
                                options=["Calendar Year", "Water Year"],
                                id="yearwindow",
                                style={"width": "50%"},
                                value="Water Year",
                            ),
                            dcc.Graph(id="exceedance-plot-annual"),
                        ]
                    ),
                    dbc.Col(
                        [
                            dcc.Markdown("**Annual Average**"),
                            dcc.Dropdown(
                                options=["Calendar Year", "Water Year"],
                                id="yearwindow-repeater",
                                style={"width": "50%"},
                                value="Water Year",
                                disabled=True,
                            ),
                            dcc.Graph(id="bar-plot-annual"),
                        ]
                    ),
                ]
            ),
            dcc.RangeSlider(
                1922,
                2021,
                1,
                value=[1922, 2021],
                marks={i: "{}".format(i) for i in range(1922, 2021, 5)},
                pushable=False,
                id="slider-yr-range",
            ),
            html.Div(id="output-container-range-slider"),
        ],
        fluid=False,
    )
    return layout


# CALLBACKS Start Here


# Return B Part based on alias search
@callback(
    Output(component_id="b-part", component_property="value"),
    Input(component_id="alias", component_property="value"),
)
def update_b_part(alias):
    i = aliases.index(str(alias))
    b = bparts[i]
    return b


# Timeseries Plot
@callback(
    Output(component_id="timeseries-plot", component_property="figure"),
    Input(component_id="b-part", component_property="value"),
)
def update_timeseries(b_part):
    fig = px.line(
        df_dv,
        x=df_dv.index,
        y=b_part,
        color="Scenario",
        color_discrete_sequence=PLOT_COLORS,
    )
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(gridcolor="LightGray"),
        yaxis=dict(gridcolor="LightGray"),
    )
    return fig


# Annual Timeseries Plot
@callback(
    Output(component_id="annual-timeseries-plot", component_property="figure"),
    Input(component_id="b-part", component_property="value"),
    Input(component_id="year-type-annual-timeseries", component_property="value"),
    Input(component_id="agg-annual-timeseries", component_property="value"),
)
def update_annual_timeseries(
    b_part,
    year_type: str = "Calendar Year",
    agg_method: str = "Mean",
):
    offsets = {
        "Calendar Year": 1,
        "Water Year": 10,
    }
    df_agg = (
        df_dv.loc[:, [b_part, "Scenario"]]
        .groupby("Scenario")
        .resample(rule=pd.offsets.YearBegin(month=offsets[year_type]))
        .agg({b_part: [agg_method.lower(), "count"]})
        .reset_index()
    )
    df_agg.columns = ["-".join(c).strip("- ") for c in df_agg.columns]
    count = df_agg[f"{b_part}-count"]
    df_agg[year_type] = df_agg["Date"]
    df_agg[b_part] = df_agg[f"{b_part}-{agg_method.lower()}"]  # Clean name of agg
    df_agg = df_agg.loc[count == 12, :]  # Filter to only show full years of data
    fig = px.line(
        df_agg,
        x=year_type,
        y=b_part,
        color="Scenario",
        color_discrete_sequence=PLOT_COLORS,
    )
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(gridcolor="LightGray"),
        yaxis=dict(gridcolor="LightGray"),
    )
    return fig


# Exceedance Plot
@callback(
    Output(component_id="exceedance-plot", component_property="figure"),
    Input(component_id="b-part", component_property="value"),
    Input(component_id="monthchecklist-exc", component_property="value"),
)
def update_exceedance(b_part, monthchecklist):
    fig = mon_exc_plot(df_dv, b_part, monthchecklist)
    return fig


# Annual Exceedance Plot
@callback(
    Output(component_id="exceedance-plot-annual", component_property="figure"),
    Input(component_id="b-part", component_property="value"),
    Input(component_id="monthchecklist-exc", component_property="value"),
    Input(component_id="yearwindow", component_property="value"),
)
def update_exceedance(b_part, monthchecklist, yearwindow):
    fig = ann_exc_plot(df_dv, b_part, monthchecklist, yearwindow)
    return fig


# Monthly Average Plot
@callback(
    Output(component_id="bar-plot", component_property="figure"),
    Input(component_id="b-part", component_property="value"),
    Input(component_id="wytchecklist-bar", component_property="value"),
    Input(component_id="slider-yr-range", component_property="value"),
)
def update_monthly(b_part, wytchecklist, slider_yr_range):
    startyr = slider_yr_range[0]
    endyr = slider_yr_range[1]
    df0 = df_dv.loc[
        df_dv["WYT_SAC_"].isin(convert_wyt_nums(wytchecklist))
        & (df_dv["iwy"] >= startyr)
        & (df_dv["iwy"] <= endyr)
    ]
    df1 = round(df0.groupby(["Scenario", "iwm"]).mean())
    df1 = df1.reindex(scen_aliases, level="Scenario")
    fig = px.line(
        df1,
        x=df1.index.get_level_values(1),
        y=b_part,
        color=df1.index.get_level_values(0),
        labels={"color": "Scenario"},
        color_discrete_sequence=PLOT_COLORS,
    )
    fig.update_layout(
        plot_bgcolor="white",
        xaxis=dict(
            tickmode="array",
            tickvals=monthfilter,
            ticktext=month_list,
            showgrid=True,
            gridcolor="LightGray",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="LightGray",
        ),
        yaxis_tickformat=",d",
        xaxis_title="Month"
    )

    return fig


# Annual Bar Plot
@callback(
    Output(component_id="bar-plot-annual", component_property="figure"),
    Input(component_id="b-part", component_property="value"),
    Input(component_id="wytchecklist-bar", component_property="value"),
    Input(component_id="slider-yr-range", component_property="value"),
)
def update_bar_annual(b_part, wytchecklist, slider_yr_range):
    startyr = slider_yr_range[0]
    endyr = slider_yr_range[1]
    print(wytchecklist)
    df1 = df_dv.loc[
        df_dv["WYT_SAC_"].isin(convert_wyt_nums(wytchecklist))
        & (df_dv["iwy"] >= startyr)
        & (df_dv["iwy"] <= endyr)
    ]

    df1 = cfs_taf(df1, var_dict)

    df2 = round(df1.groupby(["Scenario"]).sum() / (endyr - startyr + 1))
    df2 = df2.reindex(scen_aliases, level="Scenario")
    fig = px.bar(
        df2,
        x=df2.index.get_level_values(0),
        y=b_part,
        color=df2.index.get_level_values(0),
        text_auto=True,
        color_discrete_sequence=PLOT_COLORS,
    )
    fig.update_layout(
        barmode="relative",
        plot_bgcolor="white"
    )
    return fig


# Flow Summary tables
@callback(
    Output(component_id="sum_tbl", component_property="data"),
    Input(component_id="slider-yr-range", component_property="value"),
    Input(component_id="monthchecklist", component_property="value"),
)
def update_table(slider_yr_range, monthchecklist):
    monthfilter = []
    for v in monthchecklist:
        monthfilter.append(month_map[v])

    df_tbl = make_summary_df(
        scen_aliases,
        df_dv,
        var_dict,
        start_yr=slider_yr_range[0],
        end_yr=slider_yr_range[1],
        monthfilter=monthfilter,
    )
    data = df_tbl.to_dict(orient="records")
    return data


# Reservoir Summary tables
@callback(
    Output(component_id="sum_tbl_res", component_property="data"),
    Input(component_id="slider-yr-range", component_property="value"),
    Input(component_id="monthradio", component_property="value"),
)
def update_table2(slider_yr_range, monthradio):
    monthradio = [month_map[monthradio]]

    df_tbl = make_ressum_df(
        scen_aliases,
        df_dv,
        var_dict,
        start_yr=slider_yr_range[0],
        end_yr=slider_yr_range[1],
        monthfilter=monthradio,
    )
    data = df_tbl.to_dict(orient="records")
    return data


@callback(
    Output(component_id="output-container-range-slider", component_property="children"),
    Input(component_id="slider-yr-range", component_property="value"),
)
def set_slider(value):
    return value[0], str("-"), value[1]


@callback(
    Output("dummy-div1", "children"),
    Input("load-studies", "n_clicks"),
    State("file-table", "data"),
    prevent_initial_call=True,
)
def load(n_clicks, full_scen_table):
    scen_dict = {}
    for s in full_scen_table:
        if s["alias"].strip() != "":
            scen_dict[s["alias"]] = s["pathname"]
    load_data_mult(scen_dict, var_dict, date_map)
    print(scen_dict)
    return "Loading"


# Callback to populate the ledger
@callback(Output("file-table", "data"), Input("populate-table", "n_clicks"))
def populate_table(n_clicks):
    scenarios = list_files("uploads")
    for s in scenarios:
        new_entries = [
            {"pathname": scenarios[s], "filename": s, "alias": ""} for s in scenarios
        ]

    return new_entries


# Return a scenario dictionary with the aliases that user entered
@callback(Output("table-update-output", "children"), Input("file-table", "data"))
def display_updated_data(full_scen_table):
    if full_scen_table is None:
        return "No data in the table."
    else:
        pass

    scen_dict = {}
    for s in full_scen_table:
        if s["alias"].strip() != "":
            scen_dict[s["alias"]] = s["pathname"]
