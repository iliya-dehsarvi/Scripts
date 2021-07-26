'''
#1
    TSLA: 0.7088571677207947
    AAPL: 0.7295304839611053
    AAL: 0.7037035264968872
    
    total cases = 1000
    internet speed = 128.8 Mbps
    time = 35.71
#2
    TSLA: 0.7078310823440552

    total cases = 500
    internet speed = 123.7 Mbps
    time = 5.90
#3
    AAPL: 0.7003654985427856
    
    total cases = 500
    internet speed = 133.7 Mbps
    time = 5.84
#4
    AAL: 0.6923800768852234
    
    total cases = 500
    internet speed = 126.2 Mbps
    time = 5.77
#5
    TSLA: 0.6530425071716308 183.56400000000002
    AAPL: 0.6781869411468506 45.843
    AAL: 0.7054386854171752 1.262
    AMZN: 0.7054386854171752 318.241
    CLF: 0.7054386854171752 0.645
    
    total cases = 10
    internet speed = 121.3 Mbps
    time = 0.57
'''
#<span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="50">1,835.64</span>
#....................................................................................
print('\n'*1000)
import requests, webbrowser, re, threading, random
from bs4 import BeautifulSoup, SoupStrainer
from time import *
from trader import create_order, stock_position, get_account
DEBUG = True
run = True
timer = time()
counter = 0

toBeAddedSymbols = ['FB', 'TSLA', 'MFST', 'NFLX', 'AMD']
symbols = [] # Contains all the symbols to be watched and traded

#symbols.append('FB')
#symbols.append('AAPL')
#symbols.append('GOOG')
##symbols.append('NFLX')
#symbols.append('AMZN')
#symbols.append('MSFT')
#symbols.append('PANW')
#symbols.append('TSLA')
#symbols.append('ANET')
#symbols.append('BABA')

symbols.append('AAPL')
symbols.append('AAL')
symbols.append('GOOG')
symbols.append('AMZN')
symbols.append('UAL')

symbolsCounter = {symbol:0 for symbol in symbols}
for symbol in toBeAddedSymbols:
    symbolsCounter[symbol] = 0

priceHistory = {}
currentlyOwned = []
profits = {}

url = "https://yahoo-finance-free.p.rapidapi.com/v6/finance/quote"
headers = {
    'x-rapidapi-host': "yahoo-finance-free.p.rapidapi.com",
    'x-rapidapi-key': "ffe01c2c87msh2f0ee91f9c03770p15ec73jsneecbb3a5e36a"
    }
#....................................................................................

def apiQuote(symbol):
    querystring = {"region":"US","lang":"en","symbols":symbol}
    response = requests.request("GET", url, headers=headers, params=querystring)
    entryQuote = eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))['quoteResponse']['result'][0]['regularMarketPrice']
    priceHistory[symbol] = [entryQuote]
    profits[symbol] = []
    print(entryQuote)
    
#....................................................................................

for symbol in symbols: apiQuote(symbol)
#    querystring = {"region":"US","lang":"en","symbols":symbol}
#    response = requests.request("GET", url, headers=headers, params=querystring)
#    entryQuote = eval(response.text.replace('true', 'True').replace('false', 'False').replace('null', 'None'))['quoteResponse']['result'][0]['regularMarketPrice']
#    priceHistory[symbol] = [entryQuote]
#    profits[symbol] = []

print(priceHistory)

#....................................................................................

URL = 'https://finance.yahoo.com/quote/'

#....................................................................................

def getCounter():
    global counter
    return counter
def counterUpdate():
    global counter
    counter += 1

#....................................................................................

def growthRate(pre, curr): return ((100*curr)/pre)-100

#....................................................................................

def getQuote(symbol, previousPrice):
    try:
        s = time()
        symbol = symbol.upper()
        page = requests.get(URL+symbol)
        soup = BeautifulSoup(page.text, 'lxml')
        spans = soup.find_all('span', class_='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)')
    #    print(spans, '\n'*5)
        quote = float(str(spans[0]).replace('<span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="50">', '').replace('</span>', '').replace(',', ''))
        
        
        
        
        
        '''
        
        instantGrowth = growthRate(priceHistory[symbol][-1], quote)
        totalGrowth = growthRate(priceHistory[symbol][0], quote)
        priceHistory[symbol].append(quote)


        
        
        '''
        q = random.randint(int(priceHistory[symbol][-1]-(priceHistory[symbol][-1]*0.02)),int(priceHistory[symbol][-1]+(priceHistory[symbol][-1]*0.02)))
        instantGrowth = growthRate(previousPrice, q)
        totalGrowth = growthRate(priceHistory[symbol][0], q)
        priceHistory[symbol].append(q)
#        '''
        
        
        
        
        
        if totalGrowth<-1:
            print(symbol, 'removed .............................................................')
            symbols.remove(symbol)
            symbols.append(toBeAddedSymbols[0])
            apiQuote(toBeAddedSymbols[0])
            toBeAddedSymbols.remove(toBeAddedSymbols[0])
            toBeAddedSymbols.append(symbol)
            
