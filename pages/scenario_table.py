# from csrs import Scenario
import dash_bootstrap_components as dbc
from dash import Input, Output, callback, dash_table, dcc, html, register_page

# from .client import client


# register_page(
#    __name__,
#    name='Scenario Table',
#    top_nav=True,
#    path='/scenario_table'
# )

TABLE_CELL_STYLE = {
    "minWidth": "3rem",
    "width": "50%",
    "maxWidth": "15rem",
    "textAlign": "left",
}

TABLE_STYLE = {
    "overflowX": "auto",
}


WIDGET_STYLE = {
    "margin-left": "1rem",
    "margin-right": "1rem",
    "padding": "1rem 1rem",
    "backgroundColor": "light grey",
}


def layout(**kwargs):
    return dbc.Container(
        class_name="my-3",
        id="scenario-list",
        children=[dcc.Markdown("Placeholder for csrs stuff")],
    )


# class ScenarioTableWidget(html.Div):
#    def __init__(self, scenarios: list[Scenario], *args, **kwargs):
#        kwargs["id"] = kwargs.get("id", "widget-scenario-table")
#        kwargs["style"] = kwargs.get("style", WIDGET_STYLE)
#        super().__init__(*args, **kwargs)
#        self.scenarios = scenarios
#
#        attrs_data = [scenario.model_dump() for scenario in self.scenarios]
#
#        attrs = html.Div(
#            [
#                dash_table.DataTable(
#                    attrs_data,
#                    style_table=TABLE_STYLE,
#                    style_cell=TABLE_CELL_STYLE,
#                    id="scenario-table-object",
#                )
#            ],
#            style={"margin": "1rem"},
#        )
#
#        # Create the internal layout
#        self.children = [
#            html.H2(
#                "Compare Scenario Assumptions",
#                className="card-title",
#            ),
#            attrs,
#        ]
#
#
# def layout(**kwargs):
#    return html.Div(
#        id="scenario-list",
#        children=[
#            ScenarioTableWidget(client.get_scenario()),
#            html.Div(id="assumption-focus"),
#        ],
#    )
