from datetime import datetime
from QuantConnect.Data.UniverseSelection import * 
from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel

class LiquidValueStocks(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2016, 10, 1)
        self.SetEndDate(2017, 10, 1)
        self.SetCash(100000)
        self.AddAlpha(NullAlphaModel())
        
        #1. Create an instance of our LiquidValueUniverseSelectionModel and set to hourly resolution
        self.AddUniverseSelection(LiquidValueUniverseSelectionModel())
        
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())
        self.SetExecution(ImmediateExecutionModel())
        
        
# Define the Universe Model Class
class LiquidValueUniverseSelectionModel(FundamentalUniverseSelectionModel):
    
    def __init__(self):
        super().__init__(True, None, None)
    
    #2. Add an empty SelectCoarse() method with its parameters
    def SelectCoarse(self, algorithm, coarse):
        pass
    
    #2. Add an empty SelectFine() method with is parameters
    def SelectFine(self, algorithm, fine):
        pass
