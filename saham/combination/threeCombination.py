import yfinance as yf
import pandas as pd
import time

#### Three Combinations ####

# Empty all the list for the summary (for combination 3)

stockSymbolList3 = list()
initialCapitalList3 = list()
totalProfitList3 = list()
profitPercentageList3 = list()
totalTaxList3 = list()   
numberPurchaseList3 = list()
numberSellList3 = list()  
indicatorColumnList3 = list()

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
  stockSymbolList3.append(stockSymbol)
  initialCapitalList3.append(initialCapital)
  totalProfitList3.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList3.append(profitTemp)
  totalTaxList3.append(totalTax)
  numberPurchaseList3.append(numberPurchase)
  numberSellList3.append(numberSell)

  indicatorColumnList3.append(indicatorName)
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
  stockSymbolList3.append(stockSymbol)
  initialCapitalList3.append(initialCapital)
  totalProfitList3.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList3.append(profitTemp)
  totalTaxList3.append(totalTax)
  numberPurchaseList3.append(numberPurchase)
  numberSellList3.append(numberSell)

  indicatorColumnList3.append(indicatorName)
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
  stockSymbolList3.append(stockSymbol)
  initialCapitalList3.append(initialCapital)
  totalProfitList3.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList3.append(profitTemp)
  totalTaxList3.append(totalTax)
  numberPurchaseList3.append(numberPurchase)
  numberSellList3.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList3.append(indicatorName)
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
  stockSymbolList3.append(stockSymbol)
  initialCapitalList3.append(initialCapital)
  totalProfitList3.append(totalProfit)
  profitTemp = profitPercentage
  profitPercentageList3.append(profitTemp)
  totalTaxList3.append(totalTax)
  numberPurchaseList3.append(numberPurchase)
  numberSellList3.append(numberSell)
  # splitTemp = indicatorColumn.split("_")
  # indicatorName = splitTemp
  indicatorColumnList3.append(indicatorName)
  #print("MARK 17")