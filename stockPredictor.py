'''
TO DO:
    • add open
    • add high
    • add low
    • make it a function that returns a data fram of open, close, low, high, and growth rate of each since the day before
    •
    • fix the calender so you can add more data //DONE
'''

DEBUG = True
from time import *
from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from yahoo_fin.stock_info import get_live_price, get_data
import requests, bitfinex, datetime, threading, subprocess
from pymongo import MongoClient
from os import path

''' ''' ''' '''
SYMBOL='btc'
SYMBOL+='usd'
''' ''' ''' '''


print('\n'*100)
plt.style.use('seaborn-darkgrid')

#....................................................................................
def writer(predicted):
    with open(SYMBOL+'previouslyPredicted.txt', 'w') as db:
        db.truncate(0)
        db.write(str(predicted))
#....................................................................................
def reader():
    with open(SYMBOL+'previouslyPredicted.txt') as db:
        prePredict = list(db)[0]
    return float(prePredict)
#....................................................................................
try: reader()
except: writer('0')




'''....................................................................................'''
def growthRate(pre, curr): return ((100*curr)/pre)-100
'''....................................................................................'''
def predict(SYMBOL, graph=False, graphTag='close'):
    TIMER=time()




    #....................................................................................
#    '''
    api_v2 = bitfinex.bitfinex_v2.api_v2()
    pair = SYMBOL
    bin_size = '1m'
    limit = 1000
#    t_start = datetime.datetime(2018, 4, 1, 0, 0)
#    t_start = mktime(t_start.timetuple()) * 1000
    #t_stop = datetime.datetime(2018, 4, 2, 0, 0)
    #t_stop = mktime(t_stop.timetuple()) * 1000
    result = api_v2.candles(symbol=pair, interval=bin_size,limit=limit)#, start=t_start, end=t_stop)
    tags = ['time', 'open', 'close', 'high', 'low', 'volume']
    df = pd.DataFrame(result, columns=tags)
    df.drop_duplicates(inplace=True)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    df.sort_index(inplace=True)
    #print(df)

    #....................................................................................
    '''
    df = get_data(SYMBOL)#, start_date='08-1-2020')
    if len(df)>=1260: df = df.iloc[-1260:]
#    '''
    #....................................................................................
    actual_price5 = df.tail(1)
#    print(actual_price, get_live_price(SYMBOL))
    #df = df.head(len(df)-1) #<-------- get rid of the last day's data
    days = []
    dates = []
    df_days = df.index.values
    for index, day in enumerate(df_days):
        dates.append( str(day).replace('T00:00:00.000000000','') )
        days.append([index])
    '''
    print(df.columns.tolist())
    '''
    df_adj_close5 = df.loc[:, 'close']
#    df_open = df.loc[:, 'open']
#    df_high = df.loc[:, 'high']
#    df_low = df.loc[:, 'low']
    adj_close_prices5 = [float(adj_close_price5) for adj_close_price5 in df_adj_close5]
#    open_prices = [float(open_price) for open_price in df_open]
#    high_prices = [float(high_price) for high_price in df_high]
#    low_prices = [float(low_price) for low_price in df_low]
    '''Models:'''
    #....................................................................................
    #lin_svr = SVR(kernel='linear', C=1000.0)
    #lin_svr.fit(days, adj_close_prices)
    ''''''
    #poly_svr = SVR(kernel='poly', C=1000.0, degree=2)
    #poly_svr.fit(days, adj_close_prices)
    ''''''
    rbf_svr5 = SVR(kernel='rbf', C=1000.0, gamma=0.15)
    rbf_svr5.fit(days, adj_close_prices5)






    #....................................................................................
#    '''
    api_v2 = bitfinex.bitfinex_v2.api_v2()
    pair = SYMBOL
    bin_size = '1m'
    limit = 1000
#    t_start = datetime.datetime(2018, 4, 1, 0, 0)
#    t_start = mktime(t_start.timetuple()) * 1000
    #t_stop = datetime.datetime(2018, 4, 2, 0, 0)
    #t_stop = mktime(t_stop.timetuple()) * 1000
    result = api_v2.candles(symbol=pair, interval=bin_size,limit=limit)#, start=t_start, end=t_stop)
    tags = ['time', 'open', 'close', 'high', 'low', 'volume']
    df = pd.DataFrame(result, columns=tags)
    df.drop_duplicates(inplace=True)
    df['time'] = pd.to_datetime(df['time'], unit='ms')
    df.set_index('time', inplace=True)
    df.sort_index(inplace=True)
    #print(df)

    #....................................................................................
    '''
    df = get_data(SYMBOL)#, start_date='08-1-2020')
    if len(df)>=1260: df = df.iloc[-1260:]
#    '''
    #....................................................................................
    actual_price = df.tail(1)
