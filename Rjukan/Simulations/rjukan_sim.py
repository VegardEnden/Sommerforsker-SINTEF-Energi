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

run_session("Rjukan","summag","lg",summag=[0.9,2.0,1],week=[1],min=[0],max=[100],series=1,loadInflow=True)