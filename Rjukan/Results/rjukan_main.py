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

# plot_reservoir_volumes(name,"RN","lg",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_20","lg",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_20old","lg",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_20_322","pca",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_20_spill20","lg",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_30","lg",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_50_spill100","lg",lim=(0,2000))
# plot_reservoir_volumes(name,"CVaR_0.9_50","lg",lim=(0,2000))
# plot_reservoir_volumes(name, "Time-dependent", "lg", lim=(0,2000),week_marker=[25,50,80,100,135])


# compare_volumes(name,"CVaR_0.9_50_spill100","CVaR_0.9_50","lg","lg")
# compare_volumes_mean(name,"CVaR_0.9_50","CVaR_0.9_50old","lg","lg",lim=(0,2000))
# compare_volumes_mean(name,"CVaR_0.9_20","CVaR_0.9_20old","lg","lg",lim=(0,2000))

# scenario_volumes(name, "RN", "lg", lim=(0,2000))
# scenario_volumes(name, "CVaR_0.9_20", "lg", lim=(0,2000))
# scenario_volumes(name, "CVaR_0.9_50", "lg", lim=(0,2000))
# scenario_volumes(name, "Time-dependent", "lg", lim=(0,2000))

# plot_total_overflow(name,"CVaR_0.9_50","lg",lim=(0,40))
# plot_total_overflow(name,"CVaR_0.9_20_spill50","lg",lim=(0,40))
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
#     "CVaR (0.9,20%) old": [
#             cvar_20old_income[0] * 100 / rn_income[0],
#             cvar_20old_income[1] * 100 / rn_income[0],
#         ],
#     "CVaR (0.9,30%)": [
#         cvar_30_income[0] * 100 / rn_income[0],
#         cvar_30_income[1] * 100 / rn_income[0],
#     ],
#     "CVaR (0.9,50%)": [
#         cvar_50_income[0] * 100 / rn_income[0],
#         cvar_50_income[1] * 100 / rn_income[0],
#     ],
#     # "CVaR (0.9,50%) with spill penalty": [
#     #     cvar_50spill_income[0] * 100 / rn_income[0],
#     #     cvar_50spill_income[1] * 100 / rn_income[0],
#     # ],
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

rn_flex = flexibility_factor(name,"RN","lg")
cvar20_flex = flexibility_factor(name,"CVaR_0.9_20","lg")
cvar50_flex = flexibility_factor(name,"CVaR_0.9_50","lg")
timedep_flex = flexibility_factor(name,"Time-dependent","lg")

fig, ax = plt.subplots(figsize=(10,10))

x = np.linspace(1,30,30)

ax.plot(x,rn_flex,label="RN")
ax.plot(x,cvar20_flex,label="CVaR 20%")
ax.plot(x,cvar50_flex,label="CVaR 50%")
ax.plot(x,timedep_flex,label="Time-dependent CVaR")

ax.legend()

plt.show()

print("All done!")
