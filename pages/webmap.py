from dash import Dash, dcc, html, Input, Output, callback, register_page
import plotly.graph_objects as go
import dashboard_map.from_shp_to_dash as api

# get the average annual sum of each delivery/agencyname
data_df = api.calc_mean()

# get a list of the scenarios for the dropdown
scenario_list = data_df["Scenario"].unique()

# get the geodata of the agencies
geodf = api.load_shp()

# Get the figure for the state border
figca = api.create_ca_plot()


# Register the page webmap on the dashboard menu
register_page(
    __name__,
    name="Webmap",
    top_nav=True,
    path="/webmap",
)


# layout function
def layout():
    layout = html.Div(
        children=[
            html.H1("State Water Project Contractor Deliveries"),
            html.Div(
                [
                    html.Label("Scenario 1:", htmlFor=("scenario_1")),
                    dcc.Dropdown(scenario_list, scenario_list[0], id="scenario_1"),
                ],
                style={"width": "48%", "display": "inline-block"},
            ),
            html.Div(
                [
                    html.Label("Scenario 2:", htmlFor=("scenario_2")),
                    dcc.Dropdown(scenario_list, scenario_list[1], id="scenario_2"),
                ],
                style={"width": "48%", "float": "right"},
            ),
            dcc.Graph(
                id="my_id",
            ),
        ]
    )

    return layout


@callback(
    Output("my_id", "figure"),
    Input("scenario_1", "value"),
    Input("scenario_2", "value"),
)
def update_graph(scen1: str, scen2: str):
    # Geo DataFrame to hold all necessary data
    scen_geodf = api.create_df_for_scen(data_df, geodf, scen1, scen2)

    # Choropleth map to show % change of flow by agency
    fig = api.create_plot(scen_geodf)

    # Scatter graph to show positive & negative percentages
    fig1 = api.create_fig_1(scen_geodf)

    trace2 = figca.data[0]
    trace1 = fig.data[0]
    trace3 = fig1.data[0]

    mycolor_scale = [
        [0, "#0000ff"],
        [0.1, "#3333ff"],
        [0.2, "#6666ff"],
        [0.3, "#9999ff"],
        [0.4, "#ccccff"],
        [0.5, "#ffffff"],
        [0.6, "#ffcccc"],
        [0.7, "#ff9999"],
        [0.8, "#ff6666"],
        [0.9, "#ff3333"],
        [1.0, "#ff0000"],
    ]

    layout = go.Layout(
        geo={"visible": False, "fitbounds": "locations"},
        autosize=False,
        height=1000,
        colorscale={"diverging": mycolor_scale},
        coloraxis={
            "cmin": -50,
            "cmax": 50,
            "cauto": False,
            "autocolorscale": False,
            "colorbar": {"title": {"text": "VAL DIFF %"}},
        },
    )
    final_fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)

    return final_fig
