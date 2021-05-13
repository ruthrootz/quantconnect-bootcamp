from datetime import timedelta
from QuantConnect.Data.UniverseSelection import * 
from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel

class LiquidValueStocks(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2017, 5, 15)
        self.SetEndDate(2017, 7, 15)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Hour
        self.AddUniverseSelection(LiquidValueUniverseSelectionModel())
        
        #1. Create and instance of the LongShortEYAlphaModel
        self.AddAlpha(LongShortEYAlphaModel())
        
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetExecution(ImmediateExecutionModel())

class LiquidValueUniverseSelectionModel(FundamentalUniverseSelectionModel):
    
    def __init__(self):
        super().__init__(True, None, None)
        self.lastMonth = -1 
        
    def SelectCoarse(self, algorithm, coarse):
        if self.lastMonth == algorithm.Time.month:
            return Universe.Unchanged
        self.lastMonth = algorithm.Time.month

        sortedByDollarVolume = sorted([x for x in coarse if x.HasFundamentalData],
            key=lambda x: x.DollarVolume, reverse=True)

        return [x.Symbol for x in sortedByDollarVolume[:100]]

    def SelectFine(self, algorithm, fine):
        sortedByYields = sorted(fine, key=lambda f: f.ValuationRatios.EarningYield, reverse=True)
        universe = sortedByYields[:10] + sortedByYields[-10:]
        return [f.Symbol for f in universe]

# Define the LongShortAlphaModel class  
class LongShortEYAlphaModel(AlphaModel):

    def __init__(self):
        self.lastMonth = -1

    def Update(self, algorithm, data):
        insights = []
        
        #2. If else statement to emit signals once a month 
        if self.lastMonth == algorithm.Time.month:
            return insights
        self.lastMonth = algorithm.Time.month
        #3. For loop to emit insights with insight directions 
        # based on whether earnings yield is greater or less than zero once a month
        for security in algorithm.ActiveSecurities.Values:
            direction = 1 if security.Fundamentals.ValuationRatios.EarningYield > 0 else -1 
            insights.append(Insight.Price(security.Symbol, timedelta(28), direction)) 
        return insights
