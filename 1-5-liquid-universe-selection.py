class LiquidUniverseSelection(QCAlgorithm):
    
    filteredByPrice = None
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 11)  
        self.SetEndDate(2019, 7, 1) 
        self.SetCash(100000)  
        self.AddUniverse(self.CoarseSelectionFilter)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.UniverseSettings.Leverage = 2
       
    def CoarseSelectionFilter(self, coarse):
        sortedByDollarVolume = sorted(coarse, key=lambda c: c.DollarVolume, reverse=True)
        filteredByPrice = [c.Symbol for c in sortedByDollarVolume if c.Price > 10]
        return filteredByPrice[:10] 

    def OnSecuritiesChanged(self, changes):
        self.changes = changes
        self.Log(f"OnSecuritiesChanged({self.Time}):: {changes}")
        for security in self.changes.RemovedSecurities:
            if security.Invested:
                self.Liquidate(security.Symbol)
        for security in self.changes.AddedSecurities:
            self.SetHoldings(security.Symbol, 0.18)
            
