import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pyprodrisk import ProdriskSession

from Tools.helpers import run_session, run_timedependent_session, run_session_old

run_session("Rjukan","RN_cap","lg",loadInflow=True,hardCap=True)

# run_timedependent_session("Rjukan","lg",loadInflow=True)

# run_session_old("Rjukan", "CVaR_0.9_20old","lg",cvar=[0.9,0.2],loadInflow=True)