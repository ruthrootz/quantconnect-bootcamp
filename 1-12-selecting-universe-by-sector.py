from datetime import timedelta
from QuantConnect.Data.UniverseSelection import * 
from Selection.FundamentalUniverseSelectionModel import FundamentalUniverseSelectionModel
from Portfolio.EqualWeightingPortfolioConstructionModel import EqualWeightingPortfolioConstructionModel

class SectorBalancedPortfolioConstruction(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2016, 12, 28) 
        self.SetEndDate(2017, 3, 1) 
        self.SetCash(100000) 
        self.UniverseSettings.Resolution = Resolution.Hour
        self.SetUniverseSelection(MyUniverseSelectionModel())
        self.SetAlpha(ConstantAlphaModel(InsightType.Price, InsightDirection.Up, timedelta(1), 0.025, None))
        self.SetPortfolioConstruction(MySectorWeightingPortfolioConstructionModel(Resolution.Daily))
        self.SetExecution(ImmediateExecutionModel())

class MyUniverseSelectionModel(FundamentalUniverseSelectionModel):

    def __init__(self):
        super().__init__(True, None, None)

    def SelectCoarse(self, algorithm, coarse):
        filtered = [x for x in coarse if x.HasFundamentalData and x.Price > 0]
        sortedByDollarVolume = sorted(filtered, key=lambda x: x.DollarVolume, reverse=True)
        return [x.Symbol for x in sortedByDollarVolume][:100]

    def SelectFine(self, algorithm, fine):
        filtered = [f for f in fine if f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.Technology]
        self.technology = sorted(filtered, key=lambda f: f.MarketCap, reverse=True)[:3]
        filtered = [f for f in fine if f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.FinancialServices]
        self.financialServices = sorted(filtered, key=lambda f: f.MarketCap, reverse=True)[:2]
        filtered = [f for f in fine if f.AssetClassification.MorningstarSectorCode == MorningstarSectorCode.ConsumerDefensive]
        self.consumerDefensive = sorted(filtered, key=lambda f: f.MarketCap, reverse=True)[:1]
        return [x.Symbol for x in self.technology + self.financialServices + self.consumerDefensive]
        
class MySectorWeightingPortfolioConstructionModel(EqualWeightingPortfolioConstructionModel):

    def __init__(self, rebalance = Resolution.Daily):
        super().__init__(rebalance)
        self.symbolBySectorCode = dict()

    def OnSecuritiesChanged(self, algorithm, changes):
        
        for security in changes.AddedSecurities:
            #1. When new assets are added to the universe, save the Morningstar sector code 
            # for each security to the variable sectorCode
            sectorCode = security.Fundamentals.AssetClassification.MorningstarSectorCode
            # 2. If the sectorCode is not in the self.symbolBySectorCode dictionary, create a new list 
            # and append the symbol to the list, keyed by sectorCode in the self.symbolBySectorCode dictionary 
            if sectorCode not in self.symbolBySectorCode:
                self.symbolBySectorCode[sectorCode] = list()
            self.symbolBySectorCode[sectorCode].append(security.Symbol)
        for security in changes.RemovedSecurities:
            #3. For securities that are removed, save their Morningstar sector code to sectorCode
            
            #4. If the sectorCode is in the self.symbolBySectorCode dictionary
            if sectorCode in self.symbolBySectorCode:
                symbol = security.Symbol
                # If the symbol is in the dictionary's sectorCode list;
                if symbol in sectorCode: 
                    # Then remove the corresponding symbol from the dictionary
                    self.symbolBySectorCode.remove(symbol)
        # We use the super() function to avoid using the base class name explicity
        super().OnSecuritiesChanged(algorithm, changes)

