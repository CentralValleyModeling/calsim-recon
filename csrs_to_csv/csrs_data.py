import csrs
import pandas as pd
import yaml


class csrsData:
    def __init__(self, scenario_list, url="https://calsim-scenario-results-server.azurewebsites.net"):
        self.scenario_list = scenario_list
        self.url = url
    
    def csrs_to_csv(self, csv_filename: str, yaml_filename: str) -> None:
        if self.scenario_list is None:
            self.scenario_list = []
    
        # Get an instance of the csrs client
        client = csrs.RemoteClient(self.url)

        # Open the given yaml file for reading
        with open(yaml_filename, 'r') as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)
                return
    
        # Get the bparts from the yaml file
        paths = []

        # Append the bparts from the yaml in the dictioniary data to paths
        for key in data:
            b = data[key]['bpart']
            paths.append(b.lower())

        # Throw an error if there are no paths
        if len(paths) == 0:
            raise ValueError('No bparts in the yaml file.')
        
        # Get all the scenarios if none are given
        scenarios = []
        if not self.scenario_list:
            scenarios = client.get_scenario()
        else:
            for name in self.scenario_list:
                s = client.get_scenario(name=name)
                scenarios.append(s[0])

        ts_list = []
        scen_names = []

        # For each scenario, get the timeseries
        for scenario in scenarios:
            scen_ts_list = []
            for path in paths:
                try:
                    ts = client.get_timeseries(
                        scenario=scenario.name,
                        version=scenario.version,
                        path=path
                    )

                except Exception:
                    ts = None

                if ts is None:
                    idx_1 = []
                    vals = []
                else:
                    idx_1 = pd.to_datetime(ts.dates)
                    n = len(idx_1)
                    if n < 1:
                        continue

                    vals = ts.values
                pd_series = pd.Series(vals, index=idx_1, name=path)
            
                # Combine the duplicate indexes
                pd_series = pd_series.groupby(level=0).mean()
                scen_ts_list.append(pd_series)

            # Concatenate all the timeseries for a scenario column-wise
            df = pd.concat(scen_ts_list, axis=1)
            ts_list.append(df)
            scen_names.append(scenario.name)
    
        # Concatenate a list of timeseries into a dataframe
        df = pd.concat(ts_list, axis=0, keys=scen_names, names=['Scenario'])

        # Make the Scenario index a column
        df = df.reset_index(level='Scenario')

        # Save the dataframe into the given csv file
        df.to_csv(csv_filename, float_format='%.2f')

