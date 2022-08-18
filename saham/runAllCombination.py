import yfinance as yf
import pandas as pd
import time
import sys

from saham.scrapping.scrapping import Scrapping, CreatePathSimulation
from saham.dataframeTolayer import DataframeToLayer, StockFraction

#indicatior import

from saham.indikator.mfiiIndikator import MFIIndicator
from saham.indikator.bbIndikator import BollingerBands
from saham.indikator.soIndikator import StochasticOscillator
from saham.indikator.ccIndikator import CCIIndicator

#combination import
from saham.combination.oneCombination import *
from saham.combination.twoCombination import *
from saham.combination.threeCombination import *
from saham.combination.fourCombination import *

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
        "Ticker Code": stockSymbolList2,
        "Initial Capital": initialCapitalList2,
        "Total Capital Gain": totalProfitList2,
        "Capital Gain Percentage": profitPercentageList2,
        "Transaction Fee": totalTaxList2,
        "Number Purchased": numberPurchaseList2,
        "Number Sold": numberSellList2,
        "Indicator": indicatorColumnList2
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
        "Ticker Code": stockSymbolList3,
        "Initial Capital": initialCapitalList3,
        "Total Capital Gain": totalProfitList3,
        "Capital Gain Percentage": profitPercentageList3,
        "Transaction Fee": totalTaxList3,
        "Number Purchased": numberPurchaseList3,
        "Number Sold": numberSellList3,
        "Indicator": indicatorColumnList3
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
        "Ticker Code": stockSymbolList4,
        "Initial Capital": initialCapitalList4,
        "Total Capital Gain": totalProfitList4,
        "Capital Gain Percentage": profitPercentageList4,
        "Transaction Fee": totalTaxList4,
        "Number Purchased": numberPurchaseList4,
        "Number Sold": numberSellList4,
        "Indicator": indicatorColumnList4
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