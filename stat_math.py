__author__ = "nci*, FlareFlax, veseyh"
__version__ = "0.1"
__copyright__ = "2019, MonoSec Security Solutions"
__status__ = "Prototype"

import numpy as np
import statistics


def calc_volatility(prev_data):
    buffer_data = []
    for i in range(len(prev_data) - 1):
        buffer_data.append((prev_data[i + 1]/prev_data[i]) - 1)
    #print(buffer_data)
    #calculate actual volatility
    std_dev = np.std(buffer_data, ddof=1)
    #annualized volatility
    std_dev_annualized = std_dev * 252
    print("annualized volatility: " + str(std_dev_annualized))
    return std_dev_annualized
