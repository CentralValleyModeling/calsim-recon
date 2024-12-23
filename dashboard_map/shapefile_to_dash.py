import geopandas as gpd
import plotly.express as px
from dash import Dash, dcc, html


def load_shp() -> gpd.GeoDataFrame:
    # from utils.query_data import df_dv, scen_aliases

    # Read shapefile into a pandas dataframe
    return gpd.read_file("SWP_Contractors.shp")


def create_plot(geodf: gpd.GeoDataFrame):
    # geodf.to_crs(pyproj.CRS.from_epsg(4326), inplace=True)
    print(geodf)
    fig = px.choropleth(
        geodf,
        locations=geodf.index,
        color="AGENCYNAME",
        fitbounds="locations",
        featureidkey="properties.district",
    )
    # fig.show()
    return fig


def run_test_app():
    app = Dash(__name__)
    geodf = load_shp()
    fig = create_plot(geodf)
    app.layout = html.Div(
        children=[
            html.H1("Shapefile to Map"),
            dcc.Graph(
                id="my_id",
                figure=fig,
            ),
        ]
    )

    app.run(debug=True)


def test_with_matplotlib():
    import matplotlib.pyplot as plt

    geodf = load_shp()
    geodf.plot()
    plt.show()


if __name__ == "__main__":
    run_test_app()
