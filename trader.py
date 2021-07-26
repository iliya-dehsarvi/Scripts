import requests, json, time
from links import *
from datetime import datetime
    
def get_account():
    CATCH = requests.get(ACCOUNT_URL, headers=HEADERS)
    dataContainer = eval(str(CATCH.content).replace("b'",'').replace("'", '').replace('false', 'False').replace('true', 'True'))
#    print(CATCH.content)
    return dataContainer

def stock_position(symbol):
    CATCH = requests.get(POSISIONS_URL, headers=HEADERS)
    dataContainer = eval(str(CATCH.content).replace("b'[",'').replace("]'", ''))
    try:
#        return dataContainer
        
        
        for data in dataContainer:
            if data['symbol'] == symbol:
    #            print(data['symbol'], data['qty'], data['current_price'], '\n')
                return data
    except:
        if dataContainer['symbol'] == symbol: return dataContainer
        

def create_order(symbol, qty, side, type, time_in_force, limit_price=None, stop_price=None):
    ORDER = {
        'symbol': symbol,
        'qty': qty,
        'side': side,
        'type': type,
        'time_in_force': time_in_force,
        'limit_price': limit_price,
        'stop_price': stop_price }
#    CATCH = requests.post(ORDERS_URL, json=ORDER, headers=HEADERS)

    print('\n\n\n~~~~~~~~~~~',symbol, qty, side,'~~~~~~~~~~~\n\n\n')

#    return json.loads(CATCH.content)


def create_advance_order(symbol, qty, sell_at_profit, stop_at_loss, sell_at_loss):
    ORDER = {
        'symbol': symbol,
        'qty': qty,
        'side': 'buy',
        'type': 'market',
        'time_in_force': 'day',
        'order_class': 'bracket',
        'take_profit': { 'limit_price': sell_at_profit },
        'stop_loss': { 'stop_price': stop_at_loss, 'limit_price': sell_at_loss }
        }
        
    CATCH = requests.post(ORDERS_URL, json=ORDER, headers=HEADERS)
    print('~~~~~~~~~~~',symbol, qty, sell_at_profit, stop_at_loss, sell_at_loss,'~~~~~~~~~~~')
    return json.loads(CATCH.content)
'''
def progressBar():
    STARTED_AT = datetime.now().time()
    print('|', end='')
    for i in range(50):
        print('█', end='', flush=True)
        time.sleep(0.015)
    print('|')
    return str(datetime.now().time())
'''

#def get_data(symbol):
##    task = {'symbol': symbol}
#    print(requests.get(LAST_QUOTE_URL, params=symbol, headers=HEADERS).content)
#
#def growth_slope(previous_price, current_pricel):
#    return
#
#def trader_loop(symbol):
#    owned = True
#    while True:
#        if owned and growth_slope(pre, curr) < 0: create_order(symbol, '2', 'sell', 'market', 'day')
#        elif (not owned) and growth_slope(pre, curr) > 0: create_order(symbol, '2', 'buy', 'market', 'day')

    
# 1. Find out how to get stock info
# 2.
    
#get_data('TSLA')

#create_order('CLF', '2', 'buy', 'market', 'day')

print('\n'*20)

#print(str(stock_position('TSLA')['qty']))

#create_order('TSLA', str(stock_position('TSLA')['qty']), 'sell', 'market', 'day')


#create_order('TSLA', str(stock_position('TSLA')['qty']), 'sell', 'market', 'day')
#create_order('AAPL',  str(stock_position('AAPL')['qty']), 'sell', 'market', 'day')
#create_order('AAL',  str(stock_position('AAL')['qty']), 'sell', 'market', 'day')
#create_order('AMZN',  str(stock_position('AMZN')['qty']), 'sell', 'market', 'day')
#create_order('CLF',  str(stock_position('CLF')['qty']), 'sell', 'market', 'day')

#print(stock_position('TSLA'))
#print(stock_position('AAPL'))
#print(stock_position('AAL'))
#print(stock_position('AMZN'))
#print(stock_position('CLF'))


#print(get_account())
