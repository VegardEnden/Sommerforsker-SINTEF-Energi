import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Tools.helpers import *


name = "Rjukan"

# topology(name)

# plot_reservoir_volumes(name,"RN","lg",lim=(0,2000),title="Risk-Neutral")
# plot_reservoir_volumes(name,"CVaR_0.9_20","lg",lim=(0,2000),title="CVaR with 20% weight")
# plot_reservoir_volumes(name,"CVaR_0.9_30","lg",lim=(0,2000),title="CVaR with 30% weight")
# plot_reservoir_volumes(name,"CVaR_0.9_20_322","pca",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_20_spill20","lg",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_30","lg",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_50_spill100","lg",lim=(0,2000),title="CVaR with 50% weight and spill penalty")
# plot_reservoir_volumes(name,"CVaR_0.9_50","lg",lim=(0,2000),title="CVaR with 50% weight")
# plot_reservoir_volumes(name, "Time-dependent", "lg", lim=(0,2000),week_marker=[25,50,80,100,135],title="Time-dependent CVaR")

# reservoir_energy(name,"RN","lg",lim=(0,4000))


compare_volumes_mean(name,"CVaR_0.9_20","CVaR_0.9_20old","lg","lg",lim=(0,2000),title="CVaR comparison with same 20% weight")
compare_volumes_mean(name,"CVaR_0.9_50","CVaR_0.9_50old","lg","lg",lim=(0,2000),title="CVaR comparison with same 50% weight")


# scenario_volumes(name, "RN", "lg", lim=(0,2000))
# scenario_volumes(name, "CVaR_0.9_20", "lg", lim=(0,2000))
# scenario_volumes(name, "CVaR_0.9_50", "lg", lim=(0,2000))
# scenario_volumes(name, "Time-dependent", "lg", lim=(0,2000))

# plot_total_overflow(name,"CVaR_0.9_50_spill100","lg",lim=(0,40))
# plot_total_overflow(name,"CVaR_0.9_30","lg",lim=(0,40))
# plot_total_overflow(name,"CVaR_0.9_50_spill100Froeystul","lg",lim=(0,40))
# plot_total_overflow(name,"CVaR_0.9_20","lg",lim=(0,40))
# plot_total_overflow(name,"RN","lg",lim=(0,40))
# plot_total_overflow(name,"Time-dependent","lg",lim=(0,40))

# cvar_20_income = income(name,"CVaR_0.9_20","lg")
# cvar_20old_income = income(name,"CVaR_0.9_20old","lg")
# cvar_30_income = income(name,"CVaR_0.9_30","lg")
# cvar_50_income = income(name,"CVaR_0.9_50","lg")
# cvar_50spill_income = income(name,"CVaR_0.9_50_spill100","lg")
# rn_income = income(name,"RN","lg")
# timedep_income = income(name, "Time-dependent", "lg")

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

#     "CVaR (0.9,30%)": [
#         cvar_30_income[0] * 100 / rn_income[0],
#         cvar_30_income[1] * 100 / rn_income[0],
#     ],
#     "CVaR (0.9,50%)": [
#         cvar_50_income[0] * 100 / rn_income[0],
#         cvar_50_income[1] * 100 / rn_income[0],
#     ],
#     "CVaR (0.9,50%) with spill penalty": [
#         cvar_50spill_income[0] * 100 / rn_income[0],
#         cvar_50spill_income[1] * 100 / rn_income[0],
#     ],
#     "Time-dependent CVaR": [
#         timedep_income[0] * 100 / rn_income[0],
#         timedep_income[1] * 100 / rn_income[0],
#     ],
# }, index=[
#     "Average",
#     "Avg 10% worst"
# ])


# print(income_df)

# cvar_df20 = water_value(name,"CVaR_0.9_20","lg")
# cvar_df30 = water_value(name,"CVaR_0.9_30","lg")
# cvar_df50 = water_value(name,"CVaR_0.9_50","lg")
# cvar_df50spill = water_value(name,"CVaR_0.9_50_spill100","lg")
# rn_df = water_value(name,"RN","lg")
# timedep_df = water_value(name, "Time-dependent", "lg")

# water_vals = pd.concat([rn_df,cvar_df20,cvar_df30,cvar_df50,cvar_df50spill,timedep_df])

# print("\nWater values the first week: ")

# print(water_vals)

# rn_flex = flexibility_factor(name,"RN","lg")
# cvar20_flex = flexibility_factor(name,"CVaR_0.9_20","lg")
# cvar50_flex = flexibility_factor(name,"CVaR_0.9_50","lg")
# timedep_flex = flexibility_factor(name,"Time-dependent","lg")

# plt.style.use("seaborn-v0_8-whitegrid")

# x = np.arange(1, 31)

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
#     "Flexibility Factor for Rjukan",
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
# ax2.set_xticks(np.arange(1, 31, 2))

# plt.tight_layout()

# path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Rjukan\Results\Flexibility_factor.png"

# fig.savefig(
#     path,
#     dpi=300,
#     bbox_inches="tight"
# )

print("All done!")
