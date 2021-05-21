class BootCampTask(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2013, 12, 20) 
        self.SetEndDate(2014, 2, 20) 
        self.SetCash(1000000) 
   
        #1. Request Gold futures and save the gold security
        self.gold = self.AddFuture(Futures.Metals.Gold)
        
        #2. Set our expiry filter to return all contracts expiring within 90 days
        self.gold.SetFilter(0, 90)
