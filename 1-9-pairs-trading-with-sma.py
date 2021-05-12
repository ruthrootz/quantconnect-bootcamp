from datetime import timedelta, datetime

class SMAPairsTrading(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2018, 7, 1)   
        self.SetEndDate(2019, 3, 31)
        self.SetCash(100000)
        
        symbols = [Symbol.Create("PEP", SecurityType.Equity, Market.USA), Symbol.Create("KO", SecurityType.Equity, Market.USA)]
        self.AddUniverseSelection(ManualUniverseSelectionModel(symbols))
        self.UniverseSettings.Resolution = Resolution.Hour
        self.UniverseSettings.DataNormalizationMode = DataNormalizationMode.Raw
        self.AddAlpha(PairsTradingAlphaModel())
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetExecution(ImmediateExecutionModel()) 

class PairsTradingAlphaModel(AlphaModel):

    def __init__(self):
        self.pair = [ ]
        #1. Create a 500-period Simple Moving Average Indicator monitoring the spread SMA 
        self.spreadMean = ...
        
        #2. Create a 500-period Standard Deviation Indicator monitoring the spread Std 
        self.spreadStd = ...
        
    def Update(self, algorithm, data):

        spread = self.pair[1].Price - self.pair[0].Price
        #3. Update the spreadMean indicator with the spread
        #4. Update the spreadStd indicator with the spread
        
        #5. Save our upper threshold and lower threshold
        upperthreshold = ...
        lowerthreshold = ...
        
        return []
    
    def OnSecuritiesChanged(self, algorithm, changes):
        self.pair = [x for x in changes.AddedSecurities]
