'''
Notes:

    What does it do so far?
        It places 3 orders of 1 buy and 2 sells for the top 16 most active stocks
'''











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


"""
s = time()
counter = 0
total = 0
def getSellPrice(symbol):
    ''' returns a tuple: (selling-price-with-profit, stop-price-with-loss, selling-price-with-loss) '''
    price = get_live_price(symbol)
    global total
    total += price
#    print(symbol, price, price*1.015, price*0.996, price*0.994)
    create_advance_order(symbol, '1', price*1.015, price*0.996, price*0.994)

def entryFunction(symbols):
    ''' Places 3 orders for any symbol passed to it '''
    for symbol in symbols:
        sell_at_profit, stop_at_loss, sell_at_loss = getSellPrice(symbol)
        create_advance_order(symbol, '1', sell_at_profit, stop_at_loss, sell_at_loss)

threads = []
for i, data in enumerate(get_day_most_active().to_dict()['Symbol'].values()):
    if counter+3 >= 50: break
    try:
#        print(i, end=' ')
        threads.append(threading.Thread(target=getSellPrice, args=(data,)))
        threads[i].start()
        counter+=3
#        print(i+1, stock, getSellPrice(stock), (time()-s)/60)
    except: continue
for thread in threads: thread.join()
print('\n',counter, total)
print((time()-s)/60)
"""













#'''
#s = time()
#threads = []




#for i,stock in enumerate(getAllSymbols()):
#    if counter+3 >= 50: break
#    try:
##        print(i, end=' ')
#        threads.append(threading.Thread(target=getSellPrice, args=(stock,)))
#        threads[i].start()
#        counter+=3
##        print(i+1, stock, getSellPrice(stock), (time()-s)/60)
#    except: continue
#for thread in threads: thread.join()
#
#print('\n',counter)
#print((time()-s)/60)




