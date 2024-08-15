import sys
import geopandas as gpd
import plotly.express as px
from dash import Dash, dcc, html
import json
import pyproj
import plotly.figure_factory as ff
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
    "SWP_TA_SCV": "SWC_SCVWD",  # newly added
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
        columns=["Scenario", "CONTRACTOR_CONVENTION", "iwy", "VAL"]
    )

    for code in swp2convention:
        # Create a dataframe using the Scenario and code from df_dv
        df = qd.df_dv[["Scenario", "iwy", code, "cfs_taf"]].copy()

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
        ["Scenario", "CONTRACTOR_CONVENTION", "iwy"]
    ).sum()

    # Remove iwy column
    combined_df = combined_df.reset_index()
    combined_df = combined_df.drop(columns=["iwy"])

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
    )

    figca.update_layout(colorscale_sequential=px.colors.sequential.Blues)
    # figca.update_layout(colorscale_sequentialminus="Reds")

    figca.update_layout(showlegend=True)

    return figca


def create_plot(geodf: gpd.GeoDataFrame):
    geodf.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    fig = px.choropleth(
        geodf,
        geojson=geodf.geometry,
        locations="OBJECTID",
        hover_data={"VAL_DIFF": True, "OBJECTID": False},
        hover_name="CONTRACTOR_CONVENTION",
        color="VAL_DIFF",
        basemap_visible=False,
        fitbounds="locations",
    )

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
    scen_geodf = scen_geodf.reset_index()
    # scen_geodf = scen_geodf.dropna()

    return scen_geodf


def run_test_app():
    app = Dash(__name__)
    data_df = calc_mean()
    print("data_df:")
    print(data_df)

    geodf = load_shp()
    print("geodf:")
    print(geodf)

    scen1 = "DCR_21_Hist"
    scen2 = "DCR_23_Hist"
    scen_geodf = create_df_for_scen(data_df, geodf, scen1, scen2)
    print("scen_geodf:")
    print(scen_geodf)

    fig = create_plot(scen_geodf)

    # Get the figure for the state border
    figca = create_ca_plot()

    # Add inner figure to the state
    for i in range(len(fig.data)):
        figca.add_trace(fig.data[i])

    app.layout = html.Div(
        children=[
            html.H1("Shapefile to Map"),
            dcc.Graph(
                id="my_id",
                figure=figca,
            ),
        ]
    )

    app.run(debug=True)


if __name__ == "__main__":
    run_test_app()
