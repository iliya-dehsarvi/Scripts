''' Official Packages '''
import cryptocompare
from sklearn.svm import SVR
import pandas as pd
import numpy as np
from datetime import datetime
import time
import os
''' Unofficial Packages '''
import matplotlib.pyplot as plt
import plotly.graph_objects as go
''' Public Functions '''
def getData(symbol='ETC', currency='USD', lim=1500, dataBy='m'):
    ''' returns the data as a data frame '''
    if dataBy == 'm': return pd.DataFrame( cryptocompare.get_historical_price_minute(symbol, curr=currency, limit=lim) )
    elif dataBy == 'h': return pd.DataFrame( cryptocompare.get_historical_price_hour(symbol, curr=currency, limit=lim) )
    elif dataBy == 'd': return pd.DataFrame( cryptocompare.get_historical_price_day(symbol, curr=currency, limit=lim) )

def datetimeConvertor(dataSet): return [time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(times)) for times in dataSet]

def grapher(df, symbol = 'ETC'):
    fig = go.Figure(data=[go.Candlestick(x=np.arange(0,len(df)),\
    open=df['open'],\
    high=df['high'],\
    low=df['low'],\
    close=df['close'])])
    fig.show()
    
def predictions(symbol='BTC', lim=1500, dataBy='m'):
    df = getData(symbol, lim, dataBy)
    print(df)
    indices = [[data] for data in range(len(df))]
    df_close = df.loc[:, 'close']
    df_open = df.loc[:, 'open']
    df_high = df.loc[:, 'high']
    df_low = df.loc[:, 'low']
    close_prices = [float(close_price) for close_price in df_close]
    open_prices = [float(open_price) for open_price in df_open]
    high_prices = [float(high_price) for high_price in df_high]
    low_prices = [float(low_price) for low_price in df_low]
    rbf_svr_close = SVR(kernel='rbf', C=1000.0, gamma=0.15)
    rbf_svr_close.fit(indices, close_prices)
    print('Close fitted')
    rbf_svr_open = SVR(kernel='rbf', C=1000.0, gamma=0.15)
    rbf_svr_open.fit(indices, open_prices)
    print('Open fitted')
    rbf_svr_high = SVR(kernel='rbf', C=1000.0, gamma=0.15)
    rbf_svr_high.fit(indices, high_prices)
    print('High fitted')
    rbf_svr_low = SVR(kernel='rbf', C=1000.0, gamma=0.15)
    rbf_svr_low.fit(indices, low_prices)
    print('Low fitted')
    predictedData = pd.DataFrame( [ {'time': len(df),\
                                     'close': rbf_svr_close.predict([[len(df)]])[0],\
                                     'high': rbf_svr_high.predict([[len(df)]])[0],\
                                     'low': rbf_svr_low.predict([[len(df)]])[0],\
                                     'open': rbf_svr_open.predict([[len(df)]])[0]} ] )            
    print(predictedData)
    df = df.append(predictedData, ignore_index=True)
    grapher(df, symbol)

if '__name__' == '__main__':    
    predictions('ETHBTC')
