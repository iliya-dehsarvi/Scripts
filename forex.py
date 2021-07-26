from sklearn.svm import SVR
import pandas as pd
from yahoo_fin.stock_info import get_data

#We need to set up our dataframe
#We will be only working with the past 5 years closing prices of every trading day
df = get_data('AAPL')
if len(df)>=1260: df = df.iloc[-1260:]

#For every single data we have we also want to have an index so later on we could call the prediction based on its index
indices = [[index] for index in range(len(df))]

#Let's get all the closing prices in our dataframe and make sure they are all floats
df_close = df.loc[:, 'close']
close_prices = [float(close_price) for close_price in df_close]

#Let's set up our machine learning predictor, we will be using the radial basis function which goes by RBF, there are also linear, and polynomial methods but from personal experience RBF works the best in this case!
rbf_svr = SVR(kernel='rbf', C=1000.0, gamma=0.15)

#Let's now feed our machine learning some data to predict!
rbf_svr.fit(indices, close_prices)

#And that's it! We are all done! All we need to do is to call the index we want to see the pridiction for and we could check tomorrow after the trading day closes to see if the predictin was correct or not!
predectedToCloseTomorrow = rbf_svr.predict([[len(df)]])[0] #len(df), represents the next day's predicted price index
predectedToCloseToday = rbf_svr.predict([[len(df)-1]])[0] #represents today's predicted price index

#We could even calculate the percentage growth to see if the price will be going higher or lower.
#The function below calculates the percentage growth for use all we need to do is to call it!
def growthRate(pre, curr): return ((100*curr)/pre)-100

#And now let's call the growth rate function to see if the stock price is going up or down tomorrow!
closingRate = growthRate(predectedToCloseToday, predectedToCloseTomorrow)

#We are all done let's print the closing rate!
print('The AAPL stock is predicted to close at %', '{:.3f}'.format(closingRate), 'the next trading day.')



'''
    Hello everyone,
    Machine learning is not as hard as what you think thanks to the great python libraries!
    Today I would like to show you guys how simple it is to predict the future stock prices for the next minute, 5 minute, hour or even the next trading day!

    For this project we will be using the libraries below:
    sklearn (for the machine learning prediction)
    pandas (for handling our data)
    yahoo_fin (for getting the stock prices of a specific symbol)
     
    We will be doing this project in python3, so set up your python environment!
    Let's name our python file, stockPredictor.py.
    Open the terminal and type:
    pip install sklearn
    pip install pandas
    pip install yahoo_fin

    Now lets get coding, our goal is to predict to see if the AAPL stock price is going to close higher or lower the next trading day!
    So let's get coding!

    from sklearn.svm import SVR
    import pandas as pd
    from yahoo_fin.stock_info import get_data

    #We need to set up our dataframe
    #We will be only working with the past 5 years closing prices of every trading day
    df = get_data('AAPL')
    if len(df)>=1260: df = df.iloc[-1260:]

    #For every single data we have we also want to have an index so later on we could call the prediction based on its index
    indices = [[index] for index in range(len(df))]

    #Let's get all the closing prices in our dataframe and make sure they are all floats
    df_close = df.loc[:, 'close']
    close_prices = [float(close_price) for close_price in df_close]

    #Let's set up our machine learning predictor, we will be using the radial basis function which goes by RBF, there are also linear, and polynomial methods but from personal experience RBF works the best in this case!
    rbf_svr = SVR(kernel='rbf', C=1000.0, gamma=0.15)

    #Let's now feed our machine learning some data to predict!
    rbf_svr.fit(indices, close_prices)

    #And that's it! We are all done! All we need to do is to call the index we want to see the pridiction for and we could check tomorrow after the trading day closes to see if the predictin was correct or not!
    predectedToCloseTomorrow = rbf_svr.predict([[len(df)]])[0] #len(df), represents the next day's predicted price index
    predectedToCloseToday = rbf_svr.predict([[len(df)-1]])[0] #represents today's predicted price index

    #We could even calculate the percentage growth to see if the price will be going higher or lower.
    #The function below calculates the percentage growth for use all we need to do is to call it!
    def growthRate(pre, curr): return ((100*curr)/pre)-100

    #And now let's call the growth rate function to see if the stock price is going up or down tomorrow!
    closingRate = growthRate(predectedToCloseToday, predectedToCloseTomorrow)

    #We are all done let's print the closing rate!
    print('The AAPL stock is predicted to close at %', '{:.3f}'.format(closingRate), 'the next trading day.')

'''
