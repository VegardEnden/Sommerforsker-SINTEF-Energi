import pandas as pd
import numpy as np
import time
import h5py
import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from Tools.helpers import *


name = "RjukanPump"


# topology(name)

# plot_reservoir_volumes(name,"RN","lg",lim=(0,2000))

pump_income = income(name,"RN","lg")
nopump_income = income("Rjukan","RN","lg")

income_df = pd.DataFrame({
    "No pump": [
        nopump_income[0] * 100 / nopump_income[0],  
        nopump_income[1] * 100 / nopump_income[0],
    ],
    "Pump": [
        pump_income[0] * 100 / nopump_income[0],
        pump_income[1] * 100 / nopump_income[0],
    
    ],
}, index=[
    "Average",
    "Avg 10% worst"
])


print(income_df)


print("All done!")



