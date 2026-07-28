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

run_session("Fjone","CVaR_0.9_20_66","pca",nprinc=2,princDisc=[6,6], cvar=[0.9,0.20],loadInflow=True)

# run_session_old("Fjone","CVaR_0.9_20_33old","pca",cvar=[0.9,0.2],nprinc=2,princDisc=[3,3],loadInflow=True)

# run_timedependent_session("Fjone","lg",loadInflow=True)

# run_session_summag("Fjone","lg",loadInflow=True,summag=[0.9,2,1],week=[1],min=[0],max=[100])



