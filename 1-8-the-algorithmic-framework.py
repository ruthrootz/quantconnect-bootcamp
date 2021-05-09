class FrameworkAlgorithm(QCAlgorithm):
    
    def Initialize(self):

        self.SetStartDate(2013, 10, 1)   
        self.SetEndDate(2013, 12, 1)    
        self.SetCash(100000)           
        
        #1. Create a SPY and BND Symbol object that gets passed to the Universe Selection Model
        self.symbols = [Symbol.Create("SPY", SecurityType.Equity, Market.USA), Symbol.Create("BND", SecurityType.Equity, Market.USA)]
        #2. Set the resolution of the universe assets to daily resolution
        self.UniverseSettings.Resolution = Resolution.Daily
        #3. Set a universe using self.SetUniverseSelection(), and pass in a ManualUniverseSelectionModel() 
        # initialized with the symbols list
        self.SetUniverseSelection(ManualUniverseSelectionModel(self.symbols))
        self.SetAlpha(NullAlphaModel())
        self.SetPortfolioConstruction(NullPortfolioConstructionModel())
        self.SetRiskManagement(NullRiskManagementModel())
        self.SetExecution(NullExecutionModel())
        
