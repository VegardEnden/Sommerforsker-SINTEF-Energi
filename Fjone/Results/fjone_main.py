import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Tools.helpers import *

# topology("Fjone")

# plot_reservoir_volumes("Fjone","CVaR","lg")
# plot_reservoir_volumes("Fjone","RN","lg")

# overflow("Fjone","CVaR","lg")
# overflow("Fjone","RN","lg")

income("Fjone","CVaR","lg")
income("Fjone","RN","lg")