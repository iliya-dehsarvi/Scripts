import requests, threading
from trader import create_advance_order
from yahoo_fin.stock_info import get_live_price, get_day_gainers, get_day_most_active
from screener import getAllSymbols
import pandas as pds
from time import *
from stockPredictor import predict

TIMER = time()

def displayPrediction(SYMBOL):
    try:
        prediction = predict(SYMBOL)
        print(SYMBOL.upper()+':')
        print('     '+prediction[0][0]+':')
        print('          open:     $',prediction[0][1])
        print('          high:     $',prediction[0][2])
        print('          low:      $',prediction[0][3])
        print('          close:    $',prediction[0][4])
        print()
        print('     '+prediction[1][0]+':')
        print('          open:     $',prediction[1][1])
        print('          high:     $',prediction[1][2])
        print('          low:      $',prediction[1][3])
        print('          close:    $',prediction[1][4])
        print()
        print('     '+prediction[2][0]+':')
        print('          open:     %',prediction[2][1])
        print('          high:     %',prediction[2][2])
        print('          low:      %',prediction[2][3])
        print('          close:    %',prediction[2][4])
        print('- '*50)
    except:
        print('\n!!!!! CHECK '+SYMBOL+' !!!!!\n')
        print('- '*50)

print('\n'*100)

threads = []
for i, data in enumerate(get_day_most_active().to_dict()['Symbol'].values()):
    try:
        threads.append(threading.Thread(target=displayPrediction, args=(data,)))
        threads[i].start()
    except: continue
for thread in threads: thread.join()

print('Total time:      ', time()-TIMER)
