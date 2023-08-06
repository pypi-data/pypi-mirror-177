from randomlib.modelRepo.mahaBERT import BERTModel

class MaskPredictor(BERTModel):
    def __init__(self, modelName = 'marathi-bert-v2'):
        self.modelName = modelName
        super().__init__(self.modelName)

    def predictMask(self, text, details: str = "minimum", as_dict: bool = False):
        return super().predictMask(text, details, as_dict)

    def listModels(self):
        return super().listModels()