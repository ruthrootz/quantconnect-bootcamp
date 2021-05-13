import datetime
from datetime import timedelta
from QuantConnect.Data.UniverseSelection import * 
from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel

class LiquidValueStocks(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2016, 10, 1)
        self.SetEndDate(2017, 10, 1)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Hour
        self.AddUniverseSelection(LiquidValueUniverseSelectionModel())
        self.AddAlpha(NullAlphaModel())
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetExecution(ImmediateExecutionModel())

class LiquidValueUniverseSelectionModel(FundamentalUniverseSelectionModel):
    
    def __init__(self):
        super().__init__(True, None, None)
        self.lastMonth = -1 
    
    def SelectCoarse(self, algorithm, coarse):
        
        #1. If it isn't time to update data, return the previous symbols 
        if self.lastMonth == algorithm.Time.month:
            return Universe.Unchanged
        #2. Update self.lastMonth with current month to make sure only process once per month
        self.lastMonth = algorithm.Time.month
        #3. Sort symbols by dollar volume and if they have fundamental data, in descending order
        sortedByDollarVolume = sorted([s for s in coarse if s.HasFundamentalData],
        key=lambda s: s.DollarVolume, reverse=True)
        
        #4. Return the top 100 Symbols by Dollar Volume
        return [s.Symbol for s in sortedByDollarVolume][:100]
