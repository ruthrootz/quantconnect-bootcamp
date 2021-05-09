class FrameworkAlgorithm(QCAlgorithm):
    
    def Initialize(self):
        
        self.SetStartDate(2013, 10, 1)   
        self.SetEndDate(2013, 12, 1)    
        self.SetCash(100000)

        #1. Set the NullUniverseSelectionModel()
        self.SetUniverseSelection(NullUniverseSelectionModel())
        
        #2. Set the NullAlphaModel()
        self.SetAlpha(NullAlphaModel())

        #3. Set the NullPortfolioConstructionModel()
        self.SetPortfolioConstruction(NullPortfolioConstructionModel())

        #4. Set the NullRiskManagementModel()
        self.SetRiskManagement(NullRiskManagementModel())

        #5. Set the NullExecutionModel()
        self.SetExecution(NullExecutionModel())
