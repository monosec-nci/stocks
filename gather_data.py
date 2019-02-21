from iexfinance.stocks import Stock
from datetime import datetime
from iexfinance.stocks import get_historical_data
import matplotlib.pyplot as plt
from iexfinance.stocks import get_historical_intraday
import matplotlib.patches as mpatches
import numpy as np
import math

end = datetime.now()
start = datetime(end.year, end.month, end.day - 14)
stock_list = Stock(["TNET","AAPL"])
stock_data = ["TNET","AAPL"]

def get_current_value(list):
    return list.get_price()

def get_historial_values(list):
    print(get_historical_data(list,start,end))

def plot_history(list):
    plt.figure(1)
    #get data in time frame
    df = get_historical_data(list,start,end,output_format='pandas')
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


def plot_diff(stock):
    plt.figure(2)
    diff_list = []
    df = get_historical_data("TNET",start,end,output_format='pandas')
    for i in range(len(df.open)):
        diff_list.append(df.open[i] - df.close[i])
    plt.plot(diff_list)


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


def predict_day_simple(prev_data):
    #calculate mean
    mean = 0
    for i in prev_data:
        mean += i
    mean = mean / len(prev_data)
    #print("Mean: " + str(mean))

    # calculate trend
    trend = (prev_data[-1] - prev_data[0]) / len(prev_data)
    #print("Trend: " + str(trend))
    print(str(prev_data[-1] + trend))

def predict_day_medium(prev_data, predict, stock):
    print("Predicting Days: " + str(predict))
    print("Stock to predict: " + stock)

    vol = calc_volatility(prev_data)
    cur_price = get_current_value(Stock(stock))
    #First, divide the number of days until the stock price forecast by 365, and then find the square root of that number. Then, multiply the square root with the implied volatility percentage and the current stock price.
    div = predict/365
    sqrt = math.sqrt(div)
    percent_vol = vol / 100
    #using annual volatility instead of implied volatility for now
    final_ratio = sqrt  * percent_vol * cur_price
    print("Final ratio: " + str(final_ratio))
    print()
    final_min = cur_price - final_ratio
    final_max = cur_price + final_ratio
    print("Min: " + str(final_min))
    print("Max: " + str(final_max))


def predict_next_day():
    cur_date = datetime.now()
    orig_date = datetime(cur_date.year, cur_date.month, cur_date.day - 14)
    prev_data = []
    df = get_historical_data("TNET",orig_date,cur_date, output_format='pandas')
    for i in range(len(df.close)):
        #print(df.close[i])
        prev_data.append(df.close[i])
    #df.close.plot()
    #plt.show()
    print("Previous Data: ")
    print(prev_data)
    print()
    print("Predicted Day Simple:")
    predict_day_simple(prev_data)
    print()
    print("Predicted Day Medium:")
    predict_day_medium(prev_data,3, "TNET")

def plot_all():
    plot_history("TNET")
    plot_diff("TNET")
    plt.show()

#get_current_value(stock_list)
#plot_history_intraday("TNET")
#plot_history("TNET")
#get_historial_values("TNET")
predict_next_day()
#plot_diff("TNET")
plot_all()
