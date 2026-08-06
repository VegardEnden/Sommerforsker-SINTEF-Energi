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
plot_reservoir_volumes(name,"Summag","lg",lim=(0,250))




# compare_volumes_mean(name,"CVaR_0.9_50","CVaR_0.9_50old","lg","lg",lim=(40,180))
# compare_volumes_mean(name,"CVaR_0.9_20_66","CVaR_0.9_20_66old","pca","pca",lim=(40,180))
# compare_volumes_mean(name,"CVaR_0.9_20_33","CVaR_0.9_20_33old","pca","pca",lim=(40,180))
# compare_volumes_mean(name,"CVaR_0.9_11","CVaR_0.9_20_532old","lg","lg",lim=(40,180))

# compare_three_means(name,"CVaR_0.9_15","lg", "CVaR_0.9_15_322","pca","CVaR_0.9_15","res",lim=(40,180))
# compare_three_means(name,"CVaR_0.9_50","lg", "CVaR_0.9_50_222","pca","CVaR_0.9_50","res",lim=(40,180))
# compare_four_means(name,"CVaR_0.9_20_322","pca", "CVaR_0.9_20_33","pca","CVaR_0.9_20_222","pca","CVaR_0.9_20_66","pca",lim=(40,180))

# scenario_volumes(name,"CVaR_0.9_50_spill100nape", "lg", lim=(0,250))


# plot_total_overflow(name,"RN","lg",lim=(0,0.025))
# plot_total_overflow(name,"CVar_0.9_20","lg",lim=(0,0.025))
# plot_total_overflow(name,"CVaR_0.9_30","lg",lim=(0,0.025))
# plot_total_overflow(name,"CVaR_0.9_50","lg",lim=(0,0.025))
# plot_total_overflow(name,"Time-dependent","lg",lim=(0,0.025))

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

# rn_flex = flexibility_factor(name,"RN","lg")
# cvar20_flex = flexibility_factor(name,"CVaR_0.9_20","lg")
# cvar50_flex = flexibility_factor(name,"CVaR_0.9_50","lg")
# timedep_flex = flexibility_factor(name,"Time-dependent","lg")



# plt.style.use("seaborn-v0_8-whitegrid")

# x = np.arange(1, 38)

# fig, (ax1, ax2) = plt.subplots(
#     2, 1,
#     figsize=(12, 9),
#     sharex=True,
#     gridspec_kw={"height_ratios": [3, 1]}
# )

# # =========================
# # Hovedplot
# # =========================

# ax1.plot(
#     x, rn_flex,
#     color="black",
#     linewidth=3,
#     label="RN",
#     zorder=5
# )

# ax1.plot(
#     x, cvar20_flex,
#     color="#1f77b4",
#     linestyle="--",
#     marker="o",
#     markersize=4,
#     linewidth=2,
#     label="CVaR 20%"
# )

# ax1.plot(
#     x, cvar50_flex,
#     color="#d62728",
#     linestyle="--",
#     marker="s",
#     markersize=4,
#     linewidth=2,
#     label="CVaR 50%"
# )

# ax1.plot(
#     x, timedep_flex,
#     color="#2ca02c",
#     linestyle="-.",
#     marker="^",
#     markersize=4,
#     linewidth=2,
#     label="Time-dependent CVaR"
# )

# ax1.set_title(
#     "Flexibility Factor for Fjone",
#     fontsize=18,
#     pad=15
# )

# ax1.set_ylabel(
#     "Flexibility factor",
#     fontsize=14
# )

# ax1.legend(
#     fontsize=12,
#     frameon=True,
#     loc="upper right"
# )

# ax1.grid(True, alpha=0.3)

# # =========================
# # Avvik mot RN
# # =========================

# ax2.plot(
#     x,
#     np.array(cvar20_flex) - np.array(rn_flex),
#     color="#1f77b4",
#     linewidth=2,
#     label="CVaR 20% - RN"
# )

# ax2.plot(
#     x,
#     np.array(cvar50_flex) - np.array(rn_flex),
#     color="#d62728",
#     linewidth=2,
#     label="CVaR 50% - RN"
# )

# ax2.plot(
#     x,
#     np.array(timedep_flex) - np.array(rn_flex),
#     color="#2ca02c",
#     linewidth=2,
#     label="TD CVaR - RN"
# )

# ax2.axhline(
#     y=0,
#     color="black",
#     linestyle="-",
#     linewidth=1
# )

# ax2.set_xlabel(
#     "Scenario",
#     fontsize=14
# )

# ax2.set_ylabel(
#     "Δ from RN",
#     fontsize=12
# )

# ax2.grid(True, alpha=0.3)

# # Kun hvert 2. scenario på x-aksen
# ax2.set_xticks(np.arange(1, 38, 2))

# plt.tight_layout()

# path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results\Flexibility_factor.png"

# fig.savefig(
#     path,
#     dpi=300,
#     bbox_inches="tight"
# )


print("All done!")

