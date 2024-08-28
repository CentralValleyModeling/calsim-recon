import sys
import geopandas as gpd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output, callback
import pyproj
import pandas as pd

sys.path.append(".")
import utils.query_data as qd


swp2convention = {
    "SWP_TA_AVEK": "SWC_AVEKWA",
    "SWP_TA_CVWD": "SWC_CVWD",
    "SWP_TA_CLA": "SWC_CLAWA",
    "SWP_TA_DESERT": "SWC_DWA",
    "SWP_TA_DUDLEY": "SWC_DRWD",
    "SWP_TA_EMPIRE": "SWC_EWSID",
    "SWP_TA_KERNMI": "SWC_KCWA",
    "SWP_TA_KERNAG": "SWC_KCWA",
    "SWP_TA_KINGS": "SWC_KGCC",
    "SWP_TA_LCID": "SWC_LCID",
    "SWP_TA_MWD": "SWC_MWDSC",
    "SWP_TA_MWA": "SWC_MWA",
    "SWP_TA_PWD": "SWC_PWD",
    "SWP_TA_SBV": "SWC_SBVMWD",
    "SWP_TA_SGV": "SWC_SGVMWD",
    "SWP_TA_SGP": "SWC_SGPWA",
    "SWP_TA_SLO": "SWC_SLOCFCWCD",
    "SWP_TA_SB": "SWC_SBCFCWCD",
    "SWP_TA_SCV": "SWC_SCVWD",
    "SWP_TA_CLWA1": "SWC_SCVWA",
    "SWP_TA_CLWA2": "SWC_SCVWA",
    "SWP_TA_TULARE": "SWC_TLBWSD",
    "SWP_TA_VC": "SWC_VCWPD",
    "SWP_TA_ACFC": "SWC_ACFCWCDZ7",
}

agencyname2convention = {
    "Antelope Valley - East Kern Water Agency": "SWC_AVEKWA",
    "Coachella Valley Water District": "SWC_CVWD",
    "Crestline - Lake Arrowhead Water Agency": "SWC_CLAWA",
    "Desert Water Agency": "SWC_DWA",
    "Dudley Ridge Water District": "SWC_DRWD",
    "Empire West Side Irrigation District": "SWC_EWSID",
    "Kern County Water Agency": "SWC_KCWA",
    "Kings County": "SWC_KGCC",
    "Littlerock Creek Irrigation District": "SWC_LCID",
    "Metropolitan Water District Of Southern California": "SWC_MWDSC",
    "Mojave Water Agency": "SWC_MWA",
    "Palmdale Water District": "SWC_PWD",
    "San Bernardino Valley Municipal Water District": "SWC_SBVMWD",
    "San Gabriel Valley Municipal Water District": "SWC_SGVMWD",
    "San Gabriel Valley Municipal  Water District": "SWC_SGVMWD",
    "San Gorgonio Pass Water Agency": "SWC_SGPWA",
    "San Luis Obispo County Flood Control And Water Conservation District": "SWC_SLOCFCWCD",
    "Santa Barbara County Flood Control and Water Conservation District": "SWC_SBCFCWCD",
    "Santa Clarita Valley Water Agency": "SWC_SCVWA",
    "Tulare Lake Basin Water Storage District": "SWC_TLBWSD",
    "Ventura County Watershed Protection District": "SWC_VCWPD",
}


def calc_mean():
    combined_df = pd.DataFrame(
        columns=["Scenario", "CONTRACTOR_CONVENTION", "icy", "VAL"]
    )

    for code in swp2convention:
        # Create a dataframe using the Scenario and code from df_dv
        df = qd.df_dv[["Scenario", "icy", code, "cfs_taf"]].copy()

        # Convert cfs to taf and drop cfs_taf column
        df[code] = df[code] * df["cfs_taf"]
        df = df.drop(columns=["cfs_taf"])

        # Rename code column to "VAL"
        df.rename(columns={code: "VAL"}, inplace=True)

        # Add contractor convention
        contractor_convention = swp2convention[code]
        df["CONTRACTOR_CONVENTION"] = contractor_convention

        # Concatenate data for this agency to the combined df
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # Calculate sum of val for Scenario, Agency name, and water year
    combined_df = combined_df.groupby(
        ["Scenario", "CONTRACTOR_CONVENTION", "icy"]  # change to icy
    ).sum()

    # Remove iwy column
    combined_df = combined_df.reset_index()
    combined_df = combined_df.drop(columns=["icy"])

    # Calculate mean
    combined_df = combined_df.groupby(["Scenario", "CONTRACTOR_CONVENTION"]).mean()

    # Reset the index
    combined_df = combined_df.reset_index()

    # Round
    combined_df["VAL"] = combined_df["VAL"].round()
    combined_df["VAL"] = combined_df["VAL"].astype(int)
    print("df:")
    print(combined_df)

    # Return the dataframe containing the average annual sum
    return combined_df