#    print(actual_price, get_live_price(SYMBOL))
    #df = df.head(len(df)-1) #<-------- get rid of the last day's data
    days = []
    dates = []
    df_days = df.index.values
    for index, day in enumerate(df_days):
        dates.append( str(day).replace('T00:00:00.000000000','') )
        days.append([index])
    '''
    print(df.columns.tolist())
    '''
    df_adj_close = df.loc[:, 'close']
#    df_open = df.loc[:, 'open']
#    df_high = df.loc[:, 'high']
#    df_low = df.loc[:, 'low']
    adj_close_prices = [float(adj_close_price) for adj_close_price in df_adj_close]
#    open_prices = [float(open_price) for open_price in df_open]
#    high_prices = [float(high_price) for high_price in df_high]
#    low_prices = [float(low_price) for low_price in df_low]
    '''Models:'''
    #....................................................................................
    #lin_svr = SVR(kernel='linear', C=1000.0)
    #lin_svr.fit(days, adj_close_prices)
    ''''''
    #poly_svr = SVR(kernel='poly', C=1000.0, degree=2)
    #poly_svr.fit(days, adj_close_prices)
    ''''''
    rbf_svr = SVR(kernel='rbf', C=1000.0, gamma=0.15)
    rbf_svr.fit(days, adj_close_prices)













#    with open(SYMBOL+'previouslyPredicted.txt') as db:
#        for data in db: prePredict = data
#    with open(SYMBOL+'previouslyPredicted.txt', 'a') as db: db.write(str(*rbf_svr.predict([[len(df)]]))+'\n')


#    rbf_svr_open = SVR(kernel='rbf', C=1000.0, gamma=0.15)
#    rbf_svr_open.fit(days, open_prices)
#
#    rbf_svr_high = SVR(kernel='rbf', C=1000.0, gamma=0.15)
#    rbf_svr_high.fit(days, high_prices)
#
#    rbf_svr_low = SVR(kernel='rbf', C=1000.0, gamma=0.15)
#    rbf_svr_low.fit(days, low_prices)
    #....................................................................................
    '''Outputs:'''
    '''
    print(SYMBOL.upper()+':')

    day = len(df)-1
    print(day)

    print('RBF predict today:                            $', *rbf_svr.predict([[day]]))
    print('RBF predict tomorrow:                         $', *rbf_svr.predict([[day+1]]))
    print('Projected growthRate today-tomorrow:          %', growthRate(*rbf_svr.predict([[day]]), *rbf_svr.predict([[day+1]])))
    #print('Linear predict:       ', *lin_svr.predict(day))
    #print('Poly predict:         ', *poly_svr.predict(day))
    print('Totays closing price:                         $', str(actual_price[TAG]).split('    ')[1])
    '''
#    print(SYMBOL+':\nTime:', time()-TIMER)
    #....................................................................................
    '''Graph:'''
    if graph:
        plt.figure(figsize=(8,5))
        totalDays = -59
        pricePlots=adj_close_prices[totalDays:]
        predictPlot=list(rbf_svr.predict(days))[totalDays:]
        totalDays *= -1
        totalDays += 1
        plt.plot(np.arange(1,totalDays), pricePlots, color='red', label='Original '+graphTag)

#        '''
        print(pricePlots[-1], '<-- Actual price')
        print(pricePlots[-2], '<-- Previous price')
#        '''

        plt.plot(np.arange(1,totalDays), predictPlot, color='blue', label='Predicted '+graphTag)
        totalDays -= 1


#        prePredict = reader()


#        toBeSaved = str(*rbf_svr.predict([[len(df)]]))
#        writer(toBeSaved)

#        '''
        print(*rbf_svr.predict([[len(df)]]))
        print(*rbf_svr.predict([[len(df)-1]]))
        print(dates[-1])
#        '''

        plt.plot( [1,totalDays], [*rbf_svr.predict([[len(df)]]), *rbf_svr.predict([[len(df)]])], '--', label='Predicted' )
#        plt.plot( [1,totalDays], [*rbf_svr.predict([[len(df)-1]]), *rbf_svr.predict([[len(df)-1]])], '--', label='Previously Predicted' )
        plt.plot( [1,totalDays], [pricePlots[-1], pricePlots[-1]], '--', label='Current Close' )
#        plt.plot( [1,totalDays], [pricePlots[-2], pricePlots[-2]], '--', label='Previous Close' )




        plt.plot( [1,totalDays], [*rbf_svr5.predict([[len(df)]]), *rbf_svr5.predict([[len(df)]])], '--', label='Predicted next 5 minutes' )





