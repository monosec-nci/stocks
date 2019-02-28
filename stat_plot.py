__author__ = "nci*, FlareFlax, veseyh"
__version__ = "0.1"
__copyright__ = "2019, MonoSec Security Solutions"
__status__ = "Prototype"


from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import get_historical_intraday
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import statistics

end = datetime.now()
start = datetime(end.year, end.month, end.day - 14)

def find_bollinger_bands(prev_data):
    print(prev_data)
    prev_data =
    ret_data = []
    buffer_data = []
    bollinger_data = []
    lower_val = 0
    high_val = 0
    average = 0
    for i in prev_data:
        average += i
    average = average / len(prev_data)

    for i in range(len(prev_data)-1):
        buffer_data.append((prev_data[i + 1]/prev_data[i]) - 1)
    std_dev = statistics.stdev(prev_data)
    lower_val = average - std_dev * 2 * (14/20)
    high_val = average + std_dev * 2 * (14/20)
    print("Bollinger Average: " + str(average))
    print("Bollinger High: " + str(high_val))
    print("Bollinge Low: " + str(lower_val))
    ret_data.append(average)
    ret_data.append(high_val)
    ret_data.append(lower_val)
    return ret_data

def plot_diff():
    plt.figure("Difference")
    diff_list = []
    df = get_historical_data("TNET",start,end,output_format='pandas')
    for i in range(len(df.open)):
        diff_list.append(df.open[i] - df.close[i])
    plt.plot(diff_list)

def plot_history(bollinger):
    plt.figure("History")
    #get data in time frame
    df = get_historical_data("TNET",start,end,output_format='pandas')
    #create colored legned
    blue_patch = mpatches.Patch(color='blue', label='open price')
    orange_patch = mpatches.Patch(color='orange', label='close price')
    green_patch = mpatches.Patch(color='green', label='low price')
    red_patch = mpatches.Patch(color='red',label='high price')
    plt.legend(handles=[blue_patch, orange_patch, green_patch, red_patch])
    #plot prices
    df.open.plot()
    df.close.plot()
    df.low.plot()
    df.high.plot()
    plt.plot(bollinger)


def plot_all(bollinger):
    plot_history(bollinger)
    plot_diff()
    plt.show()
