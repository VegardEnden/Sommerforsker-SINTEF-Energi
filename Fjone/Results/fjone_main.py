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

# plot_reservoir_volumes(name,"CVaR_0.9_20","lg",lim=(0,250))
# plot_reservoir_volumes(name,"CVaR_0.9_30","lg",lim=(0,250))
# plot_reservoir_volumes(name,"CVaR_0.9_20_spill","lg",lim=(0,250))
# plot_reservoir_volumes(name,"CVaR_0.9_50","lg",lim=(0,250))
# plot_reservoir_volumes(name,"CVaR_0.7_50","lg",lim=(0,250))
# plot_reservoir_volumes(name,"CVaR_0.9_20_322","pca",lim=(0,250))
# plot_reservoir_volumes(name,"CVaR_0.9_20","res",lim=(0,250))
# plot_reservoir_volumes(name,"RN","lg",lim=(0,250))
plot_reservoir_volumes(name,"RN_322","pca",lim=(0,250))
# plot_reservoir_volumes(name,"RN","res",lim=(0,250))

# # plot_bypass(name,"CVaR_0.9_20","lg")
# # plot_bypass(name,"RN","lg")

# plot_total_overflow(name,"CVaR_0.9_50","lg")
# plot_total_overflow(name,"CVaR_0.9_20","lg")
# plot_total_overflow(name,"CVaR_0.7_50","lg")
# plot_total_overflow(name,"RN","lg")

# # plot_production(name,"CVaR_0.9_50","lg")
# # plot_production(name,"RN","lg")



# cvar_20_income = income(name,"CVaR_0.9_20","lg")
# cvar_20pca_income = income(name,"CVaR_0.9_20_322","pca")
# cvar_30_income = income(name,"CVaR_0.9_30","lg")
# cvar_50_income = income(name,"CVaR_0.9_50","lg")
# rn_income = income(name,"RN","lg")

# print("---Comparison Risk-neutral vs CVaR---")

# print("\nAdjusted income with risk-neutral as baseline: ")

# income_df = pd.DataFrame({
#     "Risk-Neutral": [
#         rn_income[0] * 100 / rn_income[0],  
#         rn_income[1] * 100 / rn_income[0],
#     ],
#     "CVaR (0.9,20%)": [
#         cvar_20_income[0] * 100 / rn_income[0],
#         cvar_20_income[1] * 100 / rn_income[0],
#     ],
#     "CVaR (0.9,20%) with PCA": [
#         cvar_20pca_income[0] * 100 / rn_income[0],
#         cvar_20pca_income[1] * 100 / rn_income[0],
#     ],
#     "CVaR (0.9,30%)": [
#         cvar_30_income[0] * 100 / rn_income[0],
#         cvar_30_income[1] * 100 / rn_income[0],

#     ],
#     "CVaR (0.9,50%)": [
#         cvar_50_income[0] * 100 / rn_income[0],
#         cvar_50_income[1] * 100 / rn_income[0],
#     ]
# }, index=[
#     "Average",
#     "Avg 10% worst"
# ])


# print(income_df)

# rn_objective = obj_value(name,"RN","lg")
# cvar20_objective = obj_value(name,"CVaR_0.9_20","lg")
# cvar30_objective = obj_value(name,"CVaR_0.9_30","lg")
# cvar50_objective = obj_value(name,"CVaR_0.9_50","lg")

# print("\nObjective values: ")
# print(f"Risk-Neutral: {rn_objective}")
# print(f"CVaR (0.9,20%): {cvar20_objective}")
# print(f"CVaR (0.9,30%): {cvar30_objective}")
# print(f"CVaR (0.9,50%): {cvar50_objective}")


# cvar_df20 = water_value(name,"CVaR_0.9_20","lg")
# cvar_df20spill = water_value(name,"CVaR_0.9_20_spill","lg")
# cvar_df30 = water_value(name,"CVaR_0.9_30","lg")
# cvar_df50 = water_value(name,"CVaR_0.9_50","lg")
# rn_df = water_value(name,"RN","lg")

# water_vals = pd.concat([rn_df,cvar_df20,cvar_df20spill,cvar_df30,cvar_df50])

# print("\nWater values the first week: ")

# print(water_vals)

# print("\n---Comparison of inflow models---")

# print("\nNegative inflow last backwards iteration: ")

# neginflow_df = pd.concat([neg_inflow(name,"RN","lg"),neg_inflow(name,"RN","pca"),neg_inflow(name,"RN","res")])

# print(neginflow_df)

# neginflow_df = pd.concat([neg_inflow(name,"CVaR_0.9_20","lg"),neg_inflow(name,"CVaR_0.9_20_322","pca"),neg_inflow(name,"CVaR_0.9_20","res")])

# print(neginflow_df)

# print("\nThe following results have used CVaR with 0.9, 20%")

# lg_income = income(name,"CVaR_0.9_20","lg")
# pca_income = income(name,"CVaR_0.9_20","pca")
# res_income = income(name,"CVaR_0.9_20","res")

# print("\nAdjusted income with lognormal as baseline: ")

# income_df = pd.DataFrame({
#     "Lognormal": [
#         lg_income[0] * 100 / lg_income[0],  
#         lg_income[1] * 100 / lg_income[0],
#     ],
#     "PCA": [
#         pca_income[0] * 100 / lg_income[0],
#         pca_income[1] * 100 / lg_income[0],
#     ],
#     "Residual": [
#         res_income[0] * 100 / lg_income[0],
#         res_income[1] * 100 / lg_income[0],
#     ]
# }, index=[
#     "Average",
#     "Avg 10% worst"
# ])


# print(income_df)


# lg_df = water_value(name,"CVaR_0.9_20","lg")
# pca_df = water_value(name,"CVaR_0.9_20","pca")
# res_df = water_value(name,"CVaR_0.9_20","res")

# water_vals = pd.concat([lg_df,pca_df,res_df])

# print("\nWater values the first week: ")

# print(water_vals)

# print("\nThe following results have used Risk-Neutral")

# lg_income = income(name,"RN","lg")
# pca_income = income(name,"RN","pca")
# res_income = income(name,"RN","res")

# print("\nAdjusted income with lognormal as baseline: ")

# income_df = pd.DataFrame({
#     "Lognormal": [
#         lg_income[0] * 100 / lg_income[0],  
#         lg_income[1] * 100 / lg_income[0],
#     ],
#     "PCA": [
#         pca_income[0] * 100 / lg_income[0],
#         pca_income[1] * 100 / lg_income[0],
#     ],
#     "Residual": [
#         res_income[0] * 100 / lg_income[0],
#         res_income[1] * 100 / lg_income[0],
#     ]
# }, index=[
#     "Average",
#     "Avg 10% worst"
# ])


# print(income_df)


# lg_df = water_value(name,"RN","lg")
# pca_df = water_value(name,"RN","pca")
# res_df = water_value(name,"RN","res")

# water_vals = pd.concat([lg_df,pca_df,res_df])

# print("\nWater values the first week: ")

# print(water_vals)




print("All done!")

