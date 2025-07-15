from AI.sBertWrapper import sBertWrapper

def load_sBert():
    wrapper = sBertWrapper.load('bert_entrenado.pkl')
    return wrapper
