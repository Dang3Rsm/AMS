import yfinance as yf
import time


def get_candlestick_data(symbol):
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", interval="1m")
    return data


symbol = "ETH-USD"
data = get_candlestick_data(symbol)
# print(data)
o = data['Open']
h = data['High']
l = data['Low']
c = data['Close']
print(data)
# print(o + h + l +c)

while False:
    # Fetch the latest data
    data = get_candlestick_data(symbol)
    # print(data)
    o = data['Open']
    h = data['High']
    l = data['Low']
    c = data['Close']
    print(o + h + l +c)
    time.sleep(1)
