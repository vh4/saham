import pandas as pd
import yfinance as yf
import time
import numpy as np
from saham.runAllCombination import RunAllCombination

def main():

    #panggil fungsi runAllCombination   
    simulationSummary, twoCombinationSummary, ThreeCombinationSummary, FourCombinationSummary, stockList = RunAllCombination()

    # Check if the path exist
    path1 = "Log/Simulation/"
    path2 = "Log/Summary/"
    path3 = "Data/"
    path4 = "Log/Simulation/Layer/"
    path5 = "Log/Stocks/"

    #Analysis OneCombination 

    #sedikit
    filteredSimulationSummary_sedikit = simulationSummary.loc[(simulationSummary['Capital Gain Percentage'] >= 0) & (simulationSummary['Capital Gain Percentage'] <= 33)]
    print(filteredSimulationSummary_sedikit.sort_values(by = 'Capital Gain Percentage', ascending = False))
    
    #sedang
    filteredSimulationSummary_sedang = simulationSummary.loc[(simulationSummary['Capital Gain Percentage'] >= 34) & (simulationSummary['Capital Gain Percentage'] <= 66)]
    print(filteredSimulationSummary_sedang.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #banyak
    filteredSimulationSummary_banyak = simulationSummary.loc[(simulationSummary['Capital Gain Percentage'] >= 67) & (simulationSummary['Capital Gain Percentage'] <= 99)]
    print(filteredSimulationSummary_banyak.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #sangat banyak
    filteredSimulationSummary_sangat_banyak = simulationSummary.loc[(simulationSummary['Capital Gain Percentage'] >= 100)]
    print(filteredSimulationSummary_sangat_banyak.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #Analysis TwoCombination 

    #sedikit
    filteredTwoSimulationSummary_sedikit = twoCombinationSummary.loc[(twoCombinationSummary['Capital Gain Percentage'] >= 0) & (twoCombinationSummary['Capital Gain Percentage'] <= 33)]
    print(filteredTwoSimulationSummary_sedikit.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #sedang
    filteredTwoSimulationSummary_sedang = twoCombinationSummary.loc[(twoCombinationSummary['Capital Gain Percentage'] >= 34) & (twoCombinationSummary['Capital Gain Percentage'] <= 66)]
    print(filteredTwoSimulationSummary_sedang.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #banyak
    filteredTwoSimulationSummary_banyak = twoCombinationSummary.loc[(twoCombinationSummary['Capital Gain Percentage'] >= 67) & (twoCombinationSummary['Capital Gain Percentage'] <= 99)]
    print(filteredTwoSimulationSummary_banyak.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #sangat banyak
    filteredTwoSimulationSummary_sangat_banyak = twoCombinationSummary.loc[(twoCombinationSummary['Capital Gain Percentage'] >= 100)]
    print(filteredTwoSimulationSummary_sangat_banyak.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #Analysis ThreeCombination

    #sedikit
    filteredThreeSimulationSummary_sedikit = ThreeCombinationSummary.loc[(ThreeCombinationSummary['Capital Gain Percentage'] >= 0) & (ThreeCombinationSummary['Capital Gain Percentage'] <= 33)]
    print(filteredThreeSimulationSummary_sedikit.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #sedang
    filteredThreeSimulationSummary_sedang = ThreeCombinationSummary.loc[(ThreeCombinationSummary['Capital Gain Percentage'] >= 34) & (ThreeCombinationSummary['Capital Gain Percentage'] <= 66)]
    print(filteredThreeSimulationSummary_sedang.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #banyak
    filteredThreeSimulationSummary_banyak = ThreeCombinationSummary.loc[(ThreeCombinationSummary['Capital Gain Percentage'] >= 67) & (ThreeCombinationSummary['Capital Gain Percentage'] <= 99)]
    print(filteredThreeSimulationSummary_banyak.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #sangat banyak
    filteredThreeSimulationSummary_sangat_banyak = ThreeCombinationSummary.loc[(ThreeCombinationSummary['Capital Gain Percentage'] >= 100)]
    print(filteredThreeSimulationSummary_sangat_banyak.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #Analysis FourCombination

    #sedikit
    filteredFourSimulationSummary_sedikit = FourCombinationSummary.loc[(FourCombinationSummary['Capital Gain Percentage'] >= 0) & (FourCombinationSummary['Capital Gain Percentage'] <= 33)]
    print(filteredFourSimulationSummary_sedikit.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #sedang
    filteredFourSimulationSummary_sedang = FourCombinationSummary.loc[(FourCombinationSummary['Capital Gain Percentage'] >= 34) & (FourCombinationSummary['Capital Gain Percentage'] <= 66)]
    print(filteredFourSimulationSummary_sedang.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #banyak
    filteredFourSimulationSummary_banyak = FourCombinationSummary.loc[(FourCombinationSummary['Capital Gain Percentage'] >= 67) & (FourCombinationSummary['Capital Gain Percentage'] <= 99)]
    print(filteredFourSimulationSummary_banyak.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #sangat banyak
    filteredFourSimulationSummary_sangat_banyak = FourCombinationSummary.loc[(FourCombinationSummary['Capital Gain Percentage'] >= 100)]
    print(filteredFourSimulationSummary_sangat_banyak.sort_values(by = 'Capital Gain Percentage', ascending = False))

    #layer and fraksi

    layers = ["LAYER_1", "LAYER_2", "LAYER_3"]

    #create loop to iterate through each layer
    for layer in layers:
        
        oneLayerDataFrame = simulationSummary.loc[simulationSummary['Stock Layer'] == layer]
        print(oneLayerDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        twoLayerDataFrame = twoCombinationSummary.loc[twoCombinationSummary['Stock Layer'] == layer]
        print(twoLayerDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        threeLayerDataFrame = ThreeCombinationSummary.loc[ThreeCombinationSummary['Stock Layer'] == layer]
        print(threeLayerDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        fourLayerDataFrame = FourCombinationSummary.loc[FourCombinationSummary['Stock Layer'] == layer]
        print(fourLayerDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        #Join all dataframe in this loop to combined dataframe
        combinedDataFrame = pd.concat([oneLayerDataFrame, twoLayerDataFrame, threeLayerDataFrame, fourLayerDataFrame])

        #store the simulation summary to CSV
        combinedDataFrame.to_csv(path4 + layer + "_summary.csv")

    # Join all Fraction column
    # and then sort the dataframe by "Capital Gain Percentage"
    # and then store the dataframe to CSV

    fractions = ['Fraksi_1', 'Fraksi_2', 'Fraksi_3', 'Fraksi_4','Fraksi_5']

    # create loop to iterate through each fraction
    for fraction in fractions:

        oneFractionDataFrame = simulationSummary.loc[simulationSummary['Fraction'] == fraction]
        print(oneFractionDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        twoFractionDataFrame = twoCombinationSummary.loc[twoCombinationSummary['Fraction'] == fraction]
        print(twoFractionDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        threeFractionDataFrame = ThreeCombinationSummary.loc[ThreeCombinationSummary['Fraction'] == fraction]
        print(threeFractionDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        fourFractionDataFrame = FourCombinationSummary.loc[FourCombinationSummary['Fraction'] == fraction]
        print(fourFractionDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        # Join all dataframe in this loop to combined dataframe
        combinedDataFrame = pd.concat([oneFractionDataFrame, twoFractionDataFrame, threeFractionDataFrame, fourFractionDataFrame])

        # store the simulation summary to CSV
        combinedDataFrame.to_csv(path4 + fraction + "_summary.csv")

    #klasifikasi saham

    #Join all four summaries based on 'Ticker Code' column
    #and then sort the dataframe by "Capital Gain Percentage"
    #and then store the dataframe to CSV
    
    for stock in stockList:
        oneStockDataFrame = simulationSummary.loc[simulationSummary['Ticker Code'] == stock]
        print(oneStockDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        twoStockDataFrame = twoCombinationSummary.loc[twoCombinationSummary['Ticker Code'] == stock]
        print(twoStockDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        threeStockDataFrame = ThreeCombinationSummary.loc[ThreeCombinationSummary['Ticker Code'] == stock]
        print(threeStockDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        fourStockDataFrame = FourCombinationSummary.loc[FourCombinationSummary['Ticker Code'] == stock]
        print(fourStockDataFrame.sort_values(by = 'Capital Gain Percentage', ascending = False))

        # Join all dataframe in this loop to combined dataframe
        combinedDataFrame = pd.concat([oneStockDataFrame, twoStockDataFrame, threeStockDataFrame, fourStockDataFrame])

        # store the simulation summary to CSV
        combinedDataFrame.to_csv(path5 + stock + "_summary.csv")

        print("END PROGRAM................................................................................  ")

main()




