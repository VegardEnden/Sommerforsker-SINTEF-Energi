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

run_session("Svartisen","CVaR_0.9_20_444","pca",nprinc=3, princDisc=[4,4,4],cvar=[0.9,0.2],series=1,loadInflow=True)
