import datetime
import yfinance as yf


def get_stock(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period='2d', interval='1d')
    return history.to_json()


def get_current_stock_value(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period='2d', interval='1d')
    return history.iloc[-1]['Close']


def get_stock_value_time(ticker):
    stock = yf.Ticker(ticker)
    history = stock.history(period='5d', interval='1d')
    # print(history.loc[:, ['Close']])
    return history.loc[:, ['Close']]


def get_stock_price_by_date(ticker, date):
    start_date = datetime.datetime.strptime(date, '%Y-%m-%d')
    end_date = start_date + datetime.timedelta(days=1)
    stock = yf.Ticker(ticker)
    history = stock.history(start=start_date, end=end_date, interval='1d')
    # print(history.iloc[0]['Close'])
    return history.iloc[0]['Close']
