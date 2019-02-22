from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import get_historical_intraday
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime

end = datetime.now()
start = datetime(end.year, end.month, end.day - 14)


def plot_diff():
    plt.figure(2)
    diff_list = []
    df = get_historical_data("TNET",start,end,output_format='pandas')
    for i in range(len(df.open)):
        diff_list.append(df.open[i] - df.close[i])
    plt.plot(diff_list)

def plot_history():
    plt.figure(1)
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

def plot_all():
    plot_history()
    plot_diff()
    plt.show()
