import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Tools.helpers import *


name = "Rjukan"

# topology(name)

plot_reservoir_volumes(name,"RN","lg")


print("All done!")