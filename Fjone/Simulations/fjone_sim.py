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

# run_session("Fjone","CVaR_0.9_50_66","pca",nprinc=2,princDisc=[6,6],cvar=[0.9,0.50])

# run_session_old("Fjone","CVaR_0.9_20_532old","lg",cvar=[0.9,0.2],nprinc=3,princDisc=[5,3,2])

# run_timedependent_session("Fjone","lg",loadInflow=True)

run_session_summag("Fjone","lg",summag=[5,10,0],week=[243],min=[0],max=[100])