#            profits[toBeAddedSymbols[0]] = [0]
            if symbol in currentlyOwned:
                create_order(symbol, 1, 'sell', 'market', 'day')
                currentlyOwned.remove(symbol)
                profits[symbol].append(priceHistory[symbol][-1]-priceHistory[symbol][0])
                counterUpdate()
        
        if not (symbol in currentlyOwned): #BUY
            if -0.2<=instantGrowth<=0.5 and -0.2<=totalGrowth<=0.5:
                create_order(symbol, '1', 'buy', 'market', 'day')
                print(symbol, time()-s, time()-timer, '                 BUY                 ', 'Starting price: $'+str(priceHistory[symbol][0])+' Previous price: $'+ str(previousPrice)+' Current price: $'+str(quote), '% '+str(instantGrowth), '% '+str(totalGrowth))
                currentlyOwned.append(symbol)
                symbolsCounter[symbol]+=1
                print(currentlyOwned, symbol, symbolsCounter[symbol], 'at buy')
                
                counterUpdate()
                
                return time()-s, float(quote), '+'
        if symbol in currentlyOwned and totalGrowth>3: #SELL
                create_order(symbol, 1, 'sell', 'market', 'day')
                print(symbol, time()-s, time()-timer, '                 SELL                 ', 'Starting price: $'+str(priceHistory[symbol][0])+' Previous price: $'+ str(previousPrice)+' Current price: $'+str(quote), '% '+str(instantGrowth), '% '+str(totalGrowth))
                currentlyOwned.remove(symbol)
                profits[symbol].append(priceHistory[symbol][-1]-priceHistory[symbol][0])
                priceHistory[symbol] = [quote]
                symbolsCounter[symbol]-=1
                print(currentlyOwned, symbol, symbolsCounter[symbol], 'at sell')
                
                counterUpdate()
                
                return time()-s, quote, '-'
    #    else:
        print(symbol, time()-s, time()-timer, 'N/A', 'Starting price: $'+str(priceHistory[symbol][0])+' Previous price: $'+str(previousPrice)+' Current price: $'+str(quote), '% '+str(instantGrowth), '% '+str(totalGrowth))
        print(currentlyOwned, symbol, symbolsCounter[symbol])
        return time()-s, quote, 'Const'
    except:
        if symbol in currentlyOwned:
            print('!'*20+'\n'*2)
            create_order(symbol, 1, 'sell', 'market', 'day')
            currentlyOwned.remove(symbol)
            profits[symbol].append(priceHistory[symbol][-1]-priceHistory[symbol][0])
            symbolsCounter[symbol]-=1
            print(currentlyOwned, symbol, symbolsCounter[symbol], '\n'*3+'!'*20)
        return time()-s, 0, 'NULL'

'''....................................................................................'''

def main():
    s = time()
    i = 0
#    for i in range(3):
    while True:
#        try:
        if getCounter()+len(currentlyOwned) >= 40: break

        print('\n*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*'+(len(str(i+1))-1)*'~'+'\n~*~*~*~*~*~*~*~*~*~ '+str(i+1)+' ~*~*~*~*~*~*~*~*~*~\n*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*'+(len(str(i+1))-1)*'~'+'\n'+ str(getCounter()))
        print(symbols)
        totalProfit = 0
        for stock, profit in profits.items():
            print(stock, '  $', sum(profit))
            totalProfit += sum(profit)
        print('Total  $', totalProfit)
        threads = []
        for index, stock in enumerate(symbols):
            threads.append(threading.Thread(target=getQuote, args=(stock, priceHistory[stock][-1])))
            threads[index].start()
        for thread in threads: thread.join()
        del threads
        sleep(5)
        i+=1


#        except:
#            print(currentlyOwned)
#            for symbol in currentlyOwned:
#                create_order(symbol, 1, 'sell', 'market', 'day')
#                profits[symbol].append(priceHistory[symbol][-1]-priceHistory[symbol][0])
#                counterUpdate()
#
#            totalProfit = 0
#            for stock, profit in profits.items():
#                print(stock, '  $', sum(profit))
#                totalProfit += sum(profit)
#
#            print('\n$', totalProfit)
#            print('\n', time()-s)
#            print('\n', getCounter())
#            return


    print(currentlyOwned)
    for symbol in currentlyOwned:
        create_order(symbol, 1, 'sell', 'market', 'day')
        profits[symbol].append(priceHistory[symbol][-1]-priceHistory[symbol][0])
        counterUpdate()

    totalProfit = 0
    for stock, profit in profits.items():
        print(stock, '  $', sum(profit))
        totalProfit += sum(profit)
    
    print('\n$', totalProfit)
    print('\n', time()-s)
    print('\n', getCounter())

if run: main()

#....................................................................................


''''''
#print('\n'*1000)
