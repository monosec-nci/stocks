import numpy as np


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
