

import csrs
import pandas as pd
import csv

def csrs_to_one_pager_csv():
    url = "https://calsim-scenario-results-server.azurewebsites.net"
    csv_filename = "csrs_data.csv"

    client = csrs.RemoteClient(url)

    # date range we are interested in
    start = pd.to_datetime("1921-10-01")
    # end = pd.to_datetime("2021-09-30")

    # path names we are interested in
    path_swp_names = [
        "SWP_TA_TOTAL", 
        "SWP_CO_TOTAL", 
        "SWP_TA_FEATH", 
        "SWP_CO_FEATH"
        ]

    # Get all the scenarios
    scenario_list = client.get_scenario()
    print(scenario_list)
    with open(csv_filename, 'w', newline='') as csv_file:
        field_names = ["", "Scenario", "SWP_TA_TOTAL", "SWP_CO_TOTAL", "SWP_TA_FEATH", "SWP_CO_FEATH"]
        csv_writer = csv.writer(csv_file, delimiter=",")
        csv_writer.writerow(field_names)

        for scen in scenario_list:
            # print(scen.name)
            # print(scen.version)

            # Get data for swp_ta_total
            ts1 = client.get_timeseries(
                scenario=scen.name,
                version=scen.version,
                path="swp_ta_total",
            )

            # Get data for swp_co_total
            ts2 = client.get_timeseries(
                scenario=scen.name,
                version=scen.version,
                path="swp_co_total",
            )

            # Get data for swp_ta_feath
            ts3 = client.get_timeseries(
                scenario=scen.name,
                version=scen.version,
                path="swp_ta_feath",
            )

            # Get data for swp_co_feath
            ts4 = client.get_timeseries(
                scenario=scen.name,
                version=scen.version,
                path="swp_co_feath",
            )

            # Iterate over the timeseries to create the rows
            # and to add to the csv file
            my_time = start
            for ta_total, ta_feath, co_total, co_feath in zip(ts1.values, ts2.values, ts3.values, ts4.values):
                csv_writer.writerow([my_time, scen.name, ta_total, ta_feath, co_total, co_feath])
                my_time = my_time + pd.DateOffset(months=1)


def csrs_to_csv(csv_filename: str, scenario_names: list[str] = [], path_names: list[str] = [], url="https://calsim-scenario-results-server.azurewebsites.net") -> None:
    # Get an instance of the CSRS client
    client = csrs.RemoteClient(url)

    # Get all scenarios if none are given
    scenarios = []
    if not scenario_names:
        scenarios = client.get_scenario()
    else:
        for name in scenario_names:
            s = client.get_scenario(name=name)
            scenarios.append(s[0])
    
    paths = []
    if not path_names:
        paths = client.get_path()
    else:
        for name in path_names:
            p = client.get_path(name=name)
            paths.append(p[0])

    # Variable to hold all the timeseries
    ts_list = [] 

    # Variable to hold scenario names
    scen_names = []

    # For each scenario, get the timeseries
    for scenario in scenarios:
        print(f"Scenario: '{scenario.name}'")
        scen_ts_list = []
        for path in paths:
            #print(f"    Path: '{path}'")
            ts = client.get_timeseries(
                scenario=scenario.name,
                version=scenario.version,
                path=path.name
            )
            idx_1 = pd.to_datetime(ts.dates)
            n = len(idx_1)
            if n < 1:
                continue

            vals = ts.values
            pd_series = pd.Series(vals, index=idx_1, name=path.name)
            
            # Combine the duplicate indexes
            pd_series = pd_series.groupby(level=0).mean()

            scen_ts_list.append(pd_series)
        
        # Concatenate all timeseries for a scenario column-wise
        print("    concatenating scen_ts_list")
        df = pd.concat(scen_ts_list, axis=1)
        ts_list.append(df)
        scen_names.append(scenario.name)
    
    # Concatenate a list of timeseries into a dataframe
    print("concatenating ts_list")
    df = pd.concat(ts_list, axis=0, keys=scen_names, names=['Scenario'])

    # Make Scenario index a column
    df = df.reset_index(level='Scenario')

    # Save the dataframe into the given csv file
    df.to_csv(csv_filename, float_format='%.2f')


# csrs_to_csv("az_onepager.csv", path_names=["swp_ta_total", "swp_co_total", "swp_ta_feath", "swp_co_feath"])

csrs_to_csv("az_onepager_1.csv", scenario_names=['Adjusted Historical (Danube)'], path_names=["swp_ta_total", "swp_co_total", "swp_ta_feath", "swp_co_feath"])

#csrs_to_csv("az_data.csv")


# print(timeseries.values)



# r = requests.get('https://calsim-scenario-results-server.azurewebsites.net/timeseries?scenario=Historical%20%28Danube%29&version=1.1&path=cvp_allocation_nod_ag')
# print(r.status_code)

# https://calsim-scenario-results-server.azurewebsites.net/timeseries?scenario=Historical%20(Danube)&version=1.1&path=cvp_allocation_nod_ag

