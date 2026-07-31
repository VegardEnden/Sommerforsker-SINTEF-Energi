import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pyprodrisk import ProdriskSession

from Tools.helpers import run_session, run_session_summag, run_session_old

run_session("Svartisen","CVaR_0.9_30","lg",series=1,cvar=[0.9,0.30],loadInflow=True)

# run_session_old("Svartisen","CVaR_0.9_50old","lg",series=1,cvar=[0.9,0.50],loadInflow=True)


