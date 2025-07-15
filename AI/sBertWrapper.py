import pickle

class sBertWrapper:
    def __init__(self, model):
        self.model = model

    def encode(self, text):
        text_embed = self.model.encode(text)
        return text_embed

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self, f)

    @staticmethod
    def load(filename):
        with open(filename, 'rb') as f:
            return pickle.load(f)