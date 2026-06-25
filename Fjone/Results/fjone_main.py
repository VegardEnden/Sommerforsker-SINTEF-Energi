import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Tools.helpers import *

# topology("Fjone")

# plot_reservoir_volumes("Fjone","CVaR","lg")
# plot_reservoir_volumes("Fjone","RN","lg")

# overflow("Fjone","CVaR","lg")
# overflow("Fjone","RN","lg")

cvar_income = income("Fjone","CVaR_0.9_30","lg")
rn_income = income("Fjone","RN","lg")

income_df = pd.DataFrame({
    "Risk-Neutral": [
        rn_income[0] * 100 / rn_income[0],  
        rn_income[1] * 100 / rn_income[0],
        rn_income[2] * 100 / rn_income[0],
    ],
    "CVaR (0.9,30%)": [
        cvar_income[0] * 100 / rn_income[0],
        cvar_income[1] * 100 / rn_income[0],
        cvar_income[2] * 100 / rn_income[0],
    ]
}, index=[
    "Average income",
    "CVaR 10%",
    "CVaR 20%"
])


print(income_df)

# income("Fjone","CVaR","pca")

# cvar_df = water_value("Fjone","CVaR","lg")
# rn_df = water_value("Fjone","RN","lg")

# water_vals = pd.concat([cvar_df,rn_df])

# print(water_vals)

# neginflow_df = pd.concat([neg_inflow("Fjone","RN","lg"),neg_inflow("Fjone","RN","pca")])

# print(neginflow_df)



print("All done!")

