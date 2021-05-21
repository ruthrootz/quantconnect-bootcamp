class BootCampTask(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2013, 12, 20) 
        self.SetEndDate(2014, 2, 20) 
        self.SetCash(1000000) 
        self.gold = self.AddFuture(Futures.Metals.Gold) 
        self.gold.SetFilter(0, 90)
      
    def OnData(self, slice):
       
        # Loop over each available futures chain from slice.FutureChains data
        for chain in slice.FutureChains:
            
            #1. Filter to choose popular contracts with OpenInterest > 1000
            self.popularContracts = [x for x in chain if x.OpenInterest > 1000]
            
            #2. If the length of contracts in this chain is zero, continue to the next chain
            if len(self.popularContracts) == 0:
                break
            
            #3. Sort our contracts by open interest in descending order and save to sortedByOIContracts
            sortedByOIContracts = sorted(self.popularContracts, key=lambda k : k.OpenInterest, reverse=True)
            
            #4. Save the contract with the highest open interest to self.liquidContract
            self.liquidContract = sortedByOIContracts[0]
            
