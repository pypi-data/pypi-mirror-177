from randomlib.modelRepo.mahaHate import HateModel

class HateAnalyzer(HateModel):
    def __init__(self, modelName = 'mahahate-bert'):
        self.modelName = modelName
        super().__init__(self.modelName)

    def getPolarityScore(self, text):
        return super().getPolarityScore(text)

    def listModels(self):
        return super().listModels()
