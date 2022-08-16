import yfinance as yf
import pandas as pd
import os
import time

#scrapping stock data from yahoo finance
def Scrapping():
    stockList = ["ANTM","TLKM","BMRI","BBNI","ADRO","SIDO","TBIG",
             "ARNA","TGKA","HEXA",
             "ALMI","ADMG","LTLS","INOV",
             "EXCL","ICBP","ISAT","SCMA","TOWR","UNVR",
             "BEST","DMAS","PTBA","DOID","KLBF","MPMX","MEGA",
             "ASII","BBTN","BNGA",]
    stockObjectList = list()

    for stock in stockList:
        temp = yf.download(stock + '.JK',start = "2019-01-01",end = "2019-12-31")
        stockObjectList.append(temp)
    print(temp)
        
    time.sleep(2)

    return stockObjectList, stockList

#create path folder for simulation stock data
def CreatePathSimulation():
    
    # Check if the path exist
    path1 = "Log/Simulation/"
    path2 = "Log/Summary/"
    path3 = "Data/"
    path4 = "Log/Simulation/Layer/"
    path5 = "Log/Stocks/"

    if os.path.exists(path1):   
        print(path1,"is exists!")
    else:
        print("Creating the",path1,"Path....")
        os.makedirs(path1)

    if os.path.exists(path2):
        print(path2,"is exists!")
    else:
        print("Creating the",path2,"Path....")
        os.makedirs(path2)

    if os.path.exists(path3):
        print(path3,"is exists!")
    else:
        print("Creating the",path3,"Path....")
        os.makedirs(path3)

    if os.path.exists(path4):
        print(path4,"is exists!")
    else:
        print("Creating the",path4,"Path....")
        os.makedirs(path4)

    if os.path.exists(path5):
        print(path5,"is exists!")
    else:
        print("Creating the",path5,"Path....")
        os.makedirs(path5)


    