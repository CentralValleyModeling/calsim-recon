import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc, html

from data import create_download_button
from pages.styles import PLOT_COLORS
from utils.query_data import scen_aliases, var_dict
from utils.tools import cfs_taf, convert_cm_nums, month_list, monthfilter


INFO_ICON = html.I(className='fa fa-info-circle', style=dict(display='inline-block'))


# ToDo use dictionaries to allow arbitrary number of buttons
class CardWidget:
    def __init__(
        self,
        title: str,
        button_id: str,
        button_label="Explore",
        button_id2="placeholder",
        button_label2: str | None = None,
        popover_label: str | None = None,
        popover_content: str | None = None,
        chart: html.Div = None,
        text=None,
        image=None,
        element_id: str = None,
    ) -> None:
        if element_id is None:
            element_id = str(id(self))
        self.id = element_id
        self.title = title
        self.button_id = button_id
        self.button_label = button_label
        self.button_id2 = button_id2
        self.button_label2 = button_label2
        self.popover_label = popover_label
        self.popover_content = popover_content
        self.chart = chart
        self.text = text
        self.image = image

    def create_card(
        self,
        height="35rem",
        wyt=[1, 2, 3, 4, 5],
        startyr=1922,
        endyr=2021,
        registry_id: str | None = None,
    ):
        if registry_id:
            download_button = create_download_button(registry_id, self.chart)
        else:
            download_button = None
        card = dbc.Card(
            class_name="m-2",
            children=[
                html.A(id=self.id),
                dbc.CardImg(src=self.image, top=True) if self.image else None,
                dbc.CardBody(
                    [

                        html.H4(self.title, className="card-title",
                                style={"display": "inline-block"}),
                        (
                            dbc.Button(
                                INFO_ICON,
                                id=self.popover_label,
                                color="link",
                            )
                            if self.popover_label is not None
                            else None
                        ),
                        self.chart,
                        (
                            html.P(self.text, className="card-text")
                            if isinstance(self.text, str)
                            else self.text  # If str, render, otherwise use as is
                        ),
                        dbc.Col(
                            children=[
                                (
                                    dbc.Button(
                                        self.button_label,
                                        id={
                                            "type": "dynamic-btn",
                                            "index": self.button_id,
                                        },
                                        color="primary",
                                        class_name="me-3",
                                    )
                                    if self.button_label is not None
                                    else None
                                ),
                                (
                                    dbc.Button(
                                        self.button_label2,
                                        id={
                                            "type": "dynamic-btn",
                                            "index": self.button_id2,
                                        },
                                        color="primary",
                                        class_name="me-3",
                                    )
                                    if self.button_label2 is not None
                                    else None
                                ),

                                (
                                    dbc.Popover(
                                        dbc.PopoverBody(self.popover_content),
                                        target=self.popover_label,
                                        trigger="hover"
                                    )
                                    if self.popover_label is not None
                                    else None

                                ),
                                (download_button),
                            ],
                        ),
                    ]
                ),
            ],
            # style={"height": height},
        )

        return card


def card_mon_plot(
    df,
    b_part="C_CAA003",
    yaxis_title=None,
    startyr=1922,
    endyr=2021,
    wyt=[1, 2, 3, 4, 5],
):
    # try:
    #    df1=df.loc[df['WYT_SAC_'].isin(wyt)]
    # except:
    #    print("WYT_SAC_ timeseries not found")
    df1 = df.loc[df["WYT_SAC_"].isin(wyt)]
    df1 = round(df1.groupby(["Scenario", "iwm"]).mean())
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
        xaxis_title="Month",
        yaxis_title=yaxis_title if yaxis_title is not None else b_part,
    )
    layout = html.Div([dcc.Graph(figure=fig)])
    return layout


def card_bar_plot_cy(
    df: pd.DataFrame,
    b_part: str = "C_CAA003",
    wyt: list[int] = None,
    startyr: int = 1922,
    endyr: int = 2021,
):
    if wyt is None:
        wyt = [1, 2, 3, 4, 5]
    # This is VERY specific to the DCR 2021
    df_dcr21 = df.loc[(df["Scenario"].isin(["DCR_21_Hist"])) & (df["icy"] >= startyr)]
    try:
        df_dcr21 = cfs_taf(df_dcr21, var_dict)
    except Exception:
        print(f"Unable to convert from CFS to TAF for {b_part}")
    df_dcr21_ann = round(df_dcr21.groupby(["Scenario"]).sum() / (2015 - 1922 + 1))
    df0 = df.loc[
        df["Scenario"].isin(
            [
                "DCR_23_Adj",
                "DCR_23_CC50",
                "DCR_23_CC75",
                "DCR_23_CC95",
            ]
        )
        & (df["icy"] >= startyr)
    ]
    try:
        df0 = cfs_taf(df0, var_dict)
    except Exception:
        print(f"Unable to convert from CFS to TAF for {b_part}")
    # For the last year
    df1 = round(df0.groupby(["Scenario"]).sum() / (endyr - startyr + 1))
    df_plot = pd.concat([df_dcr21_ann, df1])
    fig = px.bar(
        df_plot[b_part],
        text=df_plot[b_part],
        color=df_plot.index,
        orientation="h",
        color_discrete_sequence=PLOT_COLORS,
    )
    fig.update_layout(
        barmode="relative",
        plot_bgcolor="white",
        # width=600,
        height=300,
        showlegend=False,
        xaxis_title="TAF/Calendar Year",
        yaxis_title="",
        xaxis_tickformat=",d",
    )
    layout = html.Div([dcc.Graph(figure=fig)])

    return layout


