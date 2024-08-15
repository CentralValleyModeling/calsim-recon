from typing import Callable

import dash_bootstrap_components as dbc
import pandas as pd
from dash import callback_context, dcc, html, no_update
from plotly.graph_objects import Bar, Figure, Scatter

CHART_REGISTRY: dict[str, Callable[[], html.Div]] = {
    # key: value
    # component-id: callable that returns a plotly.graph_objects.Figure
}


def create_download_button(
    registry_id: str,
    chart: html.Div | Figure,
    button_text: str = "Download Data",
) -> dbc.Button:
    btn = dbc.Button(
        button_text,
        id=registry_id,
        rel="noopener",
        target="_blank",
    )
    CHART_REGISTRY[registry_id] = lambda *_: chart

    return btn


def find_figure_in_div(obj: html.Div | Figure) -> Figure | None:
    if isinstance(obj, Figure):
        return obj
    elif isinstance(obj, dcc.Graph):
        if hasattr(obj, "figure"):
            return obj.figure
        else:
            print(obj)
            raise ValueError(obj)
    elif hasattr(obj, "children"):
        for o in obj.children:
            fig = find_figure_in_div(o)
            if fig is not None:
                return fig
    return None  # Nothing found


def _create_dataframe_from_lines(data: Scatter) -> pd.DataFrame:
    df = pd.DataFrame(data={data.name: data.y, "X": data.x})
    return df.set_index("X")


def _create_dataframe_from_bar(data: Bar) -> pd.DataFrame:
    df = pd.DataFrame(data={data.legendgroup: data.y, "X": data.x})
    return df.set_index("X")


def create_dataframe_from_fig(fig: Figure) -> pd.DataFrame:
    frames = list()
    for data in fig.data:
        if isinstance(data, Scatter):
            df = _create_dataframe_from_lines(data)
        elif isinstance(data, Bar):
            df = _create_dataframe_from_bar(data)
        else:
            raise NotImplementedError(f"trace type not supported: {type(data)}")
        frames.append(df)

    return pd.concat(frames, axis=1, join="outer").sort_index()


def universal_data_download(csv_name: str | None = None, *args):
    _id = callback_context.triggered_id
    if _id not in CHART_REGISTRY:
        print(f"Button(id={_id}) is not registered in the CHART_REGISTRY")
        return no_update
    div = CHART_REGISTRY[_id]()
    fig = find_figure_in_div(div)
    if fig is None:
        print(f"Could not find a Figure in {div} for Button(id={_id})")
        return no_update
    df = create_dataframe_from_fig(fig)
    if csv_name is None:
        csv_name = f"{_id}.csv"

    o = dcc.send_data_frame(df.to_csv, csv_name)
    print(o)
    return o
