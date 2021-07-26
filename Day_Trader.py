import yfinance as yf
import yahoo_fin.stock_info as yahoo
from twelvedata import TDClient

import talib as ta
from sklearn.svm import SVR
import pandas as pd
import numpy as np
import os, json, requests, threading
from itertools import cycle
from sys import exit
import plotly.graph_objects as go
from time import *

class TradeX:
    def __init__(self):
        self.DFC = dict()
        self.SYMBS = ['AAPL']
        print(len(self.SYMBS))
        self.S = time()
        self.INDEX = 0
        self.COUNTER = 0
        self.TRADER()
        
    def TRADER(self):
        THREADS = []
        INDEX = 0
        for SYMB in self.SYMBS[-500:]:
            print(INDEX, SYMB)
            THREADS.append(threading.Thread(target=self._SOCKET, args=(SYMB, )))
            THREADS[INDEX].start()
            INDEX+=1
        for THREAD in THREADS: THREAD.join()
        del THREADS
        
    def _SOCKET(self, SYMB, PERIOD='5d'):
        HISTORIC_DATA = yf.download(tickers=SYMB, period=PERIOD, interval='1m')
        DF = pd.DataFrame(HISTORIC_DATA, columns = ('Open', 'High', 'Low', 'Close','', ''))
        del DF['']
        TD = TDClient(apikey='6abf7ab1ba2448a297df16da6e78f960')
        SOCKET = TD.websocket(symbols=SYMB, on_event=self.__TRADE)
        SOCKET.subscribe(['AAPL'])
        SOCKET.connect()
        SOCKET.keep_alive()
            
    def __TRADE(self, MSG):
        print(self.INDEX, SYMB, '{:.0f}'.format((time()-self.S)/60))
        self.INDEX += 1
        print(MSG)
    
    def _PATTERN(self, DF, SYMB):
        DFG = DF
        DF = DF.tail(5)
        
        CDLHAMMER = ta.CDLHAMMER(DF['Open'], DF['High'], DF['Low'], DF['Close'])
        CDLENGULFING = ta.CDLENGULFING(DF['Open'], DF['High'], DF['Low'], DF['Close'])
        CDL3BLACKCROWS = ta.CDL3BLACKCROWS(DF['Open'], DF['High'], DF['Low'], DF['Close'])
        CDL3LINESTRIKE = ta.CDL3LINESTRIKE(DF['Open'], DF['High'], DF['Low'], DF['Close'])
        CDLSTICKSANDWICH = ta.CDLSTICKSANDWICH(DF['Open'], DF['High'], DF['Low'], DF['Close'])
        CDL3WHITESOLDIERS = ta.CDL3WHITESOLDIERS(DF['Open'], DF['High'], DF['Low'], DF['Close'])

        if any(CDLHAMMER == 100) or any(CDLENGULFING == 100)\
            or any(CDL3BLACKCROWS == 100) or any(CDL3LINESTRIKE == 100)\
            or any(CDLSTICKSANDWICH == 100) or any(CDL3WHITESOLDIERS == 100):
            print(DF)
            self._GRAPHER(DFG, SYMB)
            return True
        return False
        
    def _GRAPHER(self, DF, SYMB):
        DF = DF.iloc[-60:]
        fig = go.Figure(data=[go.Candlestick(x=np.arange(0,len(DF)),\
              open=DF['Open'],\
              high=DF['High'],\
              low=DF['Low'],\
              close=DF['Close'])])
        self.COUNTER += 1
        fig.update_layout(title=SYMB+' - '+str(self.COUNTER)+' - '+str('{:.0f}'.format((time()-self.S)/60)))
        fig.show()

print('\n')
