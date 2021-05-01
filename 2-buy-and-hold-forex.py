class BootCampTask(QCAlgorithm):

    def Initialize(self):
        self.SetCash(100000)
        self.SetStartDate(2017, 5, 1)
        self.SetEndDate(2017, 5, 31)
        self.audusd = self.AddForex("AUDUSD", Resolution.Hour, Market.Oanda)
        self.SetBrokerageModel(BrokerageName.OandaBrokerage)
        
    def OnData(self, data):
        if not self.Portfolio.Invested:
            self.MarketOrder("AUDUSD", 2000)
