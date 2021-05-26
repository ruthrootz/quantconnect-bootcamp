class AlertMagentaAlligator(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 11, 20)
        self.SetCash(100000)
        self.AddEquity('SBUX', Resolution.Minute)
        self.AddEquity('TSLA', Resolution.Minute)
        self.AddEquity('BAC', Resolution.Minute)
        self.sbux = self.AddEquity('SBUX', Resolution.Daily)
        self.tsla = self.AddEquity('TSLA', Resolution.Daily)
        self.bac = self.AddEquity('BAC', Resolution.Daily)
        self.sbuxMomentum = self.MOMP('SBUX', 50, Resolution.Daily)
        self.tslaMomentum = self.MOMP('TSLA', 50, Resolution.Daily)
        self.bacMomentum = self.MOMP('BAC', 50, Resolution.Daily)

    def OnData(self, data):
        if self.IsWarmingUp:
            return
        if not self.Time.weekday() == 1:
            return
        if self.sbuxMomentum.Current.Value > self.tslaMomentum.Current.Value and self.sbuxMomentum.Current.Value > self.bacMomentum.Current.Value:
            self.Liquidate('TSLA')
            self.Liquidate('BAC')
            self.SetHoldings('SBUX', 1)
        if self.tslaMomentum.Current.Value > self.sbuxMomentum.Current.Value and self.tslaMomentum.Current.Value > self.bacMomentum.Current.Value:
            self.Liquidate('SBUX')
            self.Liquidate('BAC')
            self.SetHoldings('TSLA', 1)
        if self.bacMomentum.Current.Value > self.tslaMomentum.Current.Value and self.bacMomentum.Current.Value > self.sbuxMomentum.Current.Value:
            self.Liquidate('TSLA')
            self.Liquidate('SBUX')
            self.SetHoldings('BAC', 1)
