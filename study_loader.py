from collections import namedtuple

import pandas as pd
import yaml

from utils.tools import load_data_mult

# Scenario management
Scenario = namedtuple("Scenario", ["pathname", "alias", "active"])
with open("constants/dvars.yaml", "r") as file:
    var_dict = yaml.safe_load(file)

# s1 = Scenario('dss_files/DCRBL_DV_6.68.dss', 'DCR_21_Hist',1)
# s2 = Scenario('dss_files/DCR2023_DV_9.0.0_Danube_Adj_v1.2.dss', 'DCR_23_Adj',1)
# s3 = Scenario('dss_files/DCR2023_DV_9.0.0_Danube_CC50_v1.2.1.dss', 'DCR_23_CC50',1)
# s4 = Scenario('dss_files/DCR2023_DV_9.0.0_Danube_CC75_v1.2.1.dss', 'DCR_23_CC75',1)
# s5 = Scenario('dss_files/DCR2023_DV_9.0.0_Danube_CC95_v1.2.1.dss', 'DCR_23_CC95',1)
# s6 = Scenario('dss_files/DCR2023_DV_9.0.0_Danube_Hist_v1.1.dss', 'DCR_23_Hist',1)


# s1 = Scenario('dss_files/CS3L2020SV_SJWadj_LYRA.dss', 'DCR_21_Hist',1)
# s2 = Scenario('dss_files/DCR2023_SV_Danube_Adj_v1.2.dss', 'DCR_23_Adj',1)
# s3 = Scenario('dss_files/DCR2023_SV_Danube_cc50_v1.2.1.dss', 'DCR_23_CC50',1)
# s4 = Scenario('dss_files/DCR2023_SV_Danube_cc75_v1.2.1.dss', 'DCR_23_CC75',1)
# s5 = Scenario('dss_files/DCR2023_SV_Danube_cc95_v1.2.1.dss', 'DCR_23_CC95',1)
# s6 = Scenario('dss_files/DCR2023_SV_Danube_Hist_v1.1.dss', 'DCR_23_Hist',1)

s1 = Scenario("dss_files/DCRBL_DV_6.68.dss", "DCR_21_Hist", 1)
s2 = Scenario("dss_files/DCR2023_DV_9.3.1_v2a_Danube_Adj_v1.8.dss", "DCR_23_Adj", 1)
s3 = Scenario("dss_files/DCR2023_DV_9.3.1_Danube_cc50_v1.8.dss", "DCR_23_CC50", 1)
s4 = Scenario("dss_files/DCR2023_DV_9.3.1_Danube_CC75_v1.8.dss", "DCR_23_CC75", 1)
s5 = Scenario("dss_files/DCR2023_DV_9.3.1_Danube_CC95_v1.8.dss", "DCR_23_CC95", 1)
s6 = Scenario("dss_files/DCR2023_DV_9.3.1_Danube_Hist_v1.7.dss", "DCR_23_Hist", 1)

date_map = pd.read_csv("constants/date_map.csv", index_col=0, parse_dates=True)

scenarios = (scenario for scenario in [s1, s2, s3, s4, s5, s6] if scenario.active == 1)

scen_dict = {}
for s in scenarios:
    if s.active == 1:
        scen_dict[s.alias] = s.pathname

load_data_mult(scen_dict, var_dict, date_map)
