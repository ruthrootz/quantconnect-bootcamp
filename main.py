class BootCampTask(QCAlgorithm):

    def Initialize(self):
        self.AddEquity("SPY", Resolution.Daily)
        self.SetCash(25000)
        
    def OnData(self, data):
        pass
