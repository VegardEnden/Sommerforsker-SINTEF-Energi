import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pyprodrisk import ProdriskSession
from helpers import build_prodrisk_model

folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Svartisen\Svartisen data\\"

prdrisk_cvar = build_prodrisk_model(folder)

prdrisk_cvar.cvar = 0.9
prdrisk_cvar.cvar_weight = 0.2

status = prdrisk_cvar.run()


# area_name = prdrisk_cvar.model.area.get_object_names()[0]
# area_cvar = prdrisk_cvar.model.area[area_name]

# price = area_cvar.price.get()

# print("Price scenarios:", price.shape[1])

# # Check inflow
# modules = prdrisk_cvar.model.module.get_object_names()
# mod0 = prdrisk_cvar.model.module[modules[0]]

# inflow = mod0.localInflow.get()
# print("Inflow scenarios:", inflow.shape[1])


