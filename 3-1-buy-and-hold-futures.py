from math import floor


class BasicTemplateFuturesAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2013, 12, 20) 
        self.SetEndDate(2014, 2, 20) 
        self.SetCash(1000000) 
        self.gold = self.AddFuture(Futures.Metals.Gold) 
        self.gold.SetFilter(0, 90)
        self.Settings.FreePortfolioValuePercentage = 0.3
    
    def OnMarginCallWarning(self):
        self.Error("You received a margin call warning..")
        
    def OnData(self, slice):
        for chain in slice.FutureChains:
            self.popularContracts = [contract for contract in chain.Value if contract.OpenInterest > 1000]
            if len(self.popularContracts) == 0:
                continue
            sortedByOIContracts = sorted(self.popularContracts, key=lambda k : k.OpenInterest, reverse=True)
            self.liquidContract = sortedByOIContracts[0]
            if not self.Portfolio.Invested:
                self.SetHoldings(self.liquidContract.Symbol, 1)
