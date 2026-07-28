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




# compare_volumes_mean(name,"CVaR_0.9_20","CVaR_0.9_20old","lg","lg",lim=(40,160))
# compare_volumes_mean(name,"CVaR_0.9_15_4333","CVaR_0.9_20_4333old","pca","pca",lim=(40,180))
# compare_volumes_mean(name,"CVaR_0.9_20_33","CVaR_0.9_20_33old","pca","pca",lim=(40,180))
# compare_volumes_mean(name,"CVaR_0.9_20","CVaR_0.9_20old","res","res",lim=(40,160))

# compare_three_means(name,"CVaR_0.9_20_322old","pca", "CVaR_0.9_20_33old","pca","CVaR_0.9_20_222old","pca",lim=(40,180))
# compare_four_means(name,"CVaR_0.9_20_322","pca", "CVaR_0.9_20_33","pca","CVaR_0.9_20_222","pca","CVaR_0.9_20_4333","pca",lim=(40,180))

# scenario_volumes(name,"CVaR_0.9_50_spill100nape", "lg", lim=(0,250))


# cvar_20_income = income(name,"CVaR_0.9_20","lg")
# cvar_20pcaincome = income(name,"CVaR_0.9_20_322","pca")
# timedep_income = income(name,"Time-dependent","lg")
# cvar_50spillnape_income = income(name,"CVaR_0.9_50_spill100nape","lg")
# cvar_50_income = income(name,"CVaR_0.9_50","lg")
# rn_income = income(name,"RN","lg")
# summag_income = income(name,"Summag","lg")

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
#     "CVaR time-dependent": [
#         timedep_income[0] * 100 / rn_income[0],
#         timedep_income[1] * 100 / rn_income[0],
#     ],
    
#     "Summag": [
#         summag_income[0] * 100 / rn_income[0],
#         summag_income[1] * 100 / rn_income[0],

#     ],
#     "CVaR (0.9,50%)": [
#         cvar_50_income[0] * 100 / rn_income[0],
#         cvar_50_income[1] * 100 / rn_income[0],
#     ],
    
#     "CVaR (0.9,50%) spill on nape": [
#         cvar_50spillnape_income[0] * 100 / rn_income[0],
#         cvar_50spillnape_income[1] * 100 / rn_income[0],
#     ]
# }, index=[
#     "Average",
#     "Avg 10% worst"
# ])


# print(income_df)

# rn_objective = obj_value(name,"RN","lg")
# cvar20_objective = obj_value(name,"CVaR_0.9_20","lg")
# cvar50spill_objective = obj_value(name,"CVaR_0.9_50_spill50","lg")
# cvar30_objective = obj_value(name,"CVaR_0.9_30","lg")
# cvar50_objective = obj_value(name,"CVaR_0.9_50","lg")

# print("\nObjective values: ")
# print(f"Risk-Neutral: {rn_objective}")
# print(f"CVaR (0.9,20%): {cvar20_objective}")
# print(f"CVaR (0.9,30%): {cvar30_objective}")
# print(f"CVaR (0.9,50%): {cvar50_objective}")
# print(f"CVaR (0.9,50% with spill): {cvar50spill_objective}")


# cvar_df20 = water_value(name,"CVaR_0.9_20","lg")
# cvar_df50spill = water_value(name,"CVaR_0.9_50_spill100nape","lg")
# cvar_df30 = water_value(name,"CVaR_0.9_30","lg")
# cvar_df50 = water_value(name,"CVaR_0.9_50","lg")
# rn_df = water_value(name,"RN","lg")
# timedep_df = water_value(name, "Time-dependent","lg")

# water_vals = pd.concat([rn_df, cvar_df20,timedep_df, cvar_df30,cvar_df50,cvar_df50spill])

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

