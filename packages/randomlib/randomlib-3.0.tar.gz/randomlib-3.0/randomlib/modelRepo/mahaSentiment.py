from transformers import AutoTokenizer, AutoModelForSequenceClassification
from transformers import pipeline
import pandas as pd
from ..config import paths

class SentimentModel:
    def __init__(self, modelName='MarathiSentiment'):
        self.modelName = modelName
        self.modelRoute = paths[self.modelName]
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelRoute)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.modelRoute)
        self.classifier = pipeline('text-classification',
                              model=self.model, tokenizer=self.tokenizer)
    def getPolarityScore(self, text):
        result = self.classifier(text)
        df = pd.DataFrame.from_dict(result)
        return df

    def listModels(self):
            for model in paths:
                print(model, ": ", paths[model], "\n")