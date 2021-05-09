from datetime import timedelta

class MOMAlphaModel(AlphaModel):
    
    def __init__(self):
        self.mom = []
      
    def OnSecuritiesChanged(self, algorithm, changes):
        
        # 1. Initialize a 14-day momentum indicator for each symbol
        for security in changes.AddedSecurities:
            symbol = security.Symbol
            self.mom.append({"symbol":symbol, "indicator":algorithm.MOM(symbol, 14, Resolution.Daily)})
        
    def Update(self, algorithm, data):

        #2. Sort the list of dictionaries by indicator in descending order
        ordered = sorted(self.mom, key=lambda s: s["indicator"], reverse=True)
        
        #3. Return a group of insights, emitting InsightDirection.Up for the first item of ordered, and InsightDirection.Flat for the second
        return Insight.Group([
            # Create a grouped insight
            Insight.Price(ordered[0]["symbol"], timedelta(1), InsightDirection.Up), 
            Insight.Price(ordered[1]["symbol"], timedelta(1), InsightDirection.Flat)
         ])
        
class FrameworkAlgorithm(QCAlgorithm):
    
    def Initialize(self):

        self.SetStartDate(2013, 10, 1)   
        self.SetEndDate(2013, 12, 1)   
        self.SetCash(100000)           
        symbols = [Symbol.Create("SPY", SecurityType.Equity, Market.USA), Symbol.Create("BND", SecurityType.Equity, Market.USA)]
        self.UniverseSettings.Resolution = Resolution.Daily
        self.SetUniverseSelection(ManualUniverseSelectionModel(symbols))

        # Call the MOMAlphaModel Class 
        self.SetAlpha(MOMAlphaModel())

        self.SetPortfolioConstruction(NullPortfolioConstructionModel())
        self.SetRiskManagement(NullRiskManagementModel())
        self.SetExecution(NullExecutionModel())
        
