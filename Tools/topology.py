import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

from pyprodrisk import ProdriskSession

def topology(plant_name):

    prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)
    

    data_path = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, plant_name + " data")

    prodrisk.load_model_yaml(file_path=data_path,file_name=plant_name)
    prodrisk.load_data_h5(file_path=data_path,file_name=plant_name)

    path = os.path.join(r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter", plant_name, "Results",plant_name + "_topology.png")

    prodrisk.plot_topology(path)

    return 