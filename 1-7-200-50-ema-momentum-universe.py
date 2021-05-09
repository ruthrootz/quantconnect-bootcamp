class EMAMomentumUniverse(QCAlgorithm):
    
    def Initialize(self):
        self.SetStartDate(2019, 1, 7)
        self.SetEndDate(2019, 4, 1)
        self.SetCash(100000)
        self.UniverseSettings.Resolution = Resolution.Daily
        self.AddUniverse(self.CoarseSelectionFunction)
        
        #1. Create our dictionary and save it to self.averages
        self.averages = {}
    
    def CoarseSelectionFunction(self, universe):  
        selected = []
        universe = sorted(universe, key=lambda c: c.DollarVolume, reverse=True)  
        universe = [c for c in universe if c.Price > 10][:100]
        
        # Create loop to use all the coarse data
        for coarse in universe:  
            symbol = coarse.Symbol 
            
            #2. Check if we've created an instance of SelectionData for this symbol
            if symbol not in self.averages:
                #3. Create a new instance of SelectionData and save to averages[symbol]
                self.averages[symbol] = SelectionData()
            #4. Update the symbol with the latest coarse.AdjustedPrice data
            self.averages[symbol].update(self.Time, coarse.AdjustedPrice)
            #5. Check if 50-EMA > 200-EMA and if so append the symbol to selected list.
            if self.averages[symbol].fast > self.averages[symbol].slow:
                if self.averages[symbol].is_ready():
                    selected.append(symbol)
        return selected[:10]
        
    def OnSecuritiesChanged(self, changes):
        for security in changes.RemovedSecurities:
            self.Liquidate(security.Symbol)
       
        for security in changes.AddedSecurities:
            self.SetHoldings(security.Symbol, 0.10)
            
class SelectionData(object):
    def __init__(self):
        self.slow = ExponentialMovingAverage(200)
        self.fast = ExponentialMovingAverage(50)
    
    def is_ready(self):
        return self.slow.IsReady and self.fast.IsReady
    
    def update(self, time, price):
        self.fast.Update(time, price)
        self.slow.Update(time, price)
        
