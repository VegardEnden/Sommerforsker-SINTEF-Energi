import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pyprodrisk import ProdriskSession
from Tools.helpers import build_prodrisk_model


prodrisk = ProdriskSession(license_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk license", # absolute path to license file
                           solver_path=r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268775wpdm_prapi_cvar_win\prapi_cvar_win\6.0.1_2026-06-12_020b04dce\Prodrisk_API_6.0.1_2026-06-12_020b04dce\pyprodrisk", # absolute path to pyprodrisk binaries
                           silent=False,        # write console output
                           sim_id=None)         # use default session id (a timestamp)

local_dir = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Fjone data"

prodrisk.load_model_yaml(file_path=local_dir,file_name="Fjone.yaml",)
prodrisk.load_data_h5(file_path=local_dir,file_name="Fjone.h5")

prodrisk.temp_dir = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\tempdata"
prodrisk.log_file_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Logfiles"
prodrisk.mpi_path = r"C:\Program Files\Microsoft MPI\bin"            # absolute path to mpi executables
prodrisk.prodrisk_path = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prodrisk-CVar-and-Summag-prototype-5825\1781268777wpdm_prodrisk_cvar_win\prodrisk_cvar_win"     # absolute path to Prodrisk executables
prodrisk.keep_working_directory = False                              # remove temporary files after the simulation

prodrisk.inflow_model = "principal"

prodrisk.cvar = 0.9
prodrisk.cvar_weight = 0.2

status = prodrisk.run()

run_folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Simulations\Finished Runs"

prodrisk.dump_model_yaml(file_path=run_folder,file_name="CVaR_Fjone_pca",direction="both")
prodrisk.dump_data_h5(file_path=run_folder,file_name="CVaR_Fjone_pca",direction="both")