def load_shp() -> gpd.GeoDataFrame:
    geodf = gpd.read_file("SWP_Contractors.shp")
    geodf.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)

    # Add a column for conventions to geodf
    geodf["CONTRACTOR_CONVENTION"] = "TBD"

    # Using the agencyname2convention map, update CONTRACTOR_CONVENTION column val for each row
    for name in geodf["AGENCYNAME"]:
        # Get the contractor convention for the agency name
        convention = agencyname2convention[name]

        # Update the convention of the row
        geodf.loc[geodf["AGENCYNAME"] == name, "CONTRACTOR_CONVENTION"] = convention

    return geodf


def create_ca_plot():
    figca = px.choropleth(
        locations=["CA"],
        locationmode="USA-states",
        scope="usa",
        color_discrete_sequence=["rgba(255,0,0,0.0)"],
        basemap_visible=False,
        fitbounds="locations",
        height=800,
        color_continuous_scale="Bluered",
    )

    figca.update_layout(showlegend=True)

    figca.update_layout(
        coloraxis=dict(
            cmin=-100,  # Minimum value of the color scale
            cmax=100,  # Maximum value of the color scale
            colorbar=dict(title="<b>VAL DIFF %</b>"),  # Bold legend title
        )
    )
    return figca


def get_min_max(geodf: gpd.GeoDataFrame):
    maximum = max(geodf["VAL_PERC"])
    minimum = min(geodf["VAL_PERC"])
    if minimum < 0 and maximum > 0:
        abs_min = -minimum
        if abs_min >= maximum:
            maximum = abs_min
        else:
            minimum = -maximum

    return (minimum, maximum)


def create_plot(geodf: gpd.GeoDataFrame):
    maximum = max(geodf["VAL_PERC"])
    minimum = min(geodf["VAL_PERC"])
    if minimum < 0 and maximum > 0:
        abs_min = -minimum
        if abs_min >= maximum:
            maximum = abs_min
        else:
            minimum = -maximum

        fig = px.choropleth(
            geodf,
            geojson=geodf.geometry,
            locations=geodf["RANK"],
            hover_data={
                "VAL_DIFF": True,
                "VAL_PERC": True,
                "AGENCYNAME": True,
                "OBJECTID": False,
            },
            hover_name="CONTRACTOR_CONVENTION",
            color="VAL_PERC",
            basemap_visible=False,
            fitbounds="locations",
            color_continuous_scale=[
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
            ],
            range_color=(minimum, maximum),
        )

    my_hovertemplate = "<b>%{hovertext}<br>AGENCYNAME=%{customdata[2]}</b><br><br>index=%{location}<br>VAL_DIFF=%{customdata[0]}<br>VAL_PERC=%{z}<extra></extra>"
    fig.update_traces(hovertemplate=my_hovertemplate)

    return fig


