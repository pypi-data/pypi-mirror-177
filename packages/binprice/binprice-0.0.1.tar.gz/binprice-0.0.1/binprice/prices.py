import requests
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt


API_ADDRESS = 'https://api.binance.com'


# Fetch Candlestick data from the API
def get_candle_data(currency, interval, start, end):
    response = requests.get(f"{API_ADDRESS}/api/v3/klines",
                            params={'symbol': currency,
                                    'interval': interval,
                                    'startTime': start,
                                    'endTime': end,
                                    'limit' : 1000})
    return response


def plot_data(data):
    df = pd.DataFrame(data, columns=['Time', 'Price'])

    df.plot(x='Time', y='Price')
    plt.show()


# Main function to collect the data and display it
def candlestick_data(currency, interval= '6h'):

    # Time frame in the timestamp format
    start_at = int(round(datetime.timestamp(datetime.now() -
                                                        timedelta(hours=48)) * 1000))
    end_at = int(round(datetime.timestamp(datetime.now()) * 1000))

    # Collect candle stick data
    data = get_candle_data(currency, interval, start_at, end_at)

    # Populate the data array to be used for plotting
    data_array = []
    for item in data.json():
        time = datetime.fromtimestamp(item[0] // 1000.0)
        price = float(item[4])
        data_array.append([time, price])

    # Print the data for if GUI is not available
    for item in data.json():
        time = datetime.fromtimestamp(item[0] // 1000.0).strftime('%d.%m.%Y %H:%M:%S')
        price = float(item[4])

        print(f'{time}, Price:{price}\n')
        
    # Display the data
    plot_data(data_array)   
