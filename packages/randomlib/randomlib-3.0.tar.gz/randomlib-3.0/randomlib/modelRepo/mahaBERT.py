from transformers import BertTokenizer, BertForMaskedLM
from transformers import pipeline
from IPython.display import display
import pandas as pd
from ..config import paths

class BERTModel:
    def __init__(self, modelName='marathi-bert-v2'):
        self.modelName = modelName
        self.modelRoute = paths[self.modelName]
        self.task = "fill-mask"

        self.tokenizer = BertTokenizer.from_pretrained(self.modelRoute)
        self.model = BertForMaskedLM.from_pretrained(self.modelRoute)
        self.generator = pipeline(task = self.task,
                                    model=self.model,
                                    tokenizer=self.tokenizer)

    def predictMask(self,text: str,details: str = "minimum",as_dict: bool = False):
        if text.find(self.tokenizer.mask_token) == -1:
            print("Please mask your sentence first!")
            return None
        try:
            self.predictions = pd.DataFrame(self.generator(text))
        except Exception as e:
            print("Error in Model" + str(e))

        self.predictions['token_str'] = self.predictions['token_str'].apply(lambda word: word.replace(" ",""))

        if details == 'minimum':
            custom_predict = self.predictions[['token_str','sequence']]

        if details == "medium":
            custom_predict = self.predictions[['token_str','score','sequence']]

        if details == "all":
            custom_predict = self.predictions

        if as_dict:
            return custom_predict.to_dict('records')
        return custom_predict


    def listModels(self):
            for model in paths:
                print(model, ": ", paths[model], "\n")
