from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import pipeline
import pandas as pd
from ..config import paths

class GPTModel:
    def __init__(self, modelName='marathi-gpt'):
        self.modelName = modelName
        self.modelRoute = paths[self.modelName]
        self.tokenizer = AutoTokenizer.from_pretrained(self.modelRoute)
        self.model = AutoModelForCausalLM.from_pretrained(self.modelRoute)
        self.classifier = pipeline('text-generation',
                              model=self.model, tokenizer=self.tokenizer)

    def nextWord(self, text, numOfPredictions = 1):
        result = self.classifier(text, max_new_tokens = 1, num_return_sequences = numOfPredictions)
        df = pd.DataFrame.from_dict(result)
        # print(df)
        return df.style.set_properties(**{'text-align': 'left'}).set_table_styles([dict(selector = 'th', props=[('text-align', 'left')])])

    def completeSentence(self, text, numOfWords = 25, numOfPredictions = 1):
        result = self.classifier(text, max_new_tokens = numOfWords, num_return_sequences = numOfPredictions)
        df = pd.DataFrame.from_dict(result)
        # print(df)
        return df.style.set_properties(**{'text-align': 'left'}).set_table_styles([dict(selector = 'th', props=[('text-align', 'left')])])

    def listModels(self):
            for model in paths:
                print(model, ": ", paths[model], "\n")
