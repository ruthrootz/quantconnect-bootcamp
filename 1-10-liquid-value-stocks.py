from datetime import timedelta
from QuantConnect.Data.UniverseSelection import * 
from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel

class LiquidValueStocks(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2016, 10, 1)
        self.SetEndDate(2017, 10, 1)
        self.SetCash(100000)
        self.universe = None
        self.UniverseSettings.Resolution = Resolution.Hour
        self.AddUniverseSelection(LiquidValueUniverseSelectionModel())
        self.AddAlpha(NullAlphaModel())
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetExecution(ImmediateExecutionModel())
    
class LiquidValueUniverseSelectionModel(FundamentalUniverseSelectionModel):
    
    def __init__(self):
        self.lastMonth = -1 
        super().__init__(True, None, None)
    
    def SelectCoarse(self, algorithm, coarse):
        if self.lastMonth == algorithm.Time.month:
            return Universe.Unchanged
        self.lastMonth = algorithm.Time.month

        sortedByDollarVolume = sorted([x for x in coarse if x.HasFundamentalData],
            key=lambda x: x.DollarVolume, reverse=True)

        return [x.Symbol for x in sortedByDollarVolume[:100]]

    def SelectFine(self, algorithm, fine):
        #1. Sort yields per share
        sortedByYields = sorted(fine, key=lambda s: s.ValuationRatios.EarningYield, reverse=True) 
        
        #2. Take top 10 most profitable stocks -- and bottom 10 least profitable stocks
        # Save to the variable self.universe
        self.universe = sortedByYields[:10] + sortedByYields[-10:]
        
        #3. Return the symbol objects by iterating through self.universe with list comprehension
        return [f.Symbol for f in self.universe]
