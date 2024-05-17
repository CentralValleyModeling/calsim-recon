from dash import html, register_page, dash_table  #, callback # If you need callbacks, import it here.
import utils.onepager_api as api

register_page(
    __name__,
    name='One Pager',
    top_nav=True,
    path='/onepager'
)

# Generate historical data

dss_filenames = {
    "hist": "data/2023DCR_Hist_DV.dss"
}

csv_filename = "data\\temp.csv"

# combined_struct = api.read_all_runs_to_structure(dss_filenames)
# table_1 = combined_struct["table_1"]
# study_name = next(iter(table_1))
# table = table_1[study_name]

# data = {}
# data["v0"] = study_name
# data["v1"], data["p1"] = table["Long-term Average"]
# data["v2"], data["p2"] = table["Single Wet Year (1983)"]
# data["v3"], data["p3"] = table["Single Wet Year (1938)"]
# data["v4"], data["p4"] = table["2-Year (1982-1983)"]
# data["v5"], data["p5"] = table["4-Year (1980-1983)"]
# data["v6"], data["p6"] = table["6-Year (1978-1983)"]
# data["v7"], data["p7"] = table["10-Year (1978-1987)"]
# data["v8"], data["p8"] = table["Single Wet Year (1998)"]

combined_struct = api.read_all_runs_to_structure_csv(csv_filename)
data_list = []
for study_name, table in combined_struct.items():
    print(f"{study_name} = {table}")
    data = {}
    data["v0"] = study_name
    data["v1"], data["p1"] = table["Long-term Average"]
    data["v2"], data["p2"] = table["Single Wet Year (1983)"]
    data["v3"], data["p3"] = table["Single Wet Year (1938)"]
    data["v4"], data["p4"] = table["2-Year (1982-1983)"]
    data["v5"], data["p5"] = table["4-Year (1980-1983)"]
    data["v6"], data["p6"] = table["6-Year (1978-1983)"]
    data["v7"], data["p7"] = table["10-Year (1978-1987)"]
    data["v8"], data["p8"] = table["Single Wet Year (1998)"]
    data_list.append(data)

header1 = ("Table 5-4. Estimated Average and Wet-Period Deliveries of SWP Table A Water (Existing Conditions, in taf/year) and Percent of Maximum SWP Table A Amount, 4,133 TAF/year")


def layout():
    layout = dash_table.DataTable(
        columns=[
            {"name": [header1, "Scenario", ""], "id": "v0"},
            {"name": [header1, "Long-term Average", "val"], "id": "v1"},
            {"name": [header1, "Long-term Average", "%"], "id": "p1"},
            {"name": [header1, "Single Wet Year (1983)", "val"], "id": "v2"},
            {"name": [header1, "Single Wet Year (1983)", "%"], "id": "p2"},
            {"name": [header1, "Single Wet Year (1938)", "val"], "id": "v3"},
            {"name": [header1, "Single Wet Year (1938)", "%"], "id": "p3"},
            {"name": [header1, "2-Year (1982-1983)", "val"], "id": "v4"},
            {"name": [header1, "2-Year (1982-1983)", "%"], "id": "p4"},
            {"name": [header1, "4-Year (1980-1983)", "val"], "id": "v5"},
            {"name": [header1, "4-Year (1980-1983)", "%"], "id": "p5"},
            {"name": [header1, "6-Year (1978-1983)", "val"], "id": "v6"},
            {"name": [header1, "6-Year (1978-1983)", "%"], "id": "p6"},
            {"name": [header1, "10-Year (1978-1987)", "val"], "id": "v7"},
            {"name": [header1, "10-Year (1978-1987)", "%"], "id": "p7"},
            {"name": [header1, "Single Wet Year (1998)", "val"], "id": "v8"},
            {"name": [header1, "Single Wet Year (1998)", "%"], "id": "p8"}, 
        ],
        data=data_list,
        merge_duplicate_headers=True,
    )
    return layout
