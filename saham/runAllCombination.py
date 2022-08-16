import yfinance as yf
import pandas as pd
import time
import sys

from saham.scrapping.scrapping import Scrapping, CreatePathSimulation
from saham.dataframeTolayer import DataframeToLayer, StockFraction

from saham.indikator.mfiiIndikator import MFIIndicator
from saham.indikator.bbIndikator import BollingerBands
from saham.indikator.soIndikator import StochasticOscillator
from saham.indikator.ccIndikator import CCIIndicator


###### One Combination ######

#Create a list to later store it into dictionary format
stockSymbolList = list()
initialCapitalList = list()
orderListDicts = list()
totalProfitList = list()
profitPercentageList = list()
totalTaxList = list()
numberPurchaseList = list()
numberSellList = list()
indicatorColumnList = list()
    

def OneCombination(firstStock):

    # Unbox the firstStock
    indicatorColumn2 = False
    indicatorColumn3 = False

    try:
        stock = firstStock[0]
        # print(1)
        stockSymbol = firstStock[1]
        # print(2)
        signalColumn = firstStock[2]
        # print(3)
        indicatorColumn = firstStock[3]
        # print(4)
        indicatorColumn2 = firstStock[4]
        # print(5)
        indicatorColumn3 = firstStock[5]
        # print(6)

    except Exception as e:
        # Handle nothing just bypass the error
        # print(e)
        pass
    
    # Trading Simulation
    # Declare variable to check if we already owned the stock or not
    isOwned = False
    # Declare variable for storing total profit
    totalProfit = 0
    # Declare variable for storing current closing price on current loop
    currentPrice = 0
    # Declare variable for storing how much we purchased the stock
    numberPurchase = 0
    # Declare variable for storing how much we sell the stock
    numberSell = 0
    # Declare variable for storing initial Capital price
    initialCapital = 0
    # Declare variable for storing total tax we payed
    totalTax = 0
    # Declare variable for storing how many loop that we did
    i = 0

    # Create list for storing every simulation values
    indexList = list()
    closePriceList = list()
    taxList = list()
    orderList = list()
    purchasedPriceList = list()
    profitList = list()
    signalList = list()
    # Check if second indicator exists then create the list
    if type(indicatorColumn2) == type("String"):
        signalList2 = list()
        signalList3 = list()

    # use itterows method to iterate the Data Frame for A AND B Condition
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[signalColumn] == "BUY":
                orderList.append("BUY")
                
                try:
                    signalList.append(row[indicatorColumn])
                    #print("MARK 4")
                    # Check if second indicator exist
                    signalList2.append(row[indicatorColumn2])
                    #Check is third indicator exist
                    signalList3.append(row[indicatorColumn3])
                    
                except Exception as e:
                    # print(e)
                    pass

                # assign the current price
                currentPrice = row["Close"] * 100
                closePriceList.append(currentPrice)

                # Calculate the tax
                tax = currentPrice * 0.36 / 100
                tax = int(tax)
                taxList.append(tax)
                totalTax = totalTax + tax

                # Calculate total buy price
                buyPrice = currentPrice + tax
                purchasedPriceList.append(buyPrice)
                profitList.append(0)

                # Check if initial capital is 0 then assign the buy price to the initialCapital variable
                if initialCapital == 0:
                    initialCapital = buyPrice
                # Change the boolean to True, to indicate we already own the stock
                isOwned = True
                # add one to the number purchased
                numberPurchase = numberPurchase + 1
                i = i + 1
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[signalColumn] == "SELL":
                # Append the SELL signal
                orderList.append("SELL")

                #Append Indicator column(s) with workaround for multiple
                #columns
                try:
                    signalList.append(row[indicatorColumn])
                    # Check if second indicator exist
                    # indicatorTemp2 = row[indicatorColumn2]
                    signalList2.append(row[indicatorColumn2])
                    #Check is third indicator exist
                    # indicatorTemp3 = row[indicatorColumn3]
                    signalList3.append(row[indicatorColumn3])

                except Exception as e:
                    pass
                    # print(e)

                # Temp variable to store the current price
                tempPrice = row["Close"] * 100
                closePriceList.append(tempPrice)

                # calculate the tax
                tax = tempPrice * 0.46 / 100
                tax = int(tax)
                taxList.append(tax)
                totalTax = totalTax + tax

                # Calculate total sell price
                sellPrice = tempPrice - tax
                purchasedPriceList.append(buyPrice)

                # calc the profit by subtract it with the purchase value
                profit = sellPrice - buyPrice
                profitList.append(profit)
                # add to total profit
                totalProfit = totalProfit + profit

                # Change the boolean to False, to indicate that we don't own the stock anymore
                isOwned = False
                numberSell = numberSell + 1
                i = i + 1
                indexList.append(index)
    # print("MARK 8")
    orderName = indicatorColumn.split("_")
    orderName = orderName[0]
    # Create a Dictionary to store the Simulation Data
    simulationLogDict = dict()

    try:
        # Add all the data to the dict
        simulationLogDict["Date"] = indexList
        simulationLogDict["Close Price"] = closePriceList
        simulationLogDict["Fee"] = taxList
        simulationLogDict["Purchased Price"] = purchasedPriceList
        simulationLogDict["Capital Gain"] = profitList
        simulationLogDict[orderName] = orderList
        #print("MARK 9")
        simulationLogDict[indicatorColumn] = signalList
        #print("MARK 10")
        simulationLogDict[indicatorColumn2] = signalList2
        simulationLogDict[indicatorColumn3] = signalList3
                            
    except Exception as e:
        # print(e)
        pass

    indicatorName = indicatorColumn
    #Convert the dict to dataframe and save it to CSV
    simulationLog = pd.DataFrame(simulationLogDict)
    #print("MARK 12")
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
    simulationLog.to_csv(simulationPath)
    print(stockSymbol,"simulation stored in :",simulationPath)
    
    # SIMULATION SUMMARY
    # Calculate the profit in percentage
    try:
        profitPercentage = totalProfit / initialCapital * 100
        profitPercentage = int(profitPercentage)
    except:
        profitPercentage = 0

    # Append the simulation summary to the lists for later use
    stockSymbolList.append(stockSymbol)
    initialCapitalList.append(initialCapital)
    totalProfitList.append(totalProfit)
    profitTemp = profitPercentage
    profitPercentageList.append(profitTemp)
    totalTaxList.append(totalTax)
    numberPurchaseList.append(numberPurchase)
    numberSellList.append(numberSell)
    orderListDicts.append(simulationLogDict[orderName])
    indicatorColumnList.append(indicatorName)
    #print("MARK 13")


#### Two Combination ####
 
stockSymbolList = list()
initialCapitalList = list()  
totalProfitList = list()
profitPercentageList = list()
totalTaxList = list()
numberPurchaseList = list()
numberSellList = list()
indicatorColumnList = list()