def card_mon_exc_plot(df, b_part, monthchecklist):
    fig = mon_exc_plot(df, b_part, monthchecklist)
    fig.update_layout(
        # width=800,
        height=400,
    )

    layout = html.Div(
        [
            dbc.Col(
                [
                    dcc.Markdown("**Monthly Non-Exceedance Probability**"),
                    dcc.Graph(figure=fig),
                ]
            ),
        ]
    )
    return layout


def ann_bar_plot(df, b_part="C_CAA003", startyr=1922, endyr=2021, wyt=[1, 2, 3, 4, 5]):

    try:
        df0 = df.loc[df["WYT_SAC_"].isin(wyt)]
    except KeyError as e:
        print(e)

    df0 = cfs_taf(df0, var_dict)

    df1 = round(df0.groupby(["Scenario"]).sum() / (endyr - startyr + 1))
    df1 = df1.reindex(scen_aliases, level="Scenario")
    fig = px.bar(
        df1,
        x=df1.index.get_level_values(0),
        y=b_part,
        color=df1.index.get_level_values(0),
        text_auto=True,
        color_discrete_sequence=PLOT_COLORS,
    )
    fig.update_layout(
        barmode="relative",
        plot_bgcolor="white",
    )
    # fig.update_xaxes(gridcolor='LightGrey')
    fig.update_yaxes(gridcolor="LightGrey")
    return fig


def mon_exc_plot(df, b_part, monthchecklist):
    series_container = []
    # Filter the calendar months
    df0 = df.loc[df["icm"].isin(convert_cm_nums(monthchecklist))]
    for scenario in scen_aliases:
        series_i = df0.loc[df0["Scenario"] == scenario, b_part]
        series_i = series_i.sort_values()
        series_i = series_i.reset_index(drop=True)
        series_i.rename(scenario, inplace=True)
        series_container.append(series_i)

    df3 = pd.concat(series_container, axis=1)
    fig = go.Figure()

    for i, column in enumerate(df3.columns):
        series_sorted = df3[column].dropna()
        exceedance_prob = (series_sorted.index + 1) / len(series_sorted) * 100
        # linearly interpolate the line above so we get 100 points, from 1-100
        df = pd.DataFrame(data={"y": series_sorted, "x": exceedance_prob})
        integer_index = df["x"].round(decimals=0).astype(int)
        # This step should really be an interpolation using scipy.interp1d, but it works
        # with the dependencies that we have right now
        # TODO: 2024-07-18 Consider updating to an interpolation method
        df = df.groupby(integer_index).mean()
        df = df.reindex(index=range(1, 101, 1)).ffill()
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["y"],
                mode="lines",
                name=column,
                line=dict(color=PLOT_COLORS[i % len(PLOT_COLORS)]),
            )
        )

    fig.update_layout(
        plot_bgcolor="white",
        xaxis_title="Non Exceedance Probability (%)",
        xaxis_tickformat=",d",
        yaxis_title="",
        legend_title="Scenario",
        showlegend=True,
        xaxis=dict(gridcolor="LightGrey"),
        yaxis=dict(gridcolor="LightGrey"),
    )

    return fig


def ann_exc_plot(df, b_part, monthchecklist, yearwindow):
    series_container = []
    if yearwindow == "Calendar Year":
        yw = "icy"
    else:
        yw = "iwy"

    df0 = df.loc[df["icm"].isin(convert_cm_nums(monthchecklist))]
    df0 = cfs_taf(df0, var_dict)
    df0 = df0.groupby(["Scenario", yw]).sum()

    for scenario in scen_aliases:
        series_i = df0.loc[df0.index.get_level_values(0) == scenario, b_part]
        series_i = series_i.sort_values()
        series_i = series_i.reset_index(drop=True)
        series_i.rename(scenario, inplace=True)
        series_container.append(series_i)

    df3 = pd.concat(series_container, axis=1)
    fig1 = go.Figure()

    for i, column in enumerate(df3.columns):
        series_sorted = df3[column].dropna()
        exceedance_prob = (series_sorted.index + 1) / len(series_sorted) * 100
        # linearly interpolate the line above so we get 100 points, from 1-100
        df = pd.DataFrame(data={"y": series_sorted, "x": exceedance_prob})
        integer_index = df["x"].round(decimals=0).astype(int)
        # This step should really be an interpolation using scipy.interp1d, but it works
        # with the dependencies that we have right now
        # TODO: 2024-07-18 Consider updating to an interpolation method
        df = df.groupby(integer_index).mean()
        df = df.reindex(index=range(1, 101, 1)).ffill()

        fig1.add_trace(
            go.Scatter(
                x=df.index,
                y=df["y"],
                mode="lines",
                name=column,
                line=dict(color=PLOT_COLORS[i % len(PLOT_COLORS)]),
            )
        )

    fig1.update_layout(
        plot_bgcolor="white",
        xaxis_title="Non Exceedance Probability (%)",
        xaxis_tickformat=",d",
        yaxis_title="",
        legend_title="Scenario",
        showlegend=True,
        xaxis=dict(gridcolor="LightGrey"),
        yaxis=dict(gridcolor="LightGrey"),
    )

    return fig1


def distplot(df, b_part):
    df2 = pd.DataFrame()
    df0 = df
    df0 = cfs_taf(df0, var_dict)
    df0 = df0.groupby(["Scenario", "iwy"]).sum()

    for scenario in scen_aliases:
        df1 = df0.loc[df0.index.get_level_values(0) == scenario, b_part]
        df1 = df1.reset_index(drop=True)
        df2[scenario] = df1

    fig = px.histogram(
        df2, marginal="box", color_discrete_sequence=PLOT_COLORS, barmode="relative"
    )
    return fig


def ta_dry_wet_barplot(
    df, common_pers, bpart="SWP_TA_CO_SOD", scens=None, ta_tot=4133, perlist=None
):
    df1 = pd.DataFrame()
    df = cfs_taf(df, var_dict)
    left = {"scenario": [], "period": [], "avg": [], "pct": [], "label": []}
    l_df = pd.DataFrame()
    for s in scens:
        for c in common_pers:
            if c in perlist:
                startyr = int(common_pers[c].split("-")[0])
                endyr = int(common_pers[c].split("-")[-1])
                df1 = df.loc[df["Scenario"] == s, [bpart, "icy"]]
                df2 = df1.loc[df1["icy"].between(startyr, endyr)]
                v = round(df2[bpart].sum() / (endyr - startyr + 1), 0)
                left["scenario"].append(s)
                left["period"].append(c)
                left["avg"].append(v)
                left["pct"].append(round((v / ta_tot), 2))
                left["label"].append(f"{round((v/ta_tot)*100)}%")
    l_df = pd.DataFrame(left)
    # print(l_df)
    fig = px.bar(
        l_df,
        x="period",
        y="pct",
        text="label",
        color="scenario",
        barmode="group",
        color_discrete_sequence=PLOT_COLORS,
        hover_data={"avg": True},
        range_y=[0, 1],
    )

    fig.update_layout(
        yaxis_tickformat=".0%",
        xaxis_title="",
        yaxis_title="Table A Percent Allocation",
        yaxis=dict(
            tickmode="array",
            tickvals=[i / 100 for i in range(0, 101, 10)],
            ticktext=[f"{i}%" for i in range(0, 101, 10)],
        ),
        # width=1200,
        height=600,
    )
    fig.update_traces(textposition="outside")

    return fig


def a21_dry_wet_barplot(
    df,
    common_pers,
    bpart="SWP_IN_TOTAL",
    scens=None,
    perlist=None,
):
    df1 = pd.DataFrame()
    df = cfs_taf(df, var_dict)
    left = {"scenario": [], "period": [], "avg": []}
    l_df = pd.DataFrame()
    for s in scens:
        for c in common_pers:
            if c in perlist:
                startyr = int(common_pers[c].split("-")[0])
                endyr = int(common_pers[c].split("-")[-1])
                df1 = df.loc[df["Scenario"] == s, [bpart, "icy"]]
                df2 = df1.loc[df1["icy"].between(startyr, endyr)]
                v = round(df2[bpart].sum() / (endyr - startyr + 1), 0)
                left["scenario"].append(s)
                left["period"].append(c)
                left["avg"].append(v)
    l_df = pd.DataFrame(left)
    # print(l_df)
    fig = px.bar(
        l_df,
        x="period",
        y="avg",
        text="avg",
        color="scenario",
        barmode="group",
        color_discrete_sequence=PLOT_COLORS,
        hover_data={"avg": True},
    )

    fig.update_layout(
        yaxis_tickformat=",d",
        xaxis_title="",
        yaxis_title="Article 21 Deliveries (TAF/Contract Year)",
        # yaxis = dict(tickmode='array',
        #            tickvals=[i/100 for i in range(0, 101, 10)],
        #            ticktext=[f'{i}%' for i in range(0, 101, 10)]),
        # width=1200,
        height=600,
    )
    fig.update_traces(textposition="outside")

    fig.layout.autosize = True

    return fig
