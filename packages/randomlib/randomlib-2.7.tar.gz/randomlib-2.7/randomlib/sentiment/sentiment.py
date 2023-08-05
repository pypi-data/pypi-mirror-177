from randomlib.modelRepo.mahaSentiment import SentimentModel

class SentimentAnalyzer(SentimentModel):
    def __init__(self, modelName = 'MarathiSentiment'):
        self.modelName = modelName
        super().__init__(self.modelName)

    def getPolarityScore(self, text):
        return super().getPolarityScore(text)

    def listModels(self):
        return super().listModels()
