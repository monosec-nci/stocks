#Author: nci*
#Co-author: @FlareFlax https://github.com/FlareCoding
#This software is current open sorce and available for anyone
#For any questions or concerns, feel free to email me or send me a message on discord
#Contact info:
#EMAIL : monosec.nci@gmail.com
#DISCORD : nci*#8948
#PROGRAM:
#This program uses iexfinance to get financial data for stocks, and utilizes matplotlib to draw visualization data
#Coding style will remain snake_case in order to give python a slightly more modern feel translated over from my C++ style
#Printing will be reduced to only integral data, but since it's currently in debug stage, print statements are prevalent




from iexfinance.stocks import Stock
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import get_historical_intraday
###########
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
##########
from datetime import datetime
import numpy as np
import math
##########
import stat_math
import stat_plot

#global declarations
end = datetime.now()
start = datetime(end.year, end.month, end.day - 14)
stock_list = Stock(["TNET","AAPL"])
stock_data = ["TNET","AAPL"]

def get_current_value(list):
    return list.get_price()

def get_historial_values(list):
    return get_historical_data(list,start,end)

def predict_day_simple(prev_data):

    """
    Predicts the next day's stock price according the current slope of stock trend from 14 days of data

    Parameters
    ---
    - prev_data : arr
        an array of 14 days worth of data

    Returns
    ---
    - prev_data[-1] + trend: returns the last member of the array (array[-1]) and adds the trend onto it

    """
    #setting mean
    mean = 0

    #calculating mean from prev_data list
    for i in prev_data:
        mean += i
    mean = mean / len(prev_data)

    #find the slope/trend and return predicted price due to trend
    trend = (prev_data[-1] - prev_data[0]) / len(prev_data)
    return (prev_data[-1] + trend)

def predict_day_medium(prev_data, predict, stock):
    """
    Calculates a predictive price using volatility as an indicator

    Parameters
    ---
    - prev_data : arr
        an array of 14 days worth of data populated with data when called from predict_next_day
    - predict : int
        days in the future to predict
    - stock : str
        the string of the stock's tickner

    Returns
    ---
    final_ratio : float
        the result of the volatility calculations with ratios of day predictions and current price
    """

    cur_price = get_current_value(Stock(stock))
    #printing debug information
    print("Predicting Days: " + str(predict))
    print("Stock to predict: " + stock)
    print("Current stock price: " + str(cur_price))
    print()

    vol = stat_math.calc_volatility(prev_data)
    #First, divide the number of days until the stock price forecast by 365, and then find the square root of that number. Then, multiply the square root with the implied volatility percentage and the current stock price.
    div = predict/365
    sqrt = math.sqrt(div)
    percent_vol = vol / 100
    ## TODO: use implied volatility instead of annualized volatility / 100
    final_ratio = sqrt  * percent_vol * cur_price

    final_min = cur_price - final_ratio
    final_max = cur_price + final_ratio
    print("Min: " + str(final_min))
    print("Max: " + str(final_max))
    return final_ratio


def predict_next_day():
    """
    A method used to gather data for prev_data and calls predict_day_* methods
    Code flow and logic: check inline comments
    """

    #set up dates
    cur_date = datetime.now()
    orig_date = datetime(cur_date.year, cur_date.month, cur_date.day - 14)
    prev_data = []
    #read data from df into prev_data array
    df = get_historical_data("TNET",orig_date,cur_date, output_format='pandas')
    for i in range(len(df.close)):
        #print(df.close[i])
        prev_data.append(df.close[i])

    #print debug information and call predict functions
    print("Previous Data: ")
    print(prev_data)
    print()
    print("Predicted Day Simple:")
    print(predict_day_simple(prev_data))
    print()
    print("Predicted Day Medium:")
    predict_day_medium(prev_data,3, "TNET")

def main():
    """
    Main method: Calls plot_all from stat_plot.py and predict_next_day
    """
    stat_plot.plot_all()
    predict_next_day()


main()
