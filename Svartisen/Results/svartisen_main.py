import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Tools.helpers import *


name = "Svartisen"

topology(name)

plot_reservoir_volumes(name,"RN","lg")
plot_reservoir_volumes(name,"CVaR_0.9_20","lg")
plot_reservoir_volumes(name,"CVaR_0.9_30","lg")
plot_reservoir_volumes(name,"CVaR_0.9_50","lg")

cvar_20_income = income(name,"CVaR_0.9_20","lg")
cvar_30_income = income(name,"CVaR_0.9_30","lg")
cvar_50_income = income(name,"CVaR_0.9_50","lg")
rn_income = income(name,"RN","lg")

print("---Comparison Risk-neutral vs CVaR---")

print("\nAdjusted income with risk-neutral as baseline: ")

income_df = pd.DataFrame({
    "Risk-Neutral": [
        rn_income[0] * 100 / rn_income[0],  
        rn_income[1] * 100 / rn_income[0],
    ],
    "CVaR (0.9,20%)": [
        cvar_20_income[0] * 100 / rn_income[0],
        cvar_20_income[1] * 100 / rn_income[0],
    ],
    "CVaR (0.9,30%)": [
        cvar_30_income[0] * 100 / rn_income[0],
        cvar_30_income[1] * 100 / rn_income[0],

    ],
    
    "CVaR (0.9,50%)": [
        cvar_50_income[0] * 100 / rn_income[0],
        cvar_50_income[1] * 100 / rn_income[0],
    ]
}, index=[
    "Average",
    "Avg 10% worst"
])


print(income_df)


cvar_df20 = water_value(name,"CVaR_0.9_20","lg")
cvar_df30 = water_value(name,"CVaR_0.9_30","lg")
cvar_df50 = water_value(name,"CVaR_0.9_50","lg")
rn_df = water_value(name,"RN","lg")

water_vals = pd.concat([rn_df,cvar_df20,cvar_df30,cvar_df50])

print("\nWater values the first week: ")

print(water_vals)

print("All done!")