from datetime import timedelta
class MOMAlphaModel(AlphaModel): 
    def __init__(self):
        self.mom = []
    def OnSecuritiesChanged(self, algorithm, changes):
        for security in changes.AddedSecurities:
            symbol = security.Symbol
            self.mom.append({"symbol":symbol, "indicator":algorithm.MOM(symbol, 14, Resolution.Daily)})
    def Update(self, algorithm, data):
        ordered = sorted(self.mom, key=lambda kv: kv["indicator"].Current.Value, reverse=True)
        return Insight.Group([Insight.Price(ordered[0]['symbol'], timedelta(1), InsightDirection.Up), Insight.Price(ordered[1]['symbol'], timedelta(1), InsightDirection.Flat) ])
 
         
class FrameworkAlgorithm(QCAlgorithm):
    def Initialize(self):
        self.SetStartDate(2013, 10, 1)  
        self.SetEndDate(2013, 12, 1)   
        self.SetCash(100000)           
        symbols = [Symbol.Create("SPY", SecurityType.Equity, Market.USA),  Symbol.Create("BND", SecurityType.Equity, Market.USA)]
        self.UniverseSettings.Resolution = Resolution.Daily
        self.SetUniverseSelection(ManualUniverseSelectionModel(symbols))
        self.SetAlpha(MOMAlphaModel())
        self.SetPortfolioConstruction(EqualWeightingPortfolioConstructionModel())

        #1. Set the Risk Management handler to use a 2% maximum drawdown
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.02))
        self.SetExecution(NullExecutionModel())
