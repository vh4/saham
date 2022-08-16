import yfinance as yf
import pandas as pd
import time

def DataframeToLayer(stockList):
    print("running dataframe to layer.......")
    layerList = list()
    print("waiting for market cap.......")
    for stock in stockList:
        marketCap = yf.Ticker(stock + ".jk").info["marketCap"]  
        #First Level
        if (marketCap >= 10**13):
            layerList.append("LAYER_1")
        elif marketCap >= 2*10**12 and marketCap < 10**13:
            layerList.append("LAYER_2")
        elif marketCap < 2*10**12:
            layerList.append("LAYER_3")
        else:
            layerList.append("undefined")
        print(layerList)
    
    layerData = {
    "Ticker Code": stockList,
    "Stock Layer": layerList
    }

    layerDataFrame = pd.DataFrame(layerData)
    return layerDataFrame

def StockFraction(stockList):
    print("running stock fraction.......")
    stockFractions = list()

    # Use yf module to get stock data
    for stock in stockList:
        temp = yf.download(stock + '.JK',period = '1d', interval = '1d')
        
        # if 'Close' column in temp < 200 then 'Fraction' Column is 1
        temp.loc[(temp['Close'] < 200), 'Fraction'] = 'Fraksi_1'
    
        # if 'Close' Column > 200 and 'Close' Column < 500 then 'Fraction' Column is 2
        temp.loc[(temp['Close'] > 200) & (temp['Close'] < 500), 'Fraction'] = 'Fraksi_2'
    
        # if 'Close' Column > 500 and 'Close' Column < 2000 then 'Fraction' Column is 3
        temp.loc[(temp['Close'] > 500) & (temp['Close'] < 2000), 'Fraction'] = 'Fraksi_3'
        
        # if 'Close' Column > 2000 and 'Close' Column < 5000 then 'Fraction' Column is 4
        temp.loc[(temp['Close'] > 2000) & (temp['Close'] < 5000), 'Fraction'] = 'Fraksi_4'
        
        # if 'Close' Column > 5000 'Fraction' Column is 5
        temp.loc[temp['Close'] > 5000, 'Fraction'] = 'Fraksi_5'

        stockFractions.append(temp)
    return stockFractions
    