import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pyprodrisk import ProdriskSession

from Tools.helpers import run_session, run_timedependent_session, run_session_old, run_session_summag

# run_session("Fjone","CVaR_0.9_50_222","pca",nprinc=3,princDisc=[2,2,2], cvar=[0.9,0.50],loadInflow=True)

run_session_old("Fjone","CVaR_0.9_50old","lg",cvar=[0.9,0.5],loadInflow=True)

# run_timedependent_session("Fjone","lg",loadInflow=True)

# run_session_summag("Fjone","lg",loadInflow=True,summag=[0.9,2,1],week=[1],min=[0],max=[100])



