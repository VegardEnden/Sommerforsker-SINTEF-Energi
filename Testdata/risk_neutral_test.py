import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

from pyprodrisk import ProdriskSession


prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)

# --- configure settings for the session ---


# simulation period
prodrisk.set_optimization_period(
    pd.Timestamp("2030-01-04"),
    n_weeks=156
)

# time resolution
prodrisk.price_periods = pd.Series(
    index = [prodrisk.start_time + pd.Timedelta(hours=h) for h in 24*np.arange(7)],  # daily resolution
    data=1+np.arange(7)                                                              # 7 periods per week
)

# required file paths
local_dir = os.getcwd()
prodrisk.temp_dir = local_dir                                        # absolute path to make temporary files (here we're using location of this script)
prodrisk.log_file_path = local_dir                                   # absolute path where logfile is created
prodrisk.mpi_path = r"C:\Program Files\Microsoft MPI\bin"            # absolute path to mpi executables
prodrisk.prodrisk_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268777wpdm_prodrisk_cvar_win\prodrisk_cvar_win"     # absolute path to Prodrisk executables
prodrisk.keep_working_directory = False                              # remove temporary files after the simulation

prodrisk.windows_core_delay = 10        # skip unnecessary waiting time
prodrisk.windows_api_delay  = 10        # ditto
prodrisk.max_iterations = 5             # low number for testing only
prodrisk.max_iterations_first_run = 3
prodrisk.use_coin_osi = True            # use open-source LP solver, False to use CPLEX (if you have the license)
prodrisk.command_line_option = "-SEKV"  # command-line options
prodrisk.n_processes = 6                # use multiprocessing, set to 1 without MPI

prodrisk.n_price_levels = 7             # nodes in the price model
prodrisk.inflow_model = 'lognormal'     # use the best inflow model


prodrisk.aggregated_price_period_start_week = 53
prodrisk.sequential_price_period_start_week = 1
prodrisk.sequential_price_period_end_week = 52

# global penalty values
prodrisk.deficit_power_cost = 500.0
prodrisk.surplus_power_cost = 0.02
prodrisk.water_ration_cost = 1300.0

# import 30 inflow scenarios from the sample data file using h5py
# you may use other functions, e.g. from pandas, to load from common formats like csv instead
scendata = h5py.File('ScenarioData.h5','r')
scenarios_1 = {}
scenarios_2 = {}
for y in 1901+np.arange(30):
    scenarios_1[y] = scendata[f'SYSTEM/I-1/{y}'][:7*prodrisk.n_weeks]
    scenarios_2[y] = scendata[f'SYSTEM/I-2/{y}'][:7*prodrisk.n_weeks]

# make pandas-dataframes with time axis relative to the sessions' start time
inflow_df1 = pd.DataFrame(
    index=[prodrisk.start_time + pd.Timedelta(days=i) for i in range(7*prodrisk.n_weeks)],
    data=scenarios_1)

inflow_df2 = pd.DataFrame(
    index=[prodrisk.start_time + pd.Timedelta(days=i) for i in range(7*prodrisk.n_weeks)],
    data=scenarios_2)

scendata.close()

# add 2 inflow series and use the dataframes as scenarios
ser1 = prodrisk.model.inflowSeries.add_object('Serie1')
ser1.seriesId.set(1)
ser1.inflowScenarios.set(inflow_df1)

ser2 = prodrisk.model.inflowSeries.add_object('Serie2')
ser2.seriesId.set(2)
ser2.inflowScenarios.set(inflow_df2)

area = prodrisk.model.area.add_object('price_area')  # there must be exactly one area object in a Prodrisk session

# load prices from a traditional 'prisrekke' file
# the details of this are not important (unfolding the prisrekke-matrix...)
params = np.loadtxt('prisrekke.pri', dtype=int, delimiter=';', skiprows=1, usecols=(0), max_rows=6)
intervals = np.loadtxt('prisrekke.pri', dtype=int, delimiter=';', skiprows=6, max_rows=1, usecols=tuple(1+np.arange(params[5])))
ar_price = np.loadtxt('prisrekke.pri', delimiter=';', skiprows=8, usecols=tuple(2+np.arange(52)))

def prisrekke_to_linear(price_array, n_per, n_scen):
    linear = np.zeros(n_scen*52*n_per)
    for y in range(n_scen):
        year_array = price_array[y*n_per:(y+1)*n_per, :]
        linear[y*n_per*52:(y+1)*n_per*52] = year_array.flatten('F')
    return linear

prices = prisrekke_to_linear(ar_price, params[5], params[4])
intervals = np.tile(intervals,params[3]).cumsum() - intervals[0]
price_df = pd.DataFrame(index=[prodrisk.start_time + pd.Timedelta(hours=h) for h in intervals])
for sc in range(params[4]):
    price_df[f'scen_{sc:02}'] = np.roll(prices.data,-sc*52*params[5])[:params[3]*params[5]]

area.price.set(price_df)  # add the price to the area object


# --- make simple end values ---
refs = []
nPoints = []
x = []
y = []

for i in range(prodrisk.n_price_levels.get()):
    refs.append(i)
    nPoints.append(51)

    for n in range(51):
        x.append(np.real(100 - n * 2))
        y.append(np.real((100.0 + n * 3) * i * 5))


x_values = np.array(x).reshape((prodrisk.n_price_levels.get(), 51))
y_values = np.array(y).reshape((prodrisk.n_price_levels.get(), 51))
area.waterValue.set([
    pd.Series(name=ref, index=x_val, data=y_val) for ref, x_val, y_val in zip(refs, x_values, y_values)
])

mod = prodrisk.model.module.add_object('Lake_High')
mod.name.set('Lake_High')
mod.plantName.set('RPK_plant')
mod.number.set(1001)
mod.ownerShare.set(1.0)
mod.regulationType.set(1)
mod.rsvMax.set(150.0)
mod.connectedSeriesId.set(1)
mod.connected_unreg_series_id.set(2)
mod.meanRegInflow.set(250.0)
mod.meanUnregInflow.set(3.0)
mod.nominalHead.set(438.0)
mod.submersion.set(620.0)
mod.volHeadCurve.set(pd.Series(name=0.0, index=np.array([0.0, 24.7, 50.6, 106.7, 137.1, 150]), data=[1048, 1050, 1052, 1056, 1058, 1060.0]))
p = [3.5,42,81,93,115]
q = [3.0,12,21,24, 30]
enekv = [p_i / q_i for p_i, q_i in zip(p, q)]
mod.PQcurve.set(pd.Series(name=438, index=p, data=q))
mod.energyEquivalentConst.set(max(enekv)/3.6)
mod.maxDischargeConst.set(30.0)
mod.maxProd.set(115)
mod.maxBypassConst.set(30.0)
mod.topology.set([0,0,0])
mod.startVol.set(90.0)


status = prodrisk.run()

rsv_vols = mod.reservoirVolume.get()
inflow = mod.localInflow.get()
production = mod.production.get()
bypass = mod.bypass.get()
discharge = mod.discharge.get()
overflow = mod.overflow.get()