#        plt.plot([1,7], [*rbf_svr_open.predict([[len(df)]]), *rbf_svr_open.predict([[len(df)]])], '--', label='Predicted to OPEN at $'+'{:.5}'.format(float(*rbf_svr_open.predict([[len(df)]])))+' for the next trading day')
#        plt.plot([1,7], [*rbf_svr_low.predict([[len(df)]]), *rbf_svr_low.predict([[len(df)]])], '--', label='Predicted the LOWEST at $'+'{:.5}'.format(float(*rbf_svr_low.predict([[len(df)]])))+' for the next trading day')
#        plt.plot([1,7], [*rbf_svr_high.predict([[len(df)]]), *rbf_svr_high.predict([[len(df)]])], '--', label='Predicted the HIGHEST at $'+'{:.5}'.format(float(*rbf_svr_high.predict([[len(df)]])))+' for the next trading day')


        #plt.scatter(days, rbf_svr.predict(days), color='black', label='Tomorrows Predicted Close')
        #plt.plot(days, lin_svr.predict(days), color='red', label='Linear model')
        #plt.plot(days, poly_svr.predict(days), color='blue', label='Poly model')
#        plt.legend()
        plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05),fancybox=True, shadow=True, ncol=5, prop={'size': 6})
        plt.title(SYMBOL.upper()+'\nPredicted to '+graphTag.upper()+' at %'+str( growthRate(*rbf_svr.predict([[len(df)-1]]), *rbf_svr.predict([[len(df)]]) ) )  +'\n Predicted to '+graphTag.upper()+' at $'+str(growthRate(*rbf_svr5.predict([[len(df)-1]]), *rbf_svr5.predict([[len(df)]]) ))+' the next 5 minutes')

#        plt.show()
        plt.savefig(SYMBOL+'.pdf')
        graphAddress = '/Users/iliyadehsarvi/Desktop/summer2020Project/'+SYMBOL+'.pdf'

        subprocess.call(['osascript', '-e', 'tell application "Preview" to quit'])
        subprocess.call(['open', graphAddress])

    #....................................................................................
#    return ['Last Trading Day', *rbf_svr.predict([[len(df)-1]])],\
#           ['Next Trading Day', *rbf_svr.predict([[len(df)]])],\
#           ['Last-Next growthRate', growthRate( *rbf_svr.predict([[len(df)-1]]),*rbf_svr.predict([[len(df)]]) )]

    print(SYMBOL, growthRate( *rbf_svr.predict([[len(df)-1]]),*rbf_svr.predict([[len(df)]]) ), pricePlots[-1])
    return [SYMBOL, growthRate( *rbf_svr.predict([[len(df)-1]]),*rbf_svr.predict([[len(df)]]) ), pricePlots[-1]]


#    return ['Last Trading Day',\
#            *rbf_svr_open.predict([[len(df)-1]]), *rbf_svr_high.predict([[len(df)-1]]),\
#            *rbf_svr_low.predict([[len(df)-1]]), *rbf_svr.predict([[len(df)-1]])],\
#           ['Next Trading Day',\
#           *rbf_svr_open.predict([[len(df)]]), *rbf_svr_high.predict([[len(df)]]),\
#            *rbf_svr_low.predict([[len(df)]]), *rbf_svr.predict([[len(df)]])],\
#           ['Last-Next growthRate',\
#           growthRate( *rbf_svr_open.predict([[len(df)-1]]),*rbf_svr_open.predict([[len(df)]]) ),\
#           growthRate( *rbf_svr_high.predict([[len(df)-1]]),*rbf_svr_high.predict([[len(df)]]) ),\
#           growthRate( *rbf_svr_low.predict([[len(df)-1]]),*rbf_svr_low.predict([[len(df)]]) ),\
#           growthRate( *rbf_svr.predict([[len(df)-1]]),*rbf_svr.predict([[len(df)]]) )]
#


    #return ['open', 'high', 'low', 'close'], ['open', 'high', 'low', 'close'], [Last-Next growthRate,'%open', '%high', '%low', '%close']
'''....................................................................................'''
s = time()
symbolList = ['btcusd', 'ethusd', 'bchusd', 'ltcusd', 'etcusd', 'bsvusd', 'xrpusd']#, 'qtumusd']
#print(predict('ethusd',True, 'close'))
#'''
while True:
#    try:
    pr = predict('btcusd', True)
#        if pr[1] >= 0.1:
    print(*pr)
    sleep(30)
#    except:
#
#        break
#'''

#threads = []
#for i, data in enumerate(symbolList):
#    try:
#        threads.append(threading.Thread(target=predict, args=(data,True,'close')))
#        threads[i].start()
#    except: continue
#for thread in threads: thread.join()
#print(time()-s)



