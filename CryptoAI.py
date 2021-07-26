import yfinance as yf #Not used in this program
import cryptocompare
import talib as ta

from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet import reactor

from sklearn.svm import SVR
import pandas as pd
import numpy as np
import os, json, requests, threading
from itertools import cycle
from sys import exit
import plotly.graph_objects as go
from time import *
''''''

class CryptoAi:
    def __init__(self):
        API_KEY = 'plJ3OxshNmkTLFlJ0HYKxoJkcL83W2w94eUdozxwSnuVBFPXISmTeGbknFJor2Hf'
        API_SECRET_KEY = 'OM8fEWa5nu19hB5ex909zSFfgf1JLeM01FULXx3DAkTIRVGln8GeWfRUJyqO8xO2'
        self.CLIENT = Client(API_KEY, API_SECRET_KEY, tld='us')
#        status = self.CLIENT.get_dust_log()
#        print(status)
#        return
        self.INITUSD = 10.12
        self.S = time()
        self.DFC = dict()
        self.SYMBS = [SYMB['symbol'] for SYMB in self.CLIENT.get_symbol_ticker()]# if float(SYMB['price']) > 0.5]
#        self.SYMBS = ['NEOUSDT']
        self.INDEX = 1
        self.COUNTER = 0
        self.OHLC = 1
        
        self.TRADER()
#        print(self._DF())
#        self._GRAPHER(self._DF())
#
    def TRADER(self):
        print(time()-self.S)
        THREADS = []
        INDEX = 0
        for SYMB in self.SYMBS:
            print(INDEX, SYMB)
            THREADS.append(threading.Thread(target=self._SOCKET, args=(SYMB, )))
            THREADS[INDEX].start()
            INDEX+=1
        for THREAD in THREADS: THREAD.join()
        del THREADS
        
    def _SOCKET(self, SYMB):
        try: self.DFC[SYMB] = self._DF(SYMB)
        except: return
        BSM = BinanceSocketManager(self.CLIENT)
        CONN = BSM.start_kline_socket(SYMB, self.__TRADE)
        BSM.start()
        
    def _DF(self, SYMB='BTCUSDT', INTERVAL='1m'):
        ROOT = 'https://api.binance.com/api/v1/klines'
        URL = ROOT+'?symbol='+SYMB+'&interval='+INTERVAL
        RESPONSE = requests.get(URL)
        
        
        
#        return RESPONSE
        
        
        
        
        HISTORIC_DATA = json.loads(RESPONSE.text)
        DF = pd.DataFrame(HISTORIC_DATA, columns = ('Open time', 'Open', 'High', 'Low', 'Close',\
                                                    '', '', '', '', '', '', ''))
        del DF['']
#        del DF['Open time']
        return DF
        
    def __TRADE(self, MSG):
        SYMB = MSG['k']['s']
        
        
        
        
#        print(self.INDEX, self._DF(SYMB))
#        self.INDEX+=1
#        return
    
    
    
    
    
    
#        print(MSG)
        Q = float(MSG['k']['Q'])
        QUOTE = [[MSG['k']['t'], MSG['k']['o'], MSG['k']['h'], MSG['k']['l'], MSG['k']['c']]]
        TAGS = ['Open time', 'Open', 'High', 'Low', 'Close']
        
        if self.DFC[SYMB].tail(1)['Open time'].tolist()[0] != MSG['k']['t']:
        
        
        
        
            DF = pd.DataFrame(QUOTE, columns=TAGS)
#            self.DFC[SYMB] = self._DF(SYMB)
            self.DFC[SYMB] = self.DFC[SYMB].append(DF, ignore_index=True)
        
        
        
        
        
            if self._PATTERN(self.DFC[SYMB], SYMB): # and _PREDICT(DFC[SYMB]): print()
                self._ORDER(SYMB, Q)
        
        CHECK = 0
        for Q in QUOTE[0][-3:]:
            if QUOTE[0][1]==Q: CHECK+=1
        if CHECK==3:
            self.OHLC+=1
            print('SAME OHLC')
        
        lastFiveOpens = self.DFC[SYMB].tail(10)['Open'].tolist()
        for data in lastFiveOpens:
            if data != lastFiveOpens[0]:
                print('Not Repeating')
                break
#        print(any(self.DFC[SYMB].tail(5)['Open'] == self.DFC[SYMB].tail(1)['Open']))
#        if self.DFC[SYMB][-1]['Open'] == self.DFC[SYMB][-2] and self.DFC[SYMB][-1] == self.DFC[SYMB][-3] and self.DFC[SYMB][-1] == self.DFC[SYMB][-4] and self.DFC[SYMB][-1] == self.DFC[SYMB][-5]:
#            print('Repeating, FUCK')
        print(self.INDEX, self.OHLC, '%{:.1f}'.format((self.OHLC*100)/self.INDEX), SYMB, '{:.0f}'.format((time()-self.S)/60))
        self.INDEX += 1
        print(self.DFC[SYMB].tail(10))
        print('- '*50)
#        self._GRAPHER(self.DFC[SYMB], SYMB)

        
#            pass
#        sleep(60)
    def _PATTERN(self, DF, SYMB):
        DFG = DF
        DF = DF.tail(5)
#        CDLENGULFING = ta.CDLENGULFING(DF['Open'], DF['High'], DF['Low'], DF['Close'])
#        CDLHAMMER = ta.CDLHAMMER(DF['Open'], DF['High'], DF['Low'], DF['Close'])
#        CDL3WHITESOLDIERS = ta.CDL3WHITESOLDIERS(DF['Open'], DF['High'], DF['Low'], DF['Close'])
#        if any(CDLENGULFING == 100) or any(CDLHAMMER == 100) or any(CDL3WHITESOLDIERS == 100):
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
        
    def _PREDICT(self, DF):
        DF_CLOSE = DF.loc[:, 'Close']
        CLOSING_QUOTES = [float(closed) for closed in DF_CLOSE]
        INDECIES = [[index] for index in range(len(DF))]
        RBF = SVR(kernel='rbf', C=1000.0, gamma=0.15)
        RBF.fit(INDECIES, CLOSING_QUOTES)
        if self.__GR(RBF.predict([[len(DF)-1]]), RBF.predict([[len(DF)]])) > 0: return True
        return False

    def _GRAPHER(self, DF, SYMB='BTCUSDT'):
        try: DF = DF.iloc[-60:]
        except: pass
        fig = go.Figure(data=[go.Candlestick(x=np.arange(0,len(DF)),\
              open=DF['Open'],\
              high=DF['High'],\
              low=DF['Low'],\
              close=DF['Close'])])
        self.COUNTER += 1
        fig.update_layout(title=SYMB+' - '+str(self.COUNTER)+' - '+str('{:.0f}'.format((time()-self.S)/60)))
        fig.show()

    def _ORDER(self, SYMB, QUOTE):
    #    QUANT =
    #    self.CLIENT.order_market_buy(symbol=SYMB, quantity=)
        try:

            QUANTITY = str('{:.6f}'.format((self.INITUSD/QUOTE)/2))
            print(QUANTITY)
            ORDERED = self.CLIENT.create_test_order(symbol=SYMB, side='BUY', type='MARKET', quantity=QUANTITY)
            print('_ORDER')
            print(ORDERED)

        except Exception as e:
            print(e.status_code)
            print(e.message)
    #    print('*', self.CLIENT.get_account_status())
#        reactor.stop()

    def __GR(self, pre, curr): return ((100*curr)/pre)-100




if __name__ == '__main__': AI = CryptoAi()