def create_df_for_scen(
    data_df: pd.DataFrame, geodf: gpd.GeoDataFrame, scenario1: str, scenario2: str
):
    scen_geodf = geodf.copy()
    scen_geodf = scen_geodf.set_index("CONTRACTOR_CONVENTION")

    # Create dataframes with each scenario filtered
    data_df_1 = data_df.loc[data_df["Scenario"] == scenario1]
    data_df_2 = data_df.loc[data_df["Scenario"] == scenario2]

    # Set the index of both dataframes to CONTRACTOR_CONVENTION
    data_df_1 = data_df_1.set_index("CONTRACTOR_CONVENTION")
    data_df_2 = data_df_2.set_index("CONTRACTOR_CONVENTION")

    # Create a column in scen_geodf for the difference of both scenarios' avg annual sum
    scen_geodf["VAL_1"] = data_df_1["VAL"]
    scen_geodf["VAL_2"] = data_df_2["VAL"]
    scen_geodf["VAL_DIFF"] = scen_geodf["VAL_1"] - scen_geodf["VAL_2"]

    # Create a column in scen_geodf for val_diff percentages
    scen_geodf["VAL_PERC"] = (
        ((scen_geodf["VAL_1"] - scen_geodf["VAL_2"]) / scen_geodf["VAL_1"]) * 100
    ).round()

    # If VAL_1 is 0, set VAL_PERC to None
    scen_geodf.loc[scen_geodf["VAL_1"] == 0, "VAL_PERC"] = None

    # create another column in scen_geodf for VAl_DIFF w/ respective signs
    scen_geodf["VAL_DIFF_SIGN"] = scen_geodf["VAL_DIFF"]
    for value in scen_geodf["VAL_DIFF"]:
        if value > 0:
            scen_geodf.loc[scen_geodf["VAL_DIFF"] == value, "VAL_DIFF_SIGN"] = (
                f"+{value}"
            )

    # create an area (in square meters) column and a rank column in the scen geodf
    scen_geodf["area"] = scen_geodf.geometry.area
    scen_geodf["RANK"] = (
        scen_geodf["area"].rank(method="first", ascending=False).astype(int)
    )

    scen_geodf = scen_geodf.reset_index()
    print(f"scen_1 = {scenario1}, scen_2 = {scenario2}")
    print(scen_geodf)

    return scen_geodf


################ DEBUG #############
import plotly.graph_objects as go


def create_fig_1(geodf: gpd.GeoDataFrame):
    fig1 = go.Figure(
        data=go.Scattergeo(
            lon=geodf.geometry.centroid.x,
            lat=geodf.geometry.centroid.y,
            text=geodf["VAL_DIFF_SIGN"],
            mode="text",
            hoverinfo="none",
        )
    )

    fig1.update_geos(fitbounds="locations", visible=False)
    return fig1


####################################


def run_test_app():
    app = Dash(__name__)
    data_df = calc_mean()
    print("data_df:")
    print(data_df)

    scenario_list = data_df["Scenario"].unique()

    geodf = load_shp()
    print("geodf:")
    print(geodf)
    print("geodf.crs:", geodf.crs)

    # Get the figure for the state border
    figca = create_ca_plot()

    app.layout = html.Div(
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

    @callback(
        Output("my_id", "figure"),
        Input("scenario_1", "value"),
        Input("scenario_2", "value"),
    )
    def update_graph(scen1: str, scen2: str):
        scen_geodf = create_df_for_scen(data_df, geodf, scen1, scen2)
        print("scen_geodf:")
        print(scen_geodf)

        fig = create_plot(scen_geodf)

        # Get the figure for the state border
        # figca = create_ca_plot()

        # fig.add_trace(figca.data[0])

        # Add inner figure to the state
        # for i in range(len(fig.data)):
        #    figca.add_trace(fig.data[i])
        # figca.add_trace(fig.data[0])

        ################ DEBUG #############
        fig1 = create_fig_1(scen_geodf)
        # figca.add_trace(fig1.data[0])
        ####################################

        trace1 = figca.data[0]
        trace2 = fig.data[0]
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

        minimum, maximum = get_min_max(scen_geodf)

        layout = go.Layout(
            autosize=False,
            height=1000,
            colorscale={"diverging": mycolor_scale},
            coloraxis={
                "cmin": -50,
                "cmax": 50,
                "cauto": False,
                "autocolorscale": False,
            },
        )
        final_fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
        final_fig.update_geos(fitbounds="locations", visible=False)
        final_fig.update_layout(
            legend_title_text="VAL DIFF %",
        )

        for trace in final_fig.data:
            print(trace.hovertemplate)

        return final_fig

    app.run(debug=True)


if __name__ == "__main__":
    run_test_app()
