import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from pyprodrisk import ProdriskSession

from Tools.helpers import run_session

run_session("Fjone","CVaR_0.9_50_spill50","lg",cvar=[0.9,0.5],spillPenalty=50,bypassPenalty=50,loadInflow=True)



