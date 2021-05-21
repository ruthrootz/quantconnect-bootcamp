from math import floor

class BasicTemplateFuturesAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2013, 12, 20) 
        self.SetEndDate(2014, 2, 20) 
        self.SetCash(1000000) 
        self.gold = self.AddFuture(Futures.Metals.Gold) 
        self.gold.SetFilter(0, 90)
 
    def OnMarginCallWarning(self):
        self.Error("This is a margin call warning. The assets will be liquidated to cover losses.")
        
    def OnData(self, slice):
      
        for chain in slice.FutureChains:
            self.popularContracts = [contract for contract in chain.Value if contract.OpenInterest > 1000]
 
            if len(self.popularContracts) == 0:
                continue
            
            sortedByOIContracts = sorted(self.popularContracts, key=lambda k : k.OpenInterest, reverse=True)
            self.liquidContract = sortedByOIContracts[0]
  
            if not self.Portfolio.Invested:
                
                #1. Save the notional value of the futures contract to self.notionalValue  
                self.notionalValue = self.liquidContract.AskPrice * self.liquidContract.SymbolProperties.ContractMultiplier
                
                #2. Save the contract security object to the variable future
                future = self.Securities[self.liquidContract.Symbol]
                
                #3. Calculate the number of contracts we can afford based on the margin required
                # Divide the margin remaining by the initial margin and save to self.contractsToBuy
                self.contractsToBuy = floor(self.Portfolio.MarginRemaining / future.BuyingPowerModel.InitialOvernightMarginRequirement)
                
                #4. Make a market order for the number of contracts we calculated for that symbol
                self.MarketOrder(liquidContract.Symbol, self.contractsToBuy)
