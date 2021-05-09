class EMAMomentumUniverse(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 7)
        self.SetEndDate(2019, 4, 1)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
    
    def CoarseSelectionFunction(self, coarse):
        sortedByDollarVolume = sorted(coarse, key=lambda c: c.DollarVolume, reverse=True) 
        selected = [c.Symbol for c in sortedByDollarVolume if c.Price > 10][:10]
        return selected
        
    def OnSecuritiesChanged(self, changes):  
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol) 
        for security in changes.AddedSecurities:
            self.SetHoldings(security.Symbol, 0.10)

#1. Create a class SelectionData
class SelectionData:
    #2. Create a constructor that takes self 
    def __init__(self):
        #2. Save the fast and slow ExponentialMovingAverage
        self.slow = ExponentialMovingAverage(200)
        self.fast = ExponentialMovingAverage(50)
    
    #3. Check if our indicators are ready
    def is_ready(self):
        return self.slow.IsReady and self.fast.IsReady
    
    #4. Use the "indicator.Update" method to update the time and price of both indicators
    def update(self, time, price):
        self.slow.Update(time, price)
        self.fast.Update(time, price)
        
