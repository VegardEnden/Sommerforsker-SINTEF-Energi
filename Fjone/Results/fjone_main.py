import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Tools.helpers import *


name = "Fjone"

# topology(name)

# plot_reservoir_volumes(name,"CVaR_0.9_20","lg")
# plot_reservoir_volumes(name,"CVaR_0.9_30","lg")
# plot_reservoir_volumes(name,"CVaR_0.9_50","lg")
# plot_reservoir_volumes(name,"CVaR_0.9_20","pca")
# plot_reservoir_volumes(name,"CVaR_0.9_20","res")
# plot_reservoir_volumes(name,"RN","lg")
# plot_reservoir_volumes(name,"RN","pca")
# plot_reservoir_volumes(name,"RN","res")

# plot_inflow(name,"CVaR_0.9_20","lg")
# plot_inflow(name,"RN","lg")



cvar_20_income = income(name,"CVaR_0.9_20","lg")
cvar_50_income = income(name,"CVaR_0.9_50","lg")
rn_income = income(name,"RN","lg")


income_df = pd.DataFrame({
    "Risk-Neutral": [
        rn_income[0] * 100 / rn_income[0],  
        rn_income[1] * 100 / rn_income[1],
    ],
    "CVaR (0.9,20%)": [
        cvar_20_income[0] * 100 / rn_income[0],
        cvar_20_income[1] * 100 / rn_income[1],
    ],
    "CVaR (0.9,50%)": [
        cvar_50_income[0] * 100 / rn_income[0],
        cvar_50_income[1] * 100 / rn_income[1],
    ]
}, index=[
    "Average income",
    "CVaR 10%"
])


print(income_df)

# income(name,"CVaR","pca")

# cvar_df20 = water_value(name,"CVaR_0.9_20","lg")
# cvar_df30 = water_value(name,"CVaR_0.9_30","lg")
# cvar_df50 = water_value(name,"CVaR_0.9_50","lg")
# rn_df = water_value(name,"RN","lg")

# water_vals = pd.concat([rn_df,cvar_df20,cvar_df30,cvar_df50])

# print(water_vals)

# neginflow_df = pd.concat([neg_inflow(name,"RN","lg"),neg_inflow(name,"RN","pca"),neg_inflow(name,"RN","res")])

# print(neginflow_df)



print("All done!")

