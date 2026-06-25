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

cvar_income = income("Fjone","CVaR","lg")
rn_income = income("Fjone","RN","lg")

df = pd.DataFrame({
    "Risk-Neutral":[rn_income],
    "CVaR (0.9,20%)":[cvar_income]

}, index="Income in 1000EUR")

# income("Fjone","CVaR","pca")

# cvar_df = water_value("Fjone","CVaR","lg")
# rn_df = water_value("Fjone","RN","lg")

# water_vals = pd.concat([cvar_df,rn_df])

# print(water_vals)


print("All done!")

