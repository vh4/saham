import yfinance as yf
import pandas as pd
import time

#### Four Combination #####
#function X AND X AND X AND X

# Empty all the list for the summary (for combination 4)

stockSymbolList4 = list()
initialCapitalList4 = list()
totalProfitList4 = list()
profitPercentageList4 = list()
totalTaxList4 = list()   
numberPurchaseList4 = list()
numberSellList4 = list()  
indicatorColumnList4 = list()

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
  stockSymbolList4.append(stockSymbol)
  initialCapitalList4.append(initialCapital)
  totalProfitList4.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList4.append(profitTemp)
  totalTaxList4.append(totalTax)
  numberPurchaseList4.append(numberPurchase)
  numberSellList4.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList4.append(indicatorName)
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
  stockSymbolList4.append(stockSymbol)
  initialCapitalList4.append(initialCapital)
  totalProfitList4.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList4.append(profitTemp)
  totalTaxList4.append(totalTax)
  numberPurchaseList4.append(numberPurchase)
  numberSellList4.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList4.append(indicatorName)
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
  stockSymbolList4.append(stockSymbol)
  initialCapitalList4.append(initialCapital)
  totalProfitList4.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList4.append(profitTemp)
  totalTaxList4.append(totalTax)
  numberPurchaseList4.append(numberPurchase)
  numberSellList4.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList4.append(indicatorName)
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
  stockSymbolList4.append(stockSymbol)
  initialCapitalList4.append(initialCapital)
  totalProfitList4.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList4.append(profitTemp)
  totalTaxList4.append(totalTax)
  numberPurchaseList4.append(numberPurchase)
  numberSellList4.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList4.append(indicatorName)
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
  stockSymbolList4.append(stockSymbol)
  initialCapitalList4.append(initialCapital)
  totalProfitList4.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList4.append(profitTemp)
  totalTaxList4.append(totalTax)
  numberPurchaseList4.append(numberPurchase)
  numberSellList4.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList4.append(indicatorName)
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
  stockSymbolList4.append(stockSymbol)
  initialCapitalList4.append(initialCapital)
  totalProfitList4.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList4.append(profitTemp)
  totalTaxList4.append(totalTax)
  numberPurchaseList4.append(numberPurchase)
  numberSellList4.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList4.append(indicatorName)
  #print("MARK 21")