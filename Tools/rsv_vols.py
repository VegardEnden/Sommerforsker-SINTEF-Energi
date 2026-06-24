import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

from pyprodrisk import ProdriskSession



def plot_reservoir_volumes(plant_name, method, inflow_model):

    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)
    
    folder = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Simulations", "Finished Runs")

    file = method + "_" + plant_name + "_" + inflow_model

    prodrisk.load_model_yaml(file_path=folder,file_name=file)
    prodrisk.load_data_h5(file_path=folder,file_name=file)

    if plant_name == "Fjone":
        nape_mod = prodrisk.model.module["nape"]
        rolle_mod = prodrisk.model.module["rolleivstadvatn"]
        sand_mod = prodrisk.model.module["sandvatn"]

        nape_vol = nape_mod.reservoirVolume.get()
        rolle_vol = rolle_mod.reservoirVolume.get()
        sand_vol = sand_mod.reservoirVolume.get()

        index = nape_vol.index

        total_vol = nape_vol.values + rolle_vol.values + sand_vol.values

        percs = [0,25,50,75,100]


        plot_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Results"

        # ----- Total Volume fig ----- 
        total_perc = np.percentile(total_vol,percs,axis=1)
        fig_total, ax_total = plt.subplots(figsize=(20,10),sharey=True)

        for p, vals in zip(percs,total_perc):
            ax_total.plot(index, vals, label=f"{p}th percentile")
        ax_total.set(title=method + ", " + inflow_model ,xlabel=r"Volume [Mm$^3$]",ylabel="Time")
        ax_total.legend()


        path_total = os.path.join(plot_folder, "Fjone_total_volume.png")
        fig_total.savefig(path_total, dpi=300, bbox_inches='tight')


        # ----- Nape Volume fig -----
        nape_perc = np.percentile(nape_vol.values,percs,axis=1)
        fig_nape, ax_nape = plt.subplots(figsize=(20,10),sharey=True)
        for p, vals in zip(percs,nape_perc):
            ax_nape.plot(index, vals, label=f"{p}th percentile")
        ax_nape.set(title=method + ", " + inflow_model ,xlabel=r"Volume [Mm$^3$]",ylabel="Time")
        ax_nape.legend()

        path_nape = os.path.join(plot_folder, "Fjone_nape_volume.png")
        fig_nape.savefig(path_nape, dpi=300, bbox_inches='tight')







    return


