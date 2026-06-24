import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Tools.topology import topology
from Tools.rsv_vols import plot_reservoir_volumes

topology("Fjone")

plot_reservoir_volumes("Fjone","CVaR","lg")