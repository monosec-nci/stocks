from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import get_historical_intraday
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from datetime import datetime
import numpy as np
import math
##########
import stat_math
import stat_plot


end = datetime.now()
start = datetime(end.year, end.month, end.day - 14)
stock_list = Stock(["TNET","AAPL"])
stock_data = ["TNET","AAPL"]

def get_current_value(list):
    return list.get_price()

def get_historial_values(list):
    print(get_historical_data(list,start,end))

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
    return (prev_data[-1] + trend)

def predict_day_medium(prev_data, predict, stock):
    cur_price = get_current_value(Stock(stock))
    print("Predicting Days: " + str(predict))
    print("Stock to predict: " + stock)
    print("Current stock price: " + str(cur_price))
    vol = stat_math.calc_volatility(prev_data)
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
    return final_ratio


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
    print(predict_day_simple(prev_data))
    print()
    print("Predicted Day Medium:")
    predict_day_medium(prev_data,3, "TNET")

def main():
    stat_plot.plot_all()
    predict_next_day()


main()
