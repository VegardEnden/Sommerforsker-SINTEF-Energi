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

# run_session("Svartisen","CVaR_0.9_50_10","lg",series=1,cvar=[0.9,0.50],nprinc=1,princDisc=[10])

# run_session_old("Svartisen","CVaR_0.9_50_10old","lg",series=1,cvar=[0.9,0.50],nprinc=1,princDisc=[10])

run_session_summag("Svartisen","pca",summag=[0.9,2,0],week=[20,40,51],min=[20,10,20],max=[90,100,90])