def RunTwoCombination_AND(firstStock, secondStock):
    # Unbox the firstStock
    indicatorColumn2 = False
    indicatorColumn3 = False

    indicatorColumn2_2 = False
    indicatorColumn3_2 = False

    indexList = list()
    closePriceList = list()
    taxList = list()
    orderList = list()
    orderList_2 = list()
    purchasedPriceList = list()
    profitList = list()
    signalList = list()

    try:
        stock = firstStock[0]
        # print(1)
        stockSymbol = firstStock[1]
        # print(2)
        signalColumn = firstStock[2]
        # print(3)
        indicatorColumn = firstStock[3]
        # print(4)
        indicatorColumn2 = firstStock[4]
        # print(5)
        indicatorColumn3 = firstStock[5]
        # print(6)
        # print("ALL")

    except Exception as e:
        # Handle nothing just bypass the error
        # print(e)
        pass
    try:
        stock_2 = secondStock[0]
        # print(1)
        stockSymbol_2 = secondStock[1]
        # print(2)
        signalColumn_2 = secondStock[2]
        # print(3)
        indicatorColumn_2 = secondStock[3]
        # print(4)
        indicatorColumn2_2 = secondStock[4]
        # print(5)
        indicatorColumn3_2 = secondStock[5]
        # print(6)
        #print("MARK 2")

    except Exception as e:
        # Handle nothing just bypass the error
        # print(e)
        pass
    
    # Trading Simulation
    # Declare variable to check if we already owned the stock or not
    isOwned = False
    # Declare variable for storing total profit
    totalProfit = 0
    # Declare variable for storing current closing price on current loop
    currentPrice = 0
    # Declare variable for storing how much we purchased the stock
    numberPurchase = 0
    # Declare variable for storing how much we sell the stock
    numberSell = 0
    # Declare variable for storing initial Capital price
    initialCapital = 0
    # Declare variable for storing total tax we payed
    totalTax = 0
    # Declare variable for storing how many loop that we did
    i = 0

    # Check if second indicator exists then create the list
    if type(indicatorColumn2) == type("String"):
        signalList2 = list()
        signalList3 = list()
    #print("MARK 3")
    
    signalList_2 = list()
        # Check if second indicator exists then create the list
    if type(indicatorColumn2_2) == type("String"):
        signalList2_2 = list()
        signalList3_2 = list()
        # print("MARK 3 Optional")


    #Transaction Fee
    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))

    # use itterows method to iterate the Data Frame for A AND B Condition
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[signalColumn] == "BUY" and row[signalColumn_2] == "BUY":
                orderList.append("BUY")
                orderList_2.append("BUY")
                
                try:
                    signalList.append(row[indicatorColumn])
                    #print("MARK 4")
                    # Check if second indicator exist
                    signalList2.append(row[indicatorColumn2])
                    #Check is third indicator exist
                    signalList3.append(row[indicatorColumn3])
                    
                except Exception as e:
                    # print(e)
                    pass
                try:   
                    signalList_2.append(row[indicatorColumn_2])
                    # Check if second indicator exist
                    signalList2_2.append(row[indicatorColumn2_2])
                    #Check is third indicator exist
                    signalList3_2.append(row[indicatorColumn3_2])
                    #print("MARK 5")
                except Exception as e:
                    #print(e)
                    pass
                # assign the current price
                currentPrice = row["Close"] * 100
                closePriceList.append(currentPrice)

                # Calculate the tax
                tax = currentPrice * 0.36 / 100
                tax = int(tax)
                taxList.append(tax)
                totalTax = totalTax + tax

                # Calculate total buy price
                buyPrice = currentPrice + tax
                purchasedPriceList.append(buyPrice)
                profitList.append(0)

                # Check if initial capital is 0 then assign the buy price to the initialCapital variable
                if initialCapital == 0:
                    initialCapital = buyPrice
                # Change the boolean to True, to indicate we already own the stock
                isOwned = True
                # add one to the number purchased
                numberPurchase = numberPurchase + 1
                i = i + 1
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[signalColumn] == "SELL" and row[signalColumn_2] == 'SELL':
                # Append the SELL signal
                orderList.append("SELL")
                orderList_2.append("SELL")

                #Append Indicator column(s) with workaround for multiple
                #columns
                try:
                    signalList.append(row[indicatorColumn])
                    #print("MARK 6")
                    # Check if second indicator exist
                    # indicatorTemp2 = row[indicatorColumn2]
                    signalList2.append(row[indicatorColumn2])
                    #Check is third indicator exist
                    # indicatorTemp3 = row[indicatorColumn3]
                    signalList3.append(row[indicatorColumn3])

                except Exception as e:
                    pass
                    # print(e)

                try:
                    signalList_2.append(row[indicatorColumn_2])
                    # Check if second indicator exist
                    signalList2_2.append(row[indicatorColumn2_2])
                    #Check is third indicator exist
                    signalList3_2.append(row[indicatorColumn3_2])
                    #print("MARK 7")
                except Exception as e:
                    pass
                    # print(e)

                # Temp variable to store the current price
                tempPrice = row["Close"] * 100
                closePriceList.append(tempPrice)

                # calculate the tax
                tax = tempPrice * 0.46 / 100
                tax = int(tax)
                taxList.append(tax)
                totalTax = totalTax + tax

                # Calculate total sell price
                sellPrice = tempPrice - tax
                purchasedPriceList.append(buyPrice)

                # calc the profit by subtract it with the purchase value
                profit = sellPrice - buyPrice
                profitList.append(profit)
                # add to total profit
                totalProfit = totalProfit + profit

                # Change the boolean to False, to indicate that we don't own the stock anymore
                isOwned = False
                numberSell = numberSell + 1
                i = i + 1
                indexList.append(index)
    # print("MARK 8")
    orderName = indicatorColumn.split("_")
    orderName = orderName[0]
    orderName_2 = indicatorColumn_2.split("_")
    orderName_2 = orderName_2[0]
    # Create a Dictionary to store the Simulation Data
    simulationLogDict = dict()

    try:
        # Add all the data to the dict
        simulationLogDict["Date"] = indexList
        simulationLogDict["Close Price"] = closePriceList
        simulationLogDict["Fee"] = taxList
        simulationLogDict["Purchased Price"] = purchasedPriceList
        simulationLogDict["Capital Gain"] = profitList
        simulationLogDict[orderName] = orderList
        simulationLogDict[orderName_2] = orderList_2
        #print("MARK 9")
        simulationLogDict[indicatorColumn] = signalList
        #print("MARK 10")
        simulationLogDict[indicatorColumn2] = signalList2
        simulationLogDict[indicatorColumn3] = signalList3
                            
    except Exception as e:
        # print(e)
        pass

    try:
        simulationLogDict[indicatorColumn_2] = signalList_2
        #print("MARK 11 START")
        simulationLogDict[indicatorColumn2_2] = signalList2_2
        simulationLogDict[indicatorColumn3_2] = signalList3_2
        #print("MARK 11 END")
    except Exception as e:
        # print(e)
        pass

    indicatorName = indicatorColumn + "_AND_" + indicatorColumn_2
    #Convert the dict to dataframe and save it to CSV
    simulationLog = pd.DataFrame(simulationLogDict)
    #print("MARK 12")
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
    simulationLog.to_csv(simulationPath)
    print(stockSymbol,"simulation stored in :",simulationPath)
    
    # SIMULATION SUMMARY
    #Calculate the profit in percentage
    try:
        profitPercentage = totalProfit / initialCapital * 100
        profitPercentage = int(profitPercentage)
    except:
        profitPercentage = 0

    # Append the simulation summary to the lists for later use
    stockSymbolList.append(stockSymbol)
    initialCapitalList.append(initialCapital)
    totalProfitList.append(totalProfit)
    profitTemp = profitPercentage
    profitPercentageList.append(profitTemp)
    totalTaxList.append(totalTax)
    numberPurchaseList.append(numberPurchase)
    numberSellList.append(numberSell)

    indicatorColumnList.append(indicatorName)
    #print("MARK 13")

# (stock,stockSymbol,signalColumn,indicatorColumn,indicatorColumn2 = None,indicatorColumn3 = None):
# firstStock = ["OBJ","TLKM","BUY","RSI_1","RSI_2"]
# secondStock = ["Stock_Object","TLKM","BUY","OBV_1","OBV_2","OBV_3"]
# two = []

def RunTwoCombination_OR(firstStock, secondStock):
    # Unbox the firstStock
    indicatorColumn2 = False
    indicatorColumn3 = False

    indicatorColumn2_2 = False
    indicatorColumn3_2 = False
    try:
        stock = firstStock[0]
        # print(1)
        stockSymbol = firstStock[1]
        # print(2)
        signalColumn = firstStock[2]
        # print(3)
        indicatorColumn = firstStock[3]
        # print(4)
        # print("MARK 1")
        indicatorColumn2 = firstStock[4]
        # print(5)
        indicatorColumn3 = firstStock[5]
        # print(6)
        # print("ALL")

    except Exception as e:
        # Handle nothing just bypass the error
        #print(e)
        pass
    # Unbox the secondStock
    try:
        stock_2 = firstStock[0]
            # print(1)
        stockSymbol_2 = secondStock[1]
            # print(2)
        signalColumn_2 = secondStock[2]
            # print(3)
        indicatorColumn_2 = secondStock[3]
            # print(4)
        indicatorColumn2_2 = secondStock[4]
            # print(5)
        indicatorColumn3_2 = secondStock[5]
            # print(6)
        # print("MARK 2")

    except Exception as e:
        # Handle nothing just bypass the error
        print(e)
    
    # Trading Simulation
    # Declare variable to check if we already owned the stock or not
    isOwned = False
    # Declare variable for storing total profit
    totalProfit = 0
    # Declare variable for storing current closing price on current loop
    currentPrice = 0
    # Declare variable for storing how much we purchased the stock
    numberPurchase = 0
    # Declare variable for storing how much we sell the stock
    numberSell = 0
    # Declare variable for storing initial Capital price
    initialCapital = 0
    # Declare variable for storing total tax we payed
    totalTax = 0
    # Declare variable for storing how many loop that we did
    i = 0

    # Create list for storing every simulation values
    indexList = list()
    closePriceList = list()
    taxList = list()
    orderList = list()
    orderList_2 = list()
    purchasedPriceList = list()
    profitList = list()
    signalList = list()
 
    #Transaction Fee
    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))

        # use itterows method to iterate the Data Frame for A AND B Condition
    for index, row in stock.iterrows():
        # Check if we don't own the stock then buy one
        if isOwned == False:
            if row[signalColumn] == "BUY" or row[signalColumn_2] == "BUY":
                if row[signalColumn] == "BUY":
                    orderList.append("BUY")
                    orderList_2.append(" ")
                else:
                    orderList.append(" ")
                    orderList_2.append("BUY")
                try:
                    signalList.append(row[indicatorColumn])
                    # print("MARK 4")
                    # Check if second indicator exist
                    signalList2.append(row[indicatorColumn2])
                    #Check is third indicator exist
                    signalList3.append(row[indicatorColumn3])
                    
                except Exception as e:
                    # print(e)
                    pass

                try:   
                    signalList_2.append(row[indicatorColumn_2])
                    # Check if second indicator exist
                    signalList2_2.append(row[indicatorColumn2_2])
                    #Check is third indicator exist
                    signalList3_2.append(row[indicatorColumn3_2])
                    # print("MARK 5")
                except Exception as e:
                    # print(e)
                    pass
                # assign the current price
                currentPrice = row["Close"] * 100
                closePriceList.append(currentPrice)

                # Calculate the tax
                tax = currentPrice * 0.36 / 100
                tax = int(tax)
                taxList.append(tax)
                totalTax = totalTax + tax

                # Calculate total buy price
                buyPrice = currentPrice + tax
                purchasedPriceList.append(buyPrice)
                profitList.append(0)

                # Check if initial capital is 0 then assign the buy price to the initialCapital variable
                if initialCapital == 0:
                    initialCapital = buyPrice
                # Change the boolean to True, to indicate we already own the stock
                isOwned = True
                # add one to the number purchased
                numberPurchase = numberPurchase + 1
                i = i + 1
                indexList.append(index)
            # Unused else, maybe for further update (?) log : R To Do List
            else:
                pass
        else:
            # If we own the stock, and the signal is SELL then sell the stock
            if row[signalColumn] == "SELL" or row[signalColumn_2] == 'SELL':
                # Append the SELL signal
                if row[signalColumn] == "SELL":
                    orderList.append("SELL")
                    orderList_2.append(" ")
                else:
                    orderList.append(" ")
                    orderList_2.append("SELL")

                #Append Indicator column(s) with workaround for multiple
                #columns
                try:
                    signalList.append(row[indicatorColumn])
                    # print("MARK 6")
                    # Check if second indicator exist
                    signalList2.append(row[indicatorColumn2])
                    #Check is third indicator exist
                    signalList3.append(row[indicatorColumn3])

                except Exception as e:
                    pass
                    # print(e)

                try:
                    signalList_2.append(row[indicatorColumn_2])
                    # Check if second indicator exist
                    # indicatorTemp2_2 = row[indicatorColumn2_2]
                    signalList2_2.append(row[indicatorColumn2_2])
                    #Check is third indicator exist
                    signalList3_2.append(row[indicatorColumn3_2])
                    # print("MARK 7")
                except Exception as e:
                    pass
                    # print(e)

                # Temp variable to store the current price
                tempPrice = row["Close"] * 100
                closePriceList.append(tempPrice)

                # calculate the tax
                tax = tempPrice * 0.46 / 100
                tax = int(tax)
                taxList.append(tax)
                totalTax = totalTax + tax

                # Calculate total sell price
                sellPrice = tempPrice - tax
                purchasedPriceList.append(buyPrice)

                # calc the profit by subtract it with the purchase value
                profit = sellPrice - buyPrice
                profitList.append(profit)
                # add to total profit
                totalProfit = totalProfit + profit

                # Change the boolean to False, to indicate that we don't own the stock anymore
                isOwned = False
                numberSell = numberSell + 1
                i = i + 1
                indexList.append(index)
    # print("MARK 8")
    orderName = indicatorColumn.split("_")
    orderName = orderName[0]
    orderName_2 = indicatorColumn_2.split("_")
    orderName_2 = orderName_2[0]
    # Create a Dictionary to store the Simulation Data
    simulationLogDict = dict()

    try:
        # Add all the data to the dict
        simulationLogDict["Date"] = indexList
        simulationLogDict["Close Price"] = closePriceList
        simulationLogDict["Fee"] = taxList
        simulationLogDict["Purchased Price"] = purchasedPriceList
        simulationLogDict["Capital Gain"] = profitList
        simulationLogDict[orderName] = orderList
        simulationLogDict[orderName_2] = orderList_2
        # print("MARK 9")
        simulationLogDict[indicatorColumn] = signalList
        # print("MARK 10")
        simulationLogDict[indicatorColumn2] = signalList2
        simulationLogDict[indicatorColumn3] = signalList3
                            
    except Exception as e:
        # print(e)
        pass

    try:
        simulationLogDict[indicatorColumn_2] = signalList_2
        # print("MARK 11 START")
        simulationLogDict[indicatorColumn2_2] = signalList2_2
        simulationLogDict[indicatorColumn3_2] = signalList3_2
        # print("MARK 11 END")
    except Exception as e:
        # print(e)
        pass

    indicatorName = indicatorColumn + "_OR_" + indicatorColumn_2
    #Convert the dict to dataframe and save it to CSV
    simulationLog = pd.DataFrame(simulationLogDict)
    # print("MARK 12")
    simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
    simulationLog.to_csv(simulationPath)
    print(stockSymbol,"simulation stored in :",simulationPath)
    
    #Calculate the profit in percentage
    try:
        profitPercentage = totalProfit / initialCapital * 100
        profitPercentage = int(profitPercentage)
    except:
        profitPercentage = 0

    # Append the simulation summary to the lists for later use
    stockSymbolList.append(stockSymbol)
    initialCapitalList.append(initialCapital)
    totalProfitList.append(totalProfit)
    profitTemp = profitPercentage
    profitPercentageList.append(profitTemp)
    totalTaxList.append(totalTax)
    numberPurchaseList.append(numberPurchase)
    numberSellList.append(numberSell)
    indicatorColumnList.append(indicatorName)

#### Three Combinations ####

# Empty all the list for the summary (for combination 3)

stockSymbolList = list()
initialCapitalList = list()
totalProfitList = list()
profitPercentageList = list()
totalTaxList = list()   
numberPurchaseList = list()
numberSellList = list()  
indicatorColumnList = list()

def RunThreeCombination_AND(firstStock, secondStock, threeStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False
  
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  purchasedPriceList = list()
  profitList = list()
  signalList = list()

  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()
      #print("MARK 4 Optional")

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 5 Optional")

  signalList_3 = list()
  # Check if three indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 6 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" and row[signalColumn_2] == "BUY" and row[signalColumn_3] == "BUY":
          
        orderList.append("BUY")
        orderList_2.append('BUY')
        orderList_3.append("BUY")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 7")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 8")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 9")
          pass

        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 10")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" and row[signalColumn_2] == "SELL" and row[signalColumn_3] == "SELL":
        
        orderList.append("SELL")
        orderList_2.append('SELL')
        orderList_3.append("SELL")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 11")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 12")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 13")
          pass
          
        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 14")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]
  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 15")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 16")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 17")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_AND_" + indicatorColumn_2 + "_AND_" + indicatorColumn_3
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)

  indicatorColumnList.append(indicatorName)
  #print("MARK 18") 

#function X OR X OR X

def RunThreeCombination_OR(firstStock, secondStock, threeStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False
  
  #define for indicatior 3
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
  
  #define for indicatior 3
  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  #define for indicatior 3
  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if three indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

    #Transaction Fee
    # BUY Fee => 0.36% (Broker Fee(0.19%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))
    # SELL Fee => 0.46% (Broker Fee(0.29%) + Levy(0.04%) + PPN(0.03%) + PPh(0.1%))

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" or row[signalColumn_2] == "BUY" or row[signalColumn_3] == "BUY":

        #condition 1
        if row[signalColumn] == "BUY":
          orderList.append("BUY")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "BUY":
          orderList_2.append("BUY")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "BUY":
          orderList_3.append("BUY")
        else:
          orderList_3.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 6")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 7")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 8")
          pass
        

        #assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100

        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
       # print("MARK 9")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" or row[signalColumn_2] == "SELL" or row[signalColumn_3] == "SELL":
        
        #condition 1
        if row[signalColumn] == "SELL":
          orderList.append("SELL")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "SELL":
          orderList_2.append("SELL")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "SELL":
          orderList_3.append("SELL")
        else:
          orderList_3.append(" ")
        
        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 10")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 11")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        # Temp variable to store the current price
        
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        
        #if math.isnan(tax) == True:
          #tax = 0
        
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 13")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]
  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 13")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 14")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 15")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_OR_" + indicatorColumn_2 + "_OR_" + indicatorColumn_3
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)

  indicatorColumnList.append(indicatorName)
  #print("MARK 16") 

#function X AND X OR X

def RunThreeCombination_AND_OR(firstStock, secondStock, threeStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False
  
  #define for indicator 1
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  #define for indicator 2
  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  #define for indicator 3
  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if three indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" and row[signalColumn_2] == "BUY" or row[signalColumn_3] == "BUY":
        
        #condition 1
        if row[signalColumn] == "BUY":
          orderList.append("BUY")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "BUY":
          orderList_2.append("BUY")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "BUY":
          orderList_3.append("BUY")
        else:
          orderList_3.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 6")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 7")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 8")
          pass

        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 9")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" and row[signalColumn_2] == "SELL" or row[signalColumn_3] == "SELL":
        
        #condition 1
        if row[signalColumn] == "SELL":
          orderList.append("SELL")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "SELL":
          orderList_2.append("SELL")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "SELL":
          orderList_3.append("SELL")
        else:
          orderList_3.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 10")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 11")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 13")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]
  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print(e)
    #print("MARK 14")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print(e)
    #print("MARK 15")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print(e)
    #print("MARK 16")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_AND_" + indicatorColumn_2 + "_OR_" + indicatorColumn_3
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  # SIMULATION SUMMARY
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0

  # Append the simulation summary to the lists for later use  
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList.append(indicatorName)
  #print("MARK 17")

#function X OR X AND X

def RunThreeCombination_OR_AND(firstStock, secondStock, threeStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False
  
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if three indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" or row[signalColumn_2] == "BUY" and row[signalColumn_3] == "BUY":
        
        #condition 1
        if row[signalColumn] == "BUY":
          orderList.append("BUY")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "BUY":
          orderList_2.append("BUY")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "BUY":
          orderList_3.append("BUY")
        else:
          orderList_3.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 6")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 7")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 8")
          pass

        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 9")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" or row[signalColumn_2] == "SELL" and row[signalColumn_3] == "SELL":
        
        #condition 1
        if row[signalColumn] == "SELL":
          orderList.append("SELL")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "SELL":
          orderList_2.append("SELL")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "SELL":
          orderList_3.append("SELL")
        else:
          orderList_3.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 10")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 11")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 13")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]
  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 14")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 15")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 16")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_OR_" + indicatorColumn_2 + "_AND_" + indicatorColumn_3
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  # SIMULATION SUMMARY
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0  

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList.append(indicatorName)
  #print("MARK 17")

#### Four Combination #####
#function X AND X AND X AND X

# Empty all the list for the summary (for combination 4)

stockSymbolList = list()
initialCapitalList = list()
totalProfitList = list()
profitPercentageList = list()
totalTaxList = list()   
numberPurchaseList = list()
numberSellList = list()  
indicatorColumnList = list()

def RunFourCombination_AND(firstStock, secondStock, threeStock, fourStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False

  indicatorColumn4_4 = False
  indicatorColumn5_4 = False
  
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_4 = fourStock[0]
    stockSymbol_4 = fourStock[1]
    signalColumn_4 = fourStock[2]
    indicatorColumn_4 = fourStock[3]
    indicatorColumn4_4 = fourStock[4]
    indicatorColumn5_4 = fourStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  orderList_4 = list()
  
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

  signalList_4 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn4_4) == type("String"):
      signalList4_4 = list()
      signalList5_4 = list()
      #print("MARK 6 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" and row[signalColumn_2] == "BUY" and row[signalColumn_3] == "BUY" and row[signalColumn_4] == "BUY":
        
        orderList.append("BUY")
        orderList_2.append("BUY")
        orderList_3.append("BUY")
        orderList_4.append("BUY")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
        except Exception as e:
          #print("MARK 7")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is second indicator exist
          signalList3_2.append(row[indicatorColumn3_2])      
        except Exception as e:
          #print("MARK 8")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is second indicator exist
          signalList4_3.append(row[indicatorColumn4_3])       
        except Exception as e:
          #print("MARK 9")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])       
        except Exception as e:
          #print("MARK 10")
          pass
        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 11")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" and row[signalColumn_2] == "SELL" and row[signalColumn_3] == "SELL" and row[signalColumn_4] == "SELL":
        
        orderList.append("SELL")
        orderList_2.append("SELL")
        orderList_3.append("SELL")
        orderList_4.append("SELL")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 13")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 14")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])
          
        except Exception as e:
          #print("MARK 15")
          pass

        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 16")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]

  orderName_4 = indicatorColumn_4.split("_")
  orderName_4 = orderName_4[0]

  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[orderName_4] = orderList_4   
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 17")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 18")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 19")
    pass

  try:
    simulationLogDict[indicatorColumn_4] = signalList_4
    simulationLogDict[indicatorColumn4_4] = signalList4_4
    simulationLogDict[indicatorColumn5_4] = signalList5_4
  except Exception as e:
    #print("MARK 20")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_AND_" + indicatorColumn_2 + "_AND_" + indicatorColumn_3 + "_AND_" + indicatorColumn_4
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  # SIMULATION SUMMARY
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0  

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList.append(indicatorName)
  #print("MARK 21")

#function X OR X OR X OR X

def RunFourCombination_OR(firstStock, secondStock, threeStock, fourStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False

  indicatorColumn4_4 = False
  indicatorColumn5_4 = False
  
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_4 = fourStock[0]
    stockSymbol_4 = fourStock[1]
    signalColumn_4 = fourStock[2]
    indicatorColumn_4 = fourStock[3]
    indicatorColumn4_4 = fourStock[4]
    indicatorColumn5_4 = fourStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  orderList_4 = list()
  
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

  signalList_4 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn4_4) == type("String"):
      signalList4_4 = list()
      signalList5_4 = list()
      #print("MARK 6 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" or row[signalColumn_2] == "BUY" or row[signalColumn_3] == "BUY" or row[signalColumn_4] == "BUY":
        
        #condition 1
        if row[signalColumn] == "BUY":
          orderList.append("BUY")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "BUY":
          orderList_2.append("BUY")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "BUY":
          orderList_3.append("BUY")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "BUY":
          orderList_4.append("BUY")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
        except Exception as e:
          #print("MARK 7")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is second indicator exist
          signalList3_2.append(row[indicatorColumn3_2])      
        except Exception as e:
          #print("MARK 8")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is second indicator exist
          signalList4_3.append(row[indicatorColumn4_3])       
        except Exception as e:
          #print("MARK 9")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])       
        except Exception as e:
          #print("MARK 10")
          pass
        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 11")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" or row[signalColumn_2] == "SELL" or row[signalColumn_3] == "SELL" or row[signalColumn_4] == "SELL":
        
        #condition 1
        if row[signalColumn] == "SELL":
          orderList.append("SELL")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "SELL":
          orderList_2.append("SELL")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "SELL":
          orderList_3.append("SELL")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "SELL":
          orderList_4.append("SELL")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 13")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 14")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])
          
        except Exception as e:
          #print("MARK 15")
          pass

        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 16")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]

  orderName_4 = indicatorColumn_4.split("_")
  orderName_4 = orderName_4[0]

  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[orderName_4] = orderList_4   
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 17")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 18")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 19")
    pass

  try:
    simulationLogDict[indicatorColumn_4] = signalList_4
    simulationLogDict[indicatorColumn4_4] = signalList4_4
    simulationLogDict[indicatorColumn5_4] = signalList5_4
  except Exception as e:
    #print("MARK 20")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_OR_" + indicatorColumn_2 + "_OR_" + indicatorColumn_3 + "_OR_" + indicatorColumn_4
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  # SIMULATION SUMMARY
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0  

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList.append(indicatorName)
  #print("MARK 21")

#function X AND X AND X OR X

def RunFourCombination_AND_AND_OR(firstStock, secondStock, threeStock, fourStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False

  indicatorColumn4_4 = False
  indicatorColumn5_4 = False
  
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_4 = fourStock[0]
    stockSymbol_4 = fourStock[1]
    signalColumn_4 = fourStock[2]
    indicatorColumn_4 = fourStock[3]
    indicatorColumn4_4 = fourStock[4]
    indicatorColumn5_4 = fourStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  orderList_4 = list()
  
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

  signalList_4 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn4_4) == type("String"):
      signalList4_4 = list()
      signalList5_4 = list()
      #print("MARK 6 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" and row[signalColumn_2] == "BUY" and row[signalColumn_3] == "BUY" or row[signalColumn_4] == "BUY":
        
        #condition 1
        if row[signalColumn] == "BUY":
          orderList.append("BUY")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "BUY":
          orderList_2.append("BUY")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "BUY":
          orderList_3.append("BUY")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "BUY":
          orderList_4.append("BUY")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
        except Exception as e:
          #print("MARK 7")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is second indicator exist
          signalList3_2.append(row[indicatorColumn3_2])      
        except Exception as e:
          #print("MARK 8")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is second indicator exist
          signalList4_3.append(row[indicatorColumn4_3])       
        except Exception as e:
          #print("MARK 9")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])       
        except Exception as e:
          #print("MARK 10")
          pass
        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 11")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" and row[signalColumn_2] == "SELL" and row[signalColumn_3] == "SELL" or row[signalColumn_4] == "SELL":
        
        #condition 1
        if row[signalColumn] == "SELL":
          orderList.append("SELL")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "SELL":
          orderList_2.append("SELL")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "SELL":
          orderList_3.append("SELL")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "SELL":
          orderList_4.append("SELL")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 13")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 14")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])
          
        except Exception as e:
          #print("MARK 15")
          pass

        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 16")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]

  orderName_4 = indicatorColumn_4.split("_")
  orderName_4 = orderName_4[0]

  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[orderName_4] = orderList_4   
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 17")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 18")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 19")
    pass

  try:
    simulationLogDict[indicatorColumn_4] = signalList_4
    simulationLogDict[indicatorColumn4_4] = signalList4_4
    simulationLogDict[indicatorColumn5_4] = signalList5_4
  except Exception as e:
    #print("MARK 20")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_AND_" + indicatorColumn_2 + "_AND_" + indicatorColumn_3 + "_OR_" + indicatorColumn_4
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  # SIMULATION SUMMARY
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0  

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList.append(indicatorName)
  #print("MARK 21")

#function X OR X OR X AND X

def RunFourCombination_OR_OR_AND(firstStock, secondStock, threeStock, fourStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False

  indicatorColumn4_4 = False
  indicatorColumn5_4 = False
  
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_4 = fourStock[0]
    stockSymbol_4 = fourStock[1]
    signalColumn_4 = fourStock[2]
    indicatorColumn_4 = fourStock[3]
    indicatorColumn4_4 = fourStock[4]
    indicatorColumn5_4 = fourStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  orderList_4 = list()
  
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

  signalList_4 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn4_4) == type("String"):
      signalList4_4 = list()
      signalList5_4 = list()
      #print("MARK 6 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" or row[signalColumn_2] == "BUY" or row[signalColumn_3] == "BUY" and row[signalColumn_4] == "BUY":
        
        #condition 1
        if row[signalColumn] == "BUY":
          orderList.append("BUY")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "BUY":
          orderList_2.append("BUY")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "BUY":
          orderList_3.append("BUY")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "BUY":
          orderList_4.append("BUY")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
        except Exception as e:
          #print("MARK 7")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is second indicator exist
          signalList3_2.append(row[indicatorColumn3_2])      
        except Exception as e:
          #print("MARK 8")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is second indicator exist
          signalList4_3.append(row[indicatorColumn4_3])       
        except Exception as e:
          #print("MARK 9")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])       
        except Exception as e:
          #print("MARK 10")
          pass
        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 11")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" or row[signalColumn_2] == "SELL" or row[signalColumn_3] == "SELL" and row[signalColumn_4] == "SELL":
        
        #condition 1
        if row[signalColumn] == "SELL":
          orderList.append("SELL")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "SELL":
          orderList_2.append("SELL")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "SELL":
          orderList_3.append("SELL")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "SELL":
          orderList_4.append("SELL")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 13")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 14")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])
          
        except Exception as e:
          #print("MARK 15")
          pass

        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 16")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]

  orderName_4 = indicatorColumn_4.split("_")
  orderName_4 = orderName_4[0]

  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[orderName_4] = orderList_4   
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 17")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 18")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 19")
    pass

  try:
    simulationLogDict[indicatorColumn_4] = signalList_4
    simulationLogDict[indicatorColumn4_4] = signalList4_4
    simulationLogDict[indicatorColumn5_4] = signalList5_4
  except Exception as e:
    #print("MARK 20")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_OR_" + indicatorColumn_2 + "_OR_" + indicatorColumn_3 + "_AND_" + indicatorColumn_4
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  # SIMULATION SUMMARY
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0  

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList.append(indicatorName)
  #print("MARK 21")

#function X AND X OR X OR X

def RunFourCombination_AND_OR_OR(firstStock, secondStock, threeStock, fourStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False

  indicatorColumn4_4 = False
  indicatorColumn5_4 = False
  
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_4 = fourStock[0]
    stockSymbol_4 = fourStock[1]
    signalColumn_4 = fourStock[2]
    indicatorColumn_4 = fourStock[3]
    indicatorColumn4_4 = fourStock[4]
    indicatorColumn5_4 = fourStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  orderList_4 = list()
  
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

  signalList_4 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn4_4) == type("String"):
      signalList4_4 = list()
      signalList5_4 = list()
      #print("MARK 6 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" and row[signalColumn_2] == "BUY" or row[signalColumn_3] == "BUY" or row[signalColumn_4] == "BUY":
        
        #condition 1
        if row[signalColumn] == "BUY":
          orderList.append("BUY")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "BUY":
          orderList_2.append("BUY")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "BUY":
          orderList_3.append("BUY")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "BUY":
          orderList_4.append("BUY")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
        except Exception as e:
          #print("MARK 7")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is second indicator exist
          signalList3_2.append(row[indicatorColumn3_2])      
        except Exception as e:
          #print("MARK 8")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is second indicator exist
          signalList4_3.append(row[indicatorColumn4_3])       
        except Exception as e:
          #print("MARK 9")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])       
        except Exception as e:
          #print("MARK 10")
          pass
        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 11")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" and row[signalColumn_2] == "SELL" or row[signalColumn_3] == "SELL" or row[signalColumn_4] == "SELL":
        
        #condition 1
        if row[signalColumn] == "SELL":
          orderList.append("SELL")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "SELL":
          orderList_2.append("SELL")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "SELL":
          orderList_3.append("SELL")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "SELL":
          orderList_4.append("SELL")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 13")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 14")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])
          
        except Exception as e:
          #print("MARK 15")
          pass

        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 16")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]

  orderName_4 = indicatorColumn_4.split("_")
  orderName_4 = orderName_4[0]

  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[orderName_4] = orderList_4   
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 17")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 18")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 19")
    pass

  try:
    simulationLogDict[indicatorColumn_4] = signalList_4
    simulationLogDict[indicatorColumn4_4] = signalList4_4
    simulationLogDict[indicatorColumn5_4] = signalList5_4
  except Exception as e:
    #print("MARK 20")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_AND_" + indicatorColumn_2 + "_OR_" + indicatorColumn_3 + "_OR_" + indicatorColumn_4
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  # SIMULATION SUMMARY
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0  

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList.append(indicatorName)
  #print("MARK 21")

#function X OR X AND X AND X

def RunFourCombination_OR_AND_AND(firstStock, secondStock, threeStock, fourStock):
  
  indicatorColumn2 = False
  indicatorColumn3 = False
  
  indicatorColumn2_2 = False
  indicatorColumn3_2 = False

  indicatorColumn3_3 = False
  indicatorColumn4_3 = False

  indicatorColumn4_4 = False
  indicatorColumn5_4 = False
  
  try:
    stock = firstStock[0]
    stockSymbol = firstStock[1]
    signalColumn = firstStock[2]
    indicatorColumn = firstStock[3]
    indicatorColumn2 = firstStock[4]
    indicatorColumn3 = firstStock[5]
    #print("MARK 1")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_2 = secondStock[0]
    stockSymbol_2 = secondStock[1]
    signalColumn_2 = secondStock[2]
    indicatorColumn_2 = secondStock[3]
    indicatorColumn2_2 = secondStock[4]
    indicatorColumn3_2 = secondStock[5]
    #print("MARK 2")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_3 = threeStock[0]
    stockSymbol_3 = threeStock[1]
    signalColumn_3 = threeStock[2]
    indicatorColumn_3 = threeStock[3]
    indicatorColumn3_3 = threeStock[4]
    indicatorColumn4_3 = threeStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass

  try:
    stock_4 = fourStock[0]
    stockSymbol_4 = fourStock[1]
    signalColumn_4 = fourStock[2]
    indicatorColumn_4 = fourStock[3]
    indicatorColumn4_4 = fourStock[4]
    indicatorColumn5_4 = fourStock[5]
    #print("MARK 3")
  except Exception as e:
    # Handle nothing just bypass the error
    pass
    
  # Trading Simulation
  # Declare variable to check if we already owned the stock or not
  isOwned = False
  # Declare variable for storing total profit
  totalProfit = 0
  # Declare variable for storing current closing price on current loop
  currentPrice = 0
  # Declare variable for storing how much we purchased the stock
  numberPurchase = 0
  # Declare variable for storing how much we sell the stock
  numberSell = 0
  # Declare variable for storing initial Capital price
  initialCapital = 0
  # Declare variable for storing total tax we payed
  totalTax = 0
  # Declare variable for storing how many loop that we did
  i = 0

  # Create list for storing every simulation values
  indexList = list()
  closePriceList = list()
  taxList = list()
  
  orderList = list()
  orderList_2 = list()
  orderList_3 = list()
  orderList_4 = list()
  
  purchasedPriceList = list()
  profitList = list()
  signalList = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2) == type("String"):
      signalList2 = list()
      signalList3 = list()

  signalList_2 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn2_2) == type("String"):
      signalList2_2 = list()
      signalList3_2 = list()
      #print("MARK 4 Optional")

  signalList_3 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn3_3) == type("String"):
      signalList3_3 = list()
      signalList4_3 = list()
      #print("MARK 5 Optional")

  signalList_4 = list()
  # Check if second indicator exists then create the list
  if type(indicatorColumn4_4) == type("String"):
      signalList4_4 = list()
      signalList5_4 = list()
      #print("MARK 6 Optional")

  for index, row in stock.iterrows():
    # Check if we don't own the stock then buy one
    if isOwned == False:
      if row[signalColumn] == "BUY" or row[signalColumn_2] == "BUY" and row[signalColumn_3] == "BUY" and row[signalColumn_4] == "BUY":
        
        #condition 1
        if row[signalColumn] == "BUY":
          orderList.append("BUY")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "BUY":
          orderList_2.append("BUY")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "BUY":
          orderList_3.append("BUY")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "BUY":
          orderList_4.append("BUY")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
        except Exception as e:
          #print("MARK 7")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is second indicator exist
          signalList3_2.append(row[indicatorColumn3_2])      
        except Exception as e:
          #print("MARK 8")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is second indicator exist
          signalList4_3.append(row[indicatorColumn4_3])       
        except Exception as e:
          #print("MARK 9")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])       
        except Exception as e:
          #print("MARK 10")
          pass
        # assign the current price
        currentPrice = row["Close"] * 100
        closePriceList.append(currentPrice)

        # Calculate the tax
        tax = currentPrice * 0.36 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total buy price
        buyPrice = currentPrice + tax
        purchasedPriceList.append(buyPrice)
        profitList.append(0)

        # Check if initial capital is 0 then assign the buy price to the initialCapital variable
        if initialCapital == 0:
          initialCapital = buyPrice
        # Change the boolean to True, to indicate we already own the stock
        isOwned = True
        # add one to the number purchased
        numberPurchase = numberPurchase + 1
        i = i + 1
        indexList.append(index)
        # Unused else, maybe for further update (?) log : R To Do List
        #print("MARK 11")
      else:
        pass
    else:
      if row[signalColumn] == "SELL" or row[signalColumn_2] == "SELL" and row[signalColumn_3] == "SELL" and row[signalColumn_4] == "SELL":
        
        #condition 1
        if row[signalColumn] == "SELL":
          orderList.append("SELL")
        else:
          orderList.append(" ")
        
        #condition 2
        if row[signalColumn_2] == "SELL":
          orderList_2.append("SELL")
        else:
          orderList_2.append(" ")
        
        #condition 3
        if row[signalColumn_3] == "SELL":
          orderList_3.append("SELL")
        else:
          orderList_3.append(" ")

        #condition 4
        if row[signalColumn_4] == "SELL":
          orderList_4.append("SELL")
        else:
          orderList_4.append(" ")

        try:
          signalList.append(row[indicatorColumn])
          # Check if second indicator exist
          signalList2.append(row[indicatorColumn2])
          #Check is third indicator exist
          signalList3.append(row[indicatorColumn3])
          
        except Exception as e:
          #print("MARK 12")
          pass
          
        try:
          signalList_2.append(row[indicatorColumn_2])
          # Check if second indicator exist
          signalList2_2.append(row[indicatorColumn2_2])
          #Check is third indicator exist
          signalList3_2.append(row[indicatorColumn3_2])
          
        except Exception as e:
          #print("MARK 13")
          pass

        try:
          signalList_3.append(row[indicatorColumn_3])
          # Check if second indicator exist
          signalList3_3.append(row[indicatorColumn3_3])
          #Check is third indicator exist
          signalList4_3.append(row[indicatorColumn4_3])
          
        except Exception as e:
          #print("MARK 14")
          pass

        try:
          signalList_4.append(row[indicatorColumn_4])
          # Check if second indicator exist
          signalList4_4.append(row[indicatorColumn4_4])
          #Check is third indicator exist
          signalList5_4.append(row[indicatorColumn5_4])
          
        except Exception as e:
          #print("MARK 15")
          pass

        # Temp variable to store the current price
        tempPrice = row["Close"] * 100
        closePriceList.append(tempPrice)

        # calculate the tax
        tax = tempPrice * 0.46 / 100
        tax = int(tax)
        taxList.append(tax)
        totalTax = totalTax + tax

        # Calculate total sell price
        sellPrice = tempPrice - tax
        purchasedPriceList.append(buyPrice)

        # calc the profit by subtract it with the purchase value
        profit = sellPrice - buyPrice
        profitList.append(profit)
        # add to total profit
        totalProfit = totalProfit + profit

        # Change the boolean to False, to indicate that we don't own the stock anymore
        isOwned = False
        numberSell = numberSell + 1
        i = i + 1
        indexList.append(index)                   
        #print("MARK 16")

  orderName = indicatorColumn.split("_")
  orderName = orderName[0]

  orderName_2 = indicatorColumn_2.split("_")
  orderName_2 = orderName_2[0]

  orderName_3 = indicatorColumn_3.split("_")
  orderName_3 = orderName_3[0]

  orderName_4 = indicatorColumn_4.split("_")
  orderName_4 = orderName_4[0]

  # Create a Dictionary to store the Simulation Data
  simulationLogDict = dict()

  try:
    simulationLogDict["Date"] = indexList
    simulationLogDict["Close Price"] = closePriceList
    simulationLogDict["Fee"] = taxList
    simulationLogDict["Purchased Price"] = purchasedPriceList
    simulationLogDict["Capital Gain"] = profitList
    simulationLogDict[orderName] = orderList
    simulationLogDict[orderName_2] = orderList_2
    simulationLogDict[orderName_3] = orderList_3
    simulationLogDict[orderName_4] = orderList_4   
    simulationLogDict[indicatorColumn] = signalList    
    simulationLogDict[indicatorColumn2] = signalList2
    simulationLogDict[indicatorColumn3] = signalList3

  except Exception as e:
    #print("MARK 17")
    pass

  try:
    simulationLogDict[indicatorColumn_2] = signalList_2
    simulationLogDict[indicatorColumn2_2] = signalList2_2
    simulationLogDict[indicatorColumn3_2] = signalList3_2
  except Exception as e:
    #print("MARK 18")
    pass

  try:
    simulationLogDict[indicatorColumn_3] = signalList_3
    simulationLogDict[indicatorColumn3_3] = signalList3_3
    simulationLogDict[indicatorColumn4_3] = signalList4_3
  except Exception as e:
    #print("MARK 19")
    pass

  try:
    simulationLogDict[indicatorColumn_4] = signalList_4
    simulationLogDict[indicatorColumn4_4] = signalList4_4
    simulationLogDict[indicatorColumn5_4] = signalList5_4
  except Exception as e:
    #print("MARK 20")
    pass

  # print(simulationLogDict)
  indicatorName = indicatorColumn + "_OR_" + indicatorColumn_2 + "_AND_" + indicatorColumn_3 + "_AND_" + indicatorColumn_4
  #Convert the dict to dataframe and save it to CSV
  simulationLog = pd.DataFrame(simulationLogDict)
  # print(simulationLog)
  simulationPath = "Log/Simulation/" + stockSymbol + "_" + indicatorName+ ".csv"
  simulationLog.to_csv(simulationPath)
  print(stockSymbol,"simulation stored in :",simulationPath)
    
  # SIMULATION SUMMARY
  #Calculate the profit in percentage
  try:
    profitPercentage = totalProfit / initialCapital * 100
    profitPercentage = int(profitPercentage)
  except:
    profitPercentage = 0  

  # Append the simulation summary to the lists for later use
  stockSymbolList.append(stockSymbol)
  initialCapitalList.append(initialCapital)
  totalProfitList.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList.append(profitTemp)
  totalTaxList.append(totalTax)
  numberPurchaseList.append(numberPurchase)
  numberSellList.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList.append(indicatorName)
  #print("MARK 21")


#### RunAllCombination function ####

def RunAllCombination():
    print("is running on the main program.......")

    stockObjectList, stockList = Scrapping()
    CreatePathSimulation()

    layerDataFrame = DataframeToLayer(stockList)
    stockFractions = StockFraction(stockList)
    
    # Add column 'Fraction' from stockLayers to layerDataFrame without using loop
    layerDataFrame["Fraction"] = [stockFractions[i]["Fraction"].iloc[0] for i in range(len(stockFractions))]
    #print(layerDataFrame.head())

    #mfi indicator
    mfivalue = 14
    for stock in stockObjectList :

        MFIIndicator1 = MFIIndicator(close = stock["Close"], volume = stock["Volume"], low = stock["Low"], high = stock["High"], window=mfivalue)

        stock['MFII_' + str(mfivalue)] = MFIIndicator1.money_flow_index()

        stock.loc[(stock['MFII_14'] <= 20), 'MFI_Recommend_14'] = 'BUY'
        stock.loc[(stock['MFII_14'] >= 20) & (stock['MFII_14']  <= 80), 'MFI_Recommend_14'] = 'HOLD'  
        stock.loc[(stock['MFII_14'] >= 80), 'MFI_Recommend_14'] = 'SELL'
    
    #BB indicator
    # Initiate BB Indicator Variable
    bbvalue = 20

    for stock in stockObjectList :
        bbIndicator = BollingerBands(close = stock["Close"], window=bbvalue)

        stock["BB_MAVG_20"] = bbIndicator.bollinger_mavg() #Moving AVG
        stock["BB_atas_20"] = bbIndicator.bollinger_hband() #High Band
        stock["BB_bawah_20"] = bbIndicator.bollinger_lband() #Low Band

        stock.loc[(stock['High'] > stock['BB_atas_20']) , 'BB_Recommend_20'] = 'SELL'
        stock.loc[(stock['High'] >= stock['BB_MAVG_20']) , 'BB_Recommend_20'] = 'SELL'
        stock.loc[(stock['Low'] <= stock['BB_MAVG_20']), 'BB_Recommend_20'] = 'BUY'
        stock.loc[(stock['Low'] < stock['BB_bawah_20']) , 'BB_Recommend_20'] = 'BUY'
    
    #CCI indicator

    # Initiate CCI Indicator Variable
    ccivalue = 20

    for stock in stockObjectList :
        CCII = CCIIndicator(high = stock["High"], low = stock["Low"], close = stock["Close"], window= ccivalue)

        stock["CCI_20"] = CCII.cci()

        stock.loc[(stock['CCI_20'] >= -200) & (stock['CCI_20']  <= 0), 'CCI_Recommend_20'] = 'BUY'
        stock.loc[(stock['CCI_20'] >= 0) & (stock['CCI_20']  <= 200), 'CCI_Recommend_20'] = 'SELL'
        
    #SO indicator

    # Initiate BB Indicator Variable
    sovalue = 14

    for stock in stockObjectList :
        SO = StochasticOscillator(high = stock["High"], low = stock["Low"], close = stock["Close"], window= sovalue)

        stock["SO_14"] = SO.stoch()

        stock.loc[(stock['SO_14'] <= 20), 'SO_Recommend_14'] = 'BUY'
        stock.loc[(stock['SO_14'] >= 20) & (stock['SO_14']  <= 80), 'SO_Recommend_14'] = 'HOLD'    
        stock.loc[(stock['SO_14'] >= 80), 'SO_Recommend_14'] = 'SELL'

    #Print the dataframe with raw values to CSV
    # Check if the path exist
    path1 = "Log/Simulation/"
    path2 = "Log/Summary/"
    path3 = "Data/"
    path4 = "Log/Simulation/Layer/"
    path5 = "Log/Stocks/"

    i = 0
    for stock in stockObjectList :
        stock.to_csv(path3 + stockList[i] + '.csv')
        i = i + 1

    #one combination

    MFIIVariables_onecombination = ["Stock_Object","Stock_Name",'MFI_Recommend_' + str(mfivalue),"MFII_" +str(mfivalue)]
    BBVariables_onecombination = ["Stock_Object","Stock_Name","BB_Recommend_" + str(bbvalue), "BB_MAVG_" + str(bbvalue), "BB_atas_" + str(bbvalue),  "BB_bawah_" + str(bbvalue) ]
    CCIVariables_onecombination = ["Stock_Object","Stock_Name",'CCI_Recommend_' + str(ccivalue), 'CCI_' + str(ccivalue)]
    SOVariables_onecombination = ["Stock_Object","Stock_Name",'SO_Recommend_' + str(sovalue),'SO_' + str(sovalue),]

    i = 0
    for stock in stockObjectList:
        # Replace the placeholder of object and name with actual data
        MFIIVariables_onecombination[0] = stock
        MFIIVariables_onecombination[1] = stockList[i]

        BBVariables_onecombination[0] = stock
        BBVariables_onecombination[1] = stockList[i]

        CCIVariables_onecombination[0] = stock
        CCIVariables_onecombination[1] = stockList[i]

        SOVariables_onecombination[0] = stock
        SOVariables_onecombination[1] = stockList[i]
        
        OneCombination(MFIIVariables_onecombination)
        OneCombination(BBVariables_onecombination)
        OneCombination(CCIVariables_onecombination)
        OneCombination(SOVariables_onecombination)
        i = i + 1

                #Store lists to dictionary
    simulationSummaryDict = {
        "Ticker Code": stockSymbolList,
        "Initial Capital": initialCapitalList,
        "Total Capital Gain": totalProfitList,
        "Capital Gain Percentage": profitPercentageList,
        "Transaction Fee": totalTaxList,
        "Number Purchased": numberPurchaseList,
        "Number Sold": numberSellList,
        "Indicator": indicatorColumnList
    }
    #store the simulation summary to CSV
    fileName = "OneCombination"
    summaryPath = "Log/Summary/"+ fileName + "_summary.csv"

    simulationSummary = pd.DataFrame(simulationSummaryDict)

    # Add 'Stock Layer' column and 'Fraction' column from layerDataFrame DataFrame to simulationSummary dataframe when simulationSummary['Ticker Code'] == layerDataFrame['Ticker Code']
    simulationSummary['Stock Layer'] = simulationSummary['Ticker Code'].map(layerDataFrame.set_index('Ticker Code')['Stock Layer'])
    simulationSummary['Fraction'] = simulationSummary['Ticker Code'].map(layerDataFrame.set_index('Ticker Code')['Fraction'])
    simulationSummary.to_csv(summaryPath)
    print(simulationSummary)

    #two combination

    MFIIVariables = ["Stock_Object","Stock_Name",'MFI_Recommend_' + str(mfivalue),"MFII_" +str(mfivalue)]
    BBVariables = ["Stock_Object","Stock_Name","BB_Recommend_" + str(bbvalue), "BB_MAVG_" + str(bbvalue), "BB_atas_" + str(bbvalue),  "BB_bawah_" + str(bbvalue) ]
    CCIVariables = ["Stock_Object","Stock_Name",'CCI_Recommend_' + str(ccivalue), 'CCI_' + str(ccivalue)]
    SOVariables = ["Stock_Object","Stock_Name",'SO_Recommend_' + str(sovalue),'SO_' + str(sovalue),]

    i = 0
    for stock in stockObjectList:
        # Replace the placeholder of object and name with actual data
        MFIIVariables[0] = stock
        MFIIVariables[1] = stockList[i]

        BBVariables[0] = stock
        BBVariables[1] = stockList[i]

        CCIVariables[0] = stock
        CCIVariables[1] = stockList[i]

        SOVariables[0] = stock
        SOVariables[1] = stockList[i]

        # AB
        RunTwoCombination_AND(MFIIVariables, BBVariables)
        RunTwoCombination_OR(MFIIVariables, BBVariables)

        # AC
        RunTwoCombination_AND(MFIIVariables, CCIVariables)
        RunTwoCombination_OR(MFIIVariables, CCIVariables)

        # AD
        RunTwoCombination_AND(MFIIVariables, SOVariables)
        RunTwoCombination_OR(MFIIVariables, CCIVariables)

        # BC
        RunTwoCombination_AND(BBVariables, CCIVariables)
        RunTwoCombination_OR(BBVariables, CCIVariables)

        # BD
        RunTwoCombination_AND(BBVariables, SOVariables)
        RunTwoCombination_OR(BBVariables, SOVariables)

        # CD
        RunTwoCombination_AND(CCIVariables, SOVariables)
        RunTwoCombination_OR(CCIVariables, SOVariables)

        i = i + 1

    twoCombinationSummaryDict = {
        "Ticker Code": stockSymbolList,
        "Initial Capital": initialCapitalList,
        "Total Capital Gain": totalProfitList,
        "Capital Gain Percentage": profitPercentageList,
        "Transaction Fee": totalTaxList,
        "Number Purchased": numberPurchaseList,
        "Number Sold": numberSellList,
        "Indicator": indicatorColumnList
    }
    #store the simulation summary to CSV
    fileName = "TwoCombination"
    summaryPath = "Log/Summary/"+ fileName + "_summary.csv"

    twoCombinationSummary = pd.DataFrame(twoCombinationSummaryDict)
    # Add 'Stock Layer' column and 'Fraction' column from layerDataFrame DataFrame to twoCombinationSummary dataframe when twoCombinationSummary['Ticker Code'] == layerDataFrame['Ticker Code']
    twoCombinationSummary['Stock Layer'] = twoCombinationSummary['Ticker Code'].map(layerDataFrame.set_index('Ticker Code')['Stock Layer'])
    twoCombinationSummary['Fraction'] = twoCombinationSummary['Ticker Code'].map(layerDataFrame.set_index('Ticker Code')['Fraction'])

    twoCombinationSummary.to_csv(summaryPath)
    sorted_twoCombinationSummary = twoCombinationSummary.sort_values(by = 'Capital Gain Percentage', ascending = False)
    print(sorted_twoCombinationSummary)

    # three combination
    # define incdicator variable

    MFIIVariables = ["Stock_Object","Stock_Name",'MFI_Recommend_' + str(mfivalue),"MFII_" +str(mfivalue)]
    BBVariables = ["Stock_Object","Stock_Name","BB_Recommend_" + str(bbvalue), "BB_MAVG_" + str(bbvalue), "BB_atas_" + str(bbvalue),  "BB_bawah_" + str(bbvalue) ]
    CCIVariables = ["Stock_Object","Stock_Name",'CCI_Recommend_' + str(ccivalue), 'CCI_' + str(ccivalue)]
    SOVariables = ["Stock_Object","Stock_Name",'SO_Recommend_' + str(sovalue),'SO_' + str(sovalue),]
    
    # Running the simulation
    i = 0
    for stock in stockObjectList:
        # Replace the placeholder of object and name with actual data
        MFIIVariables[0] = stock
        MFIIVariables[1] = stockList[i]

        BBVariables[0] = stock
        BBVariables[1] = stockList[i]

        CCIVariables[0] = stock
        CCIVariables[1] = stockList[i]

        SOVariables[0] = stock
        SOVariables[1] = stockList[i]

        # ABC
        RunThreeCombination_AND(MFIIVariables, BBVariables, CCIVariables)
        RunThreeCombination_OR(MFIIVariables, BBVariables, CCIVariables)
        RunThreeCombination_AND_OR(MFIIVariables, BBVariables, CCIVariables)
        RunThreeCombination_OR_AND(MFIIVariables, BBVariables, CCIVariables)

        # ABD
        RunThreeCombination_AND(MFIIVariables, BBVariables, SOVariables)
        RunThreeCombination_OR(MFIIVariables, BBVariables, SOVariables)
        RunThreeCombination_AND_OR(MFIIVariables, BBVariables, SOVariables)
        RunThreeCombination_OR_AND(MFIIVariables, BBVariables, SOVariables)

        # ACD
        RunThreeCombination_AND(MFIIVariables, CCIVariables, SOVariables)
        RunThreeCombination_OR(MFIIVariables, CCIVariables, SOVariables)
        RunThreeCombination_AND_OR(MFIIVariables, CCIVariables, SOVariables)
        RunThreeCombination_OR_AND(MFIIVariables, CCIVariables, SOVariables)

        # BCD
        RunThreeCombination_AND(BBVariables, CCIVariables, SOVariables)
        RunThreeCombination_OR(BBVariables, CCIVariables, SOVariables)
        RunThreeCombination_AND_OR(BBVariables, CCIVariables, SOVariables)
        RunThreeCombination_OR_AND(BBVariables, CCIVariables, SOVariables)

        i = i + 1

    ThreeCombinationSummaryDict = {
        "Ticker Code": stockSymbolList,
        "Initial Capital": initialCapitalList,
        "Total Capital Gain": totalProfitList,
        "Capital Gain Percentage": profitPercentageList,
        "Transaction Fee": totalTaxList,
        "Number Purchased": numberPurchaseList,
        "Number Sold": numberSellList,
        "Indicator": indicatorColumnList
    }
    #store the simulation summary to CSV
    fileName = "ThreeCombination"
    summaryPath = "Log/Summary/"+ fileName + "_summary.csv"

    ThreeCombinationSummary = pd.DataFrame(ThreeCombinationSummaryDict)

    # Add 'Stock Layer' column and 'Fraction' column from layerDataFrame DataFrame to ThreeCombinationSummary dataframe when ThreeCombinationSummary['Ticker Code'] == layerDataFrame['Ticker Code']
    ThreeCombinationSummary['Stock Layer'] = ThreeCombinationSummary['Ticker Code'].map(layerDataFrame.set_index('Ticker Code')['Stock Layer'])
    ThreeCombinationSummary['Fraction'] = ThreeCombinationSummary['Ticker Code'].map(layerDataFrame.set_index('Ticker Code')['Fraction'])

    ThreeCombinationSummary.to_csv(summaryPath)
    sorted_ThreeCombinationSummary = ThreeCombinationSummary.sort_values(by = 'Capital Gain Percentage', ascending = False)
    print(sorted_ThreeCombinationSummary)

    # #four combination

    # #define incdicator variable

    MFIIVariables = ["Stock_Object","Stock_Name",'MFI_Recommend_' + str(mfivalue),"MFII_" +str(mfivalue)]
    BBVariables = ["Stock_Object","Stock_Name","BB_Recommend_" + str(bbvalue), "BB_MAVG_" + str(bbvalue), "BB_atas_" + str(bbvalue),  "BB_bawah_" + str(bbvalue) ]
    CCIVariables = ["Stock_Object","Stock_Name",'CCI_Recommend_' + str(ccivalue), 'CCI_' + str(ccivalue)]
    SOVariables = ["Stock_Object","Stock_Name",'SO_Recommend_' + str(sovalue),'SO_' + str(sovalue),]

    # Running the simulation
    i = 0
    for stock in stockObjectList:
        # Replace the placeholder of object and name with actual data
        MFIIVariables[0] = stock
        MFIIVariables[1] = stockList[i]

        BBVariables[0] = stock
        BBVariables[1] = stockList[i]

        CCIVariables[0] = stock
        CCIVariables[1] = stockList[i]

        SOVariables[0] = stock
        SOVariables[1] = stockList[i]

        #ABCD
        RunFourCombination_AND(MFIIVariables, BBVariables, CCIVariables, SOVariables)
        RunFourCombination_OR(MFIIVariables, BBVariables, CCIVariables, SOVariables)
        RunFourCombination_AND_AND_OR(MFIIVariables, BBVariables, CCIVariables, SOVariables)
        RunFourCombination_OR_OR_AND(MFIIVariables, BBVariables, CCIVariables, SOVariables)
        RunFourCombination_OR_AND_AND(MFIIVariables, BBVariables, CCIVariables, SOVariables)
        RunFourCombination_AND_OR_OR(MFIIVariables, BBVariables, CCIVariables, SOVariables)

        i = i + 1
        #done
    
    #Store lists to dictionary
    FourCombinationSummaryDict = {
        "Ticker Code": stockSymbolList,
        "Initial Capital": initialCapitalList,
        "Total Capital Gain": totalProfitList,
        "Capital Gain Percentage": profitPercentageList,
        "Transaction Fee": totalTaxList,
        "Number Purchased": numberPurchaseList,
        "Number Sold": numberSellList,
        "Indicator": indicatorColumnList
    }
    #store the simulation summary to CSV
    fileName = "FourCombination"
    summaryPath = "Log/Summary/"+ fileName + "_summary.csv"

    FourCombinationSummary = pd.DataFrame(FourCombinationSummaryDict)

    # Add 'Stock Layer' column and 'Fraction' column from layerDataFrame DataFrame to FourCombinationSummary dataframe when FourCombinationSummary['Ticker Code'] == layerDataFrame['Ticker Code']
    FourCombinationSummary['Stock Layer'] = FourCombinationSummary['Ticker Code'].map(layerDataFrame.set_index('Ticker Code')['Stock Layer'])
    FourCombinationSummary['Fraction'] = FourCombinationSummary['Ticker Code'].map(layerDataFrame.set_index('Ticker Code')['Fraction'])

    FourCombinationSummary.to_csv(summaryPath)
    sorted_FourCombinationSummary = FourCombinationSummary.sort_values(by = 'Capital Gain Percentage', ascending = False)
    print(sorted_FourCombinationSummary)

    return simulationSummary, twoCombinationSummary, ThreeCombinationSummary, FourCombinationSummary, stockList