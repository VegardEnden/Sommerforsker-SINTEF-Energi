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

folder = r"C:\Users\vegarden\OneDrive - SINTEF\Dokumenter\Prosjekter\Fjone\Fjone data\\"

prdrisk_riskneutral = build_prodrisk_model(folder)

status = prdrisk_riskneutral.run()