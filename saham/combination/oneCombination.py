import yfinance as yf
import pandas as pd
import time

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
