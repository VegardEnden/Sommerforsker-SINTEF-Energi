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

# topology(name)

# plot_reservoir_volumes_series(name,"RN","lg",(0,3500))
# plot_reservoir_volumes_series(name,"CVaR_0.9_20","lg",(0,3500))
# plot_reservoir_volumes_series(name,"CVaR_0.9_30","lg",(0,3500))
# plot_reservoir_volumes_series(name,"CVaR_0.9_50","lg",(0,3500))
# plot_reservoir_volumes_series(name,"RN_322","pca",(0,3500))
# plot_reservoir_volumes_series(name,"CVaR_0.9_20_444","pca",(0,3500))

# cvar_20_income = income_serial(name,"CVaR_0.9_20","lg")
# cvar_30_income = income_serial(name,"CVaR_0.9_30","lg")
# cvar_50_income = income_serial(name,"CVaR_0.9_50","lg")
# rn_income = income_serial(name,"RN","lg")

# print("---Comparison Risk-neutral vs CVaR---")

# print("\nAdjusted income with risk-neutral as baseline: ")

# income_df = pd.DataFrame({
#     "Risk-Neutral": [
#         rn_income * 100 / rn_income,  
#     ],
#     "CVaR (0.9,20%)": [
#         cvar_20_income * 100 / rn_income,
#     ],
#     "CVaR (0.9,30%)": [
#         cvar_30_income * 100 / rn_income,

#     ],
    
#     "CVaR (0.9,50%)": [
#         cvar_50_income * 100 / rn_income,
#     ]
# }, index=[
#     "Average"
# ])


# print(income_df)

# rn_obj = obj_value(name,"RN","lg")
# cvar_20_obj = obj_value(name,"CVaR_0.9_20","lg")
# cvar_30_obj = obj_value(name,"CVaR_0.9_30","lg")
# cvar_50_obj = obj_value(name,"CVaR_0.9_50","lg")

# obj_df = pd.DataFrame({
#     "Risk-Neutral": [
#         rn_obj * 100 / rn_obj,  
#     ],
#     "CVaR (0.9,20%)": [
#         cvar_20_obj * 100 / rn_obj,
#     ],
#     "CVaR (0.9,30%)": [
#         cvar_30_obj * 100 / rn_obj,

#     ],
    
#     "CVaR (0.9,50%)": [
#         cvar_50_obj * 100 / rn_obj,
#     ]
# }, index=[
#     "Expected Objective Value"
# ])

# print("\nExpected objective value: ")
# print(obj_df)



cvar_df20 = water_value(name,"CVaR_0.9_20","lg")
cvar_df30 = water_value(name,"CVaR_0.9_30","lg")
cvar_df50 = water_value(name,"CVaR_0.9_50","lg")
rn_df = water_value(name,"RN","lg")

water_vals = pd.concat([rn_df,cvar_df20,cvar_df30,cvar_df50])

print("\nWater values the first week: ")

print(water_vals)

print("All done!